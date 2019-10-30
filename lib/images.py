from PIL import Image, ImageDraw, ImageFont

from lib.constants import Y_POSITION, X_POSITIONS


def getLiccScore(syllables):
    score = Image.open("./resources/thelicc.png")
    draw = ImageDraw.Draw(score)
    font = ImageFont.truetype("./resources/arial.ttf", 28)
    x_index = 0
    for word in syllables:
        prev_x = 0
        for syllable in word:
            x = X_POSITIONS[x_index] + (len(syllable) * 10 / 2 if len(syllable) < 5 else 0)
            draw.text(xy=(x, Y_POSITION), text=syllable, fill="black", font=font)
            if len(word) > 1 and syllable != word[0]:
                draw.text(xy=(x - (x - prev_x) / 2, Y_POSITION), text="-", fill="black", font=font)
            x_index += 1
            prev_x = x + len(syllable) * 7.5
    return score

