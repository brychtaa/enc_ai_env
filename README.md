# enc_ai_env
Agentní prostředí.

![Example start](/docs/img/example_action.png)
![Example matrix](/docs/img/example_matrix.png)

## Ovládání
* Šipka nahoru - pohyb robota vpřed.
* Šipka do leva - rotace robota do leva.
* Šipka do prava - rotace robota do prava.
* Mezerník - akce vyčisti.

## Examples

### Použití Env a RobotEnv

```python
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
```

### Příklad agenta

```Python
def example_agent(env_state, history, memory):
    return move_forward
```
