# file: env.py
# author: Adam Brychta

import json

EOL_LIN = "\n"
EOL_MAC = "\r"

CONFIG_ENV_OBJECT = "envObject"
CONFIG_ENV_OBJECT_NAME = "name"
CONFIG_ENV_OBJECT_CHAR = "char"
CONFIG_ENV_OBJECT_TRAVERSABLE = "traversable"
CONFIG_ENV_OBJECT_IMG = "img"


class EnvObject:
    def __init__(self, name, char, traversable, img):
        self.name = name
        self.char = char
        self.traversable = traversable
        self.img = img


class Env:
    def __init__(self):
        self.state = None
        self.env_objects = None
        self.rows = 0
        self.cols = 0
        self.running = True

    def init(self, file_path_config):
        self.env_objects = []
        self._config_load(file_path_config)

    def reset(self, file_path_world):
        self.state = load_world(file_path_world)
        self.rows = len(self.state)
        self.cols = len(self.state[0])
        return self.state.copy()

    def _config_load(self, file_path_config):
        f = open(file_path_config, encoding="utf8", mode="r")
        if f is None:
            return None
        config = json.load(f)
        for json_env_object in config[CONFIG_ENV_OBJECT]:
            env_object = EnvObject(json_env_object[CONFIG_ENV_OBJECT_NAME], json_env_object[CONFIG_ENV_OBJECT_CHAR],
                                   json_env_object[CONFIG_ENV_OBJECT_TRAVERSABLE],
                                   json_env_object[CONFIG_ENV_OBJECT_IMG])
            self.env_objects.append(env_object)
        f.close()

    def step(self, action):
        if action is None:
            self.running = False
            return self.state.copy()
        if self.running:
            self.state = action(self.state)
        return self.state.copy()

    def get_env_object_type_char(self, char):
        for env_object in self.env_objects:
            if env_object.char == char:
                return env_object
        return None

    def get_env_object_type_name(self, name):
        for env_object in self.env_objects:
            if env_object.name == name:
                return env_object
        return None


def load_world(file_path):
    f = open(file_path, encoding="utf8", mode="r")
    if f is None:
        return None
    state = [[]]
    world = f.read()
    # Vytvori pole reprezentujici stav prostredi ze stringu na vstupu.
    for char in world:
        if char == EOL_LIN:
            # Prida dalsi radek matice.
            state.append([])
        elif char != EOL_LIN:
            # Prida znak.
            state[len(state) - 1].append(char)

    f.close()

    return state


def get_char_pos(state, char):
    # Vraci pozici prvniho nalezeneho znaku char.
    for row in range(len(state)):
        for col in range(len(state[row])):
            if state[row][col] == char:
                return row, col
    return None, None
