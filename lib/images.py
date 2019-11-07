from PIL import Image, ImageDraw, ImageFont

from lib.constants import Y_POSITION, X_POSITIONS

font = ImageFont.truetype("./resources/jazztext-regular.ttf", 32)

def getLiccScore(syllables):
    """
    Writes the given syllables on a score of THE LICC as the lyrics.

    :param syllables: a list in the format of what words.getHyphenation(str) returns
    :return: the edited image.
    """
    score = Image.open("./resources/thelicc.png")
    draw = ImageDraw.Draw(score)
    x_index = 0
    hyphen_size = draw.textsize(text="-", font=font)[0]
    for word in syllables:
        prev_end = 0
        for syllable in word:
            # black magic image manipulation. Might break if you change anything. Don't ask me
            size = draw.textsize(text=syllable, font=font)[0]
            x = X_POSITIONS[x_index] - (size / 2)            
            draw.text(xy=(x, Y_POSITION), text=syllable, fill="black", font=font)
            # if there are more than one syllable in this word and the current syllable is not the first, add a hyphen
            if len(word) > 1 and syllable != word[0]:                
                draw.text(xy=(((x + prev_end) - hyphen_size) / 2, Y_POSITION), text="-", fill="black", font=font)
            x_index += 1
            prev_end = x + size
    return score

