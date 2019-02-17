import gym
from gym import spaces

import numpy as np
import time
from gym_android_wechat_jump.env.device import Device
from gym_android_wechat_jump.env.ocr import ocr
import cv2
from gym_android_wechat_jump.env.config import cfg as cfg


class WechatJumpEnv(gym.Env):

    metadata = {'render.modes': ['human']}
    
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

        # With reward == 0 condition, we limit the game to increase score every single step.
        if self.reward <= 0:
            self.done = True
            self.reward = 0
            return

        # TODO: fix cases that score > 99
        if self.last_score >= 99:
            self.done = True
            self.reward = 0
            return

    @staticmethod
    def is_background(bgr):
        bgr_low, bgr_high = cfg.BG_COLOR_BGR_LOW, cfg.BG_COLOR_BGR_HIGH
        for c in range(3):
            if bgr[c] < bgr_low[c] or bgr[c] > bgr_high[c]:
                return False
        return True

    def _read_screen(self):
        Device.capture(cfg.PNG_ON_PC)
        bgr = cv2.imread(cfg.PNG_ON_PC)
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        crop = bgr[cfg.STATE_AREA_TOP:cfg.STATE_AREA_BOTTOM, :, :]
        resize = cv2.resize(crop, (self.STATE_SIZE, self.STATE_SIZE))
        binary = np.asarray([0 if self.is_background(resize[r,c,:]) else 255
                             for r in range(resize.shape[0]) for c in range(resize.shape[1])
                             ], np.uint8)
        binary.shape = resize.shape[:2]
        return binary, gray

    def __init__(self):
        self.state = None
        self.done = False
        self.reward = 0
        self.last_score = 0

        self.STATE_SIZE = 84

        self.action_space = spaces.Box(low=100, high=1200, shape=(1,), dtype=np.int32)
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.STATE_SIZE, self.STATE_SIZE,), dtype=np.uint8)

    def step(self, action):

        # FIXME
        if self.done:
            action = 1500

        Device.jump(action)

        t0 = time.time()

        state1, s1 = self._read_screen()
        while True:

            if time.time() - t0 > cfg.MAX_WAIT_SECONDS_AFTER_JUMP:
                break

            state2, s2 = self._read_screen()
            if np.array_equal(state1, state2):
                break
            s1 = s2
            state1 = state2

        self._handle_score(s1)
        self.state = state1
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
        self.state = cv2.resize(self.state[cfg.STATE_AREA_TOP:cfg.STATE_AREA_BOTTOM, :],
                                (self.STATE_SIZE, self.STATE_SIZE))

        return self.state

    def render(self):
        pass


def main_local():
    from gym_android_wechat_jump.env.wechat_jump_env import WechatJumpEnv
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
