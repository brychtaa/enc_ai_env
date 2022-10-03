# file: run_example.py
# author: Adam Brychta

from example.keyboard_agent import keyboard_agent
from env.env_renderer import EnvRenderer
from env.robot_env import robot_env


def run_example(file_path_config, file_path_map):
    robot_env.init(file_path_config)
    state = robot_env.reset(file_path_map)
    history = []
    memory = None

    # Spusteni GUI.
    env_renderer = EnvRenderer()
    env_renderer.reset(robot_env)

    for epoch in range(1000):
        env_renderer.update(state)
        env_renderer.render()
        # Agentovi je predana kopie stavu prostredi, odkaz na historii
        # action = example_agent(state, history.copy(), memory)
        action = keyboard_agent(state, history.copy(), memory)
        history.append([state, action])
        state = robot_env.step(action)
        if state is None:
            print(epoch)
            break

    quit()
