#!/usr/bin/env python3
import sys
import time

import wikipedia

from lib import images
from lib import twitter
from lib import words
from lib.constants import BACKOFF, MAX_ATTEMPTS, TIMEOUT_BACKOFF


def test():
    syllables = searchForLick(MAX_ATTEMPTS, BACKOFF)
    images.getLiccScore(syllables).show()


def main():
    syllables = searchForLick(MAX_ATTEMPTS, BACKOFF)
    score = images.getLiccScore(syllables)
    path = f"./temp/licc-{int(time.time())}.png"
    score.save(path)
    _ = twitter.sendTweet(path)


def searchForLick(attempts=MAX_ATTEMPTS, backoff=BACKOFF):
    """Loop MAX_ATTEMPT times, searching for a Lick meter wikipedia title.

    Args:
        Integer: attempts, retries remaining.
        Integer: backoff, seconds to wait between each loop.
    Returns:
        The syllables of a matching wikipedia title
    """
    for attempt in range(attempts):
        print(f"\r{str(attempt * 10)} articles fetched...", end="")
        sys.stdout.flush()
        title = getRandomLickTitle()
        if title is not None:
            print(f"\nFound match: {title}")
            syllables = words.adjustHyphenation(words.getHyphenation(title))
            if syllables is not None:
                return syllables

        time.sleep(backoff)

    print(f"\nNo matches found.")
    sys.exit(1)


def getRandomLickTitle():
    """Get 10 random wiki titles, check if any of them isLick().

    We grab the max allowed Wikipedia page titles (10) using wikipedia.random().
    If any title is in Lick meter, return the title. Otherwise, return None.

    Args:
        None
    Returns:
        String or None: The Lick compliant title, or None if none found.
    """
    wikipedia.set_rate_limiting(True)
    try:
        titles = wikipedia.random(10)
    except wikipedia.exceptions.HTTPTimeoutError as e:
        print(f"Wikipedia timout exception: {e}")
        time.sleep(TIMEOUT_BACKOFF)
        main()
    except wikipedia.exceptions.WikipediaException as e:
        print(f"Wikipedia exception: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Exception while fetching wiki titles: {e}")
        sys.exit(1)

    for title in titles:
        if words.isLick(title):
            return title
    return None


if __name__ == "__main__":
    main()
