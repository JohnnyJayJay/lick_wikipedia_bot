import pronouncing
import urllib
import re
import math

from lib.constants import (
    BANNED_WORDS,
    BANNED_PHRASES,
    CHARS_ONLY,
    PRONUNCIATION_OVERRIDES,
    LICK_STRESSES,
)
from num2words import num2words as n2w


def isLick(title: str):
    """Checks if a Wikipedia page title has the same stress pattern as The Lick.

    >>> isLick('Audio induction loop')
    True

    >>> isTMNT('Peter Alexander Hay')
    True

    >>> isTMNT('Romeo, Romeo, wherefore art thou, Romeo?')
    False
    """
    if containsBanned(title):
        return False

    title = cleanStr(title)
    title_stresses = getTitleStresses(title)

    if (not title_stresses) or (not title_stresses[0]):
        return False

    return True if LICK_STRESSES.match(title_stresses[0]) else False


def containsBanned(title: str):
    """Return True if banned words or phrases in string.

    This implementation is slow, but is was fast to write and I don't care about
    speed for this script.
    """

    def _containsBannedWord(title: str):
        for word in title.split():
            word = CHARS_ONLY.sub("", word.lower())
            if word in BANNED_WORDS:
                return True
        return False

    def _containsBannedPhrase(title: str):
        for phrase in BANNED_PHRASES:
            if phrase in title.lower():
                return True
        return False

    return _containsBannedWord(title) or _containsBannedPhrase(title)


def getTitleStresses(title: str):
    """Takes a wikipedia title and gets the combined stresses of all words.

    >>> getTitleStresses('Teenage Mutant Ninja Turtles')
    '12101010'

    Args:
        title: String, title of a wikipedia page.
    Returns:
        String, stresses of each syllable as 0, 1, and 2s.
    """
    title_words = title.split()
    title_stresses = ""
    title_split = []
    while title_words:
        word = title_words.pop(0)
        word_stresses = getWordStresses(word)
        # If word was a long number, it may have been parsed into several words.
        if isinstance(word_stresses, list):
            title_words = word_stresses + title_words
        elif isinstance(word_stresses, tuple):
            title_stresses += word_stresses[0]
            title_split.append(word_stresses[1])

    print((title, title_stresses, " ".join(title_split)))
    return (title_stresses, " ".join(title_split))


def getWordStresses(word: str):
    word = numbersToWords(word)
    if " " in word:
        return word.split()

    for override, stresses in PRONUNCIATION_OVERRIDES:
        if word.lower() == override.lower():
            return stresses

    try:
        phones = pronouncing.phones_for_word(word)
        stresses = pronouncing.stresses(phones[0])
        syllable_count = pronouncing.syllable_count(phones[0])
        chunks, chunk_size = len(word), int(math.ceil(len(word)/syllable_count))
        syllables = [ word[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
        syllables_hyphenated = "".join(intersperse(syllables, "-"))
    except IndexError:
        # Hacky way of discarding candidate title
        return ("?", "")
    return (stresses, syllables_hyphenated)

def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result

def numbersToWords(word):
    ordinal_number_endings = ("nd", "rd", "st", "th")
    if word.isdigit():
        if len(word) == 4:
            try:
                word = n2w(word, to="year")
            except Exception:
                # Hacky way of discarding candidate title
                return "9"
        else:
            try:
                word = n2w(word)
            except Exception:
                # Hacky way of discarding candidate title
                return "9"
    if word[:-2].isdigit() and word[-2:] in ordinal_number_endings:
        word = word[-2:]
        try:
            word = n2w(word, to="ordinal")
        except Exception:
            # Hacky way of discarding candidate title
            return "9"

    return word


def cleanStr(s: str):
    """Remove characters that the pronouncing dictionary doesn't like.

    This isn't very efficient, but it's readable at least. :-)

    >>> cleanStr('fooBar123')
    'fooBar123'

    >>> cleanStr('Hello ([world])')
    'Hello world'

    >>> cleanStr('{hello-world}')
    'hello world'

    Args:
        s: String to be stripped of offending characters
    Returns:
        String without offending characters
    """
    DEL_CHARS = ["(", ")", "[", "]", "{", "}", ",", ":", ";", "."]
    SWAP_CHARS = [("-", " ")]

    for char in DEL_CHARS:
        s = s.replace(char, "")

    for char, replacement in SWAP_CHARS:
        s = s.replace(char, replacement)

    return s


def getWikiUrl(title: str):
    title = title.replace(" ", "_")
    title = urllib.parse.quote_plus(title)
    return "https://en.wikipedia.org/wiki/" + title
