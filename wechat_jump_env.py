import gym
from gym import spaces

import numpy as np
import time
from device import Device
from ocr import ocr
import cv2
from config import cfg as cfg


class WechatJumpEnv(gym.Env):

    def _handle_score(self, img):

        width = cfg.SCORE_DIGIT_WIDTH
        height = cfg.SCORE_DIGIT_HEIGHT
        top = cfg.SCORE_DIGIT_TOP
        left_1 = cfg.SCORE_DIGIT_LEFT_1
        left_2 = cfg.SCORE_DIGIT_LEFT_2
        score_area1 = img[top:top+height, left_1:left_1+width]
        score_area2 = img[top:top+height, left_2:left_2+width]

        d1 = ocr(score_area1)
        d2 = ocr(score_area2)

        if d1 is None:
            self.done = True
            self.reward = 0
            return

        now_score = int(d1)
        if d2 is not None:
            now_score *= 10
            now_score += int(d2)

        self.reward = now_score - self.last_score
        self.last_score = now_score

        # TODO: fix cases that score > 99
        if self.last_score >= 99:
            self.done = True

    def __init__(self):
        self.state = None
        self.done = False
        self.reward = 0
        self.last_score = 0

        self.action_space = spaces.Box(low=100, high=1000, shape=(1,), dtype=np.int32)

    def step(self, action):

        # FIXME
        if self.done:
            action = 1500

        Device.jump(action)
        time.sleep(cfg.SLEEP_SECONDS_AFTER_JUMP)

        Device.capture(cfg.PNG_ON_PC)
        self.state = cv2.imread(cfg.PNG_ON_PC, cv2.IMREAD_GRAYSCALE)

        self._handle_score(self.state)
        info = {}  # TODO

        return self.state, self.reward, self.done, info

    def reset(self):
        if self.done:
            Device.reset()
            time.sleep(cfg.SLEEP_SECONDS_AFTER_RESET)

            self.done = False
            self.reward = 0
            self.last_score = 0

        Device.capture(cfg.PNG_ON_PC)
        self.state = cv2.imread(cfg.PNG_ON_PC, cv2.IMREAD_GRAYSCALE)
        self._handle_score(self.state)

        return self.state

    def render(self):
        pass


def main_local():
    from wechat_jump_env import WechatJumpEnv
    env = WechatJumpEnv()
    for _ in range(1000):
        done = False
        observation = env.reset()
        while not done:
            env.render()
            action = env.action_space.sample()[0]
            observation, reward, done, info = env.step(action)
            print(f'action={action}, reward={reward}, done={done}')


if __name__ == '__main__':
    main_local()
