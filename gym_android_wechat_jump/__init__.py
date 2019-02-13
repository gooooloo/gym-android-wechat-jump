from gym.envs.registration import register

register(
    id='android-wechat-jump-v0',
    entry_point='gym_android_wechat_jump.env:WechatJumpEnv',
)
