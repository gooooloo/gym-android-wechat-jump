import cv2
import os
from config import cfg as cfg


def ocr(img):
    assert img.shape == (cfg.SCORE_DIGIT_HEIGHT, cfg.SCORE_DIGIT_WIDTH)

    color_target = cfg.SCORE_COLOR_TARGET
    my_int = None

    # TODO: the magic numbers ( like 25, 60, etc) belongs to cfg as well...
    if img[1][1] != color_target:
        my_int = None
    elif img[25][25] == color_target:
        my_int = 1
    elif img[60][25] == color_target:
        if img[40][40] == color_target:
            my_int = 7
        else:
            my_int = 4
    elif img[40][40] != color_target:
        my_int = 0
    elif img[60][60] != color_target:
        my_int = 2
    elif img[25][5] != color_target:
        my_int = 3
    elif img[60][5] != color_target:
        if img[25][60] != color_target:
            my_int = 5
        else:
            my_int = 9
    elif img[25][60] != color_target:
            my_int = 6
    else:
        my_int = 8

    return int(my_int) if my_int is not None else None


def main():
    d = os.path.dirname(os.path.realpath(__file__))

    for i in range(10):
        img = cv2.imread(f'{d}/score_png_as_ref/{i}.png', cv2.IMREAD_GRAYSCALE)
        my_int = ocr(img)
        assert my_int == i, f'expect {i}, actual {my_int}'

    img = cv2.imread(f'{d}/score_png_as_ref/none.png', cv2.IMREAD_GRAYSCALE)
    my_int = ocr(img)
    assert my_int is None, f'expect {None}, actual {my_int}'


if __name__ == '__main__':
    main()
