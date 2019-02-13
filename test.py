if __name__ == '__main__':
    import gym
    import gym_android_wechat_jump

    env = gym.make('android-wechat-jump-v0')
    for _ in range(1000):
        done = False
        observation = env.reset()
        while not done:
            env.render()
            action = env.action_space.sample()[0]
            observation, reward, done, info = env.step(action)
            print(f'action={action}, reward={reward}, done={done}')
