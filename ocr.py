import cv2
import os


def ocr(img):
    assert img.shape == (85,69)

    COLOR_TARGET = 72
    myint = None

    if img[1][1] != COLOR_TARGET:
        myint = None
    elif img[25][25] == COLOR_TARGET:
        myint = 1
    elif img[60][25] == COLOR_TARGET:
        if img[40][40] == COLOR_TARGET:
            myint = 7
        else:
            myint = 4
    elif img[40][40] != COLOR_TARGET:
        myint = 0
    elif img[60][60] != COLOR_TARGET:
        myint = 2
    elif img[25][5] != COLOR_TARGET:
        myint = 3
    elif img[60][5] != COLOR_TARGET:
        if img[25][60] != COLOR_TARGET:
            myint = 5
        else:
            myint = 9
    elif img[25][60] != COLOR_TARGET:
            myint = 6
    else:
        myint = 8

    return int(myint) if myint is not None else None


def main():
    d = os.path.dirname(os.path.realpath(__file__))

    for i in range(10):
        img = cv2.imread(f'{d}/score_png_as_ref/{i}.png', cv2.IMREAD_GRAYSCALE)
        myint = ocr(img)
        assert myint == i, f'expect {i}, actual {myint}'

    img = cv2.imread(f'{d}/score_png_as_ref/none.png', cv2.IMREAD_GRAYSCALE)
    myint = ocr(img)
    assert myint is None, f'expect {None}, actual {myint}'


if __name__ == '__main__':
    main()
