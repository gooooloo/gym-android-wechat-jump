import cv2
import time
import os

import sys
_PATH_ = os.path.dirname(os.path.dirname(__file__))

if _PATH_ not in sys.path:
    sys.path.append(_PATH_)

from gym_android_wechat_jump.env.device import Device
from gym_android_wechat_jump.env.config import cfg as cfg


def main():
    p = '/tmp/myscore.png'
    cnt = 0
    while True:
        Device.capture(p)

        img = cv2.imread(p, cv2.IMREAD_GRAYSCALE)

        width = cfg.SCORE_DIGIT_WIDTH
        height = cfg.SCORE_DIGIT_HEIGHT
        top = cfg.SCORE_DIGIT_TOP
        left_1 = cfg.SCORE_DIGIT_LEFT_1
        left_2 = cfg.SCORE_DIGIT_LEFT_2
        score_area1 = img[top:top+height, left_1:left_1+width]
        score_area2 = img[top:top+height, left_2:left_2+width]

        cv2.imwrite(f'/tmp/myscore.{cnt}.1.png', score_area1)
        cv2.imwrite(f'/tmp/myscore.{cnt}.2.png', score_area2)
        cnt += 1
        time.sleep(1)


if __name__ == '__main__':
    main()
