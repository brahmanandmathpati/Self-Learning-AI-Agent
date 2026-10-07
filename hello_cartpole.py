import gymnasium as gym

env = gym.make("CartPole-v1")
env.action_space.seed(0)  # makes the random actions repeatable too

for episode in range(5):
    state, info = env.reset(seed=episode)  # seed = same start every time
    total_reward, done = 0.0, False
    while not done:
        action = env.action_space.sample()  # random: push left (0) or right (1)
        state, reward, terminated, truncated, info = env.step(action)
        total_reward += float(reward)
        done = terminated or truncated
    print(f"Episode {episode}: reward = {total_reward}")

env.close()
