import os
from gym_android_wechat_jump.env.config import cfg as cfg


class Device:

    @staticmethod
    def jump(ms):
        cmd = f'adb shell input swipe {cfg.COOR_X_SWIPE} {cfg.COOR_Y_SWIPE} {cfg.COOR_X_SWIPE} {cfg.COOR_Y_SWIPE} {ms}'
        # print('--->', cmd)
        os.system(cmd)

    @staticmethod
    def capture(path):
        cmd = f'adb shell screencap -p {cfg.PNG_ON_PHONE} && adb pull {cfg.PNG_ON_PHONE} {path} > /dev/null'
        # print('--->', cmd)
        os.system(cmd)

    @staticmethod
    def reset():
        cmd = f'adb shell input tap {cfg.COOR_X_RESET} {cfg.COOR_Y_RESET}'
        # print('--->', cmd)
        os.system(cmd)
