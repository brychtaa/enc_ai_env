# file: env.py
# author: Adam Brychta
import codecs
import json
import os
import zipfile

EOL_LIN = "\n"
EOL_MAC = "\r"

CONFIG_ENV_OBJECT = "envObject"
CONFIG_ENV_OBJECT_NAME = "name"
CONFIG_ENV_OBJECT_CHAR = "char"
CONFIG_ENV_OBJECT_TRAVERSABLE = "traversable"
CONFIG_ENV_OBJECT_IMG = "img"

ENCODING = 'utf-8'


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

    def init(self, path):
        file_content = get_file_content_from_zip(path, "env.json")
        self.env_objects = []
        self._config_load(file_content)

    def reset(self, path):
        file_content = get_file_content_from_zip(path, "default.map")
        self.state = load_world(file_content)
        self.rows = len(self.state)
        self.cols = len(self.state[0])
        return self.state.copy()

    def _config_load(self, file_content):
        if file_content is None:
            return None
        config = json.loads(file_content)
        for json_env_object in config[CONFIG_ENV_OBJECT]:
            env_object = EnvObject(json_env_object[CONFIG_ENV_OBJECT_NAME], json_env_object[CONFIG_ENV_OBJECT_CHAR],
                                   json_env_object[CONFIG_ENV_OBJECT_TRAVERSABLE],
                                   json_env_object[CONFIG_ENV_OBJECT_IMG])
            self.env_objects.append(env_object)

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


def load_world(file_content):
    if file_content is None:
        return None
    state = [[]]
    # Vytvori pole reprezentujici stav prostredi ze stringu na vstupu.
    for char in file_content:
        if char == EOL_LIN:
            # Prida dalsi radek matice.
            state.append([])
        elif char != EOL_LIN:
            # Prida znak.
            state[len(state) - 1].append(char)
    return state


def get_char_pos(state, char):
    # Vraci pozici prvniho nalezeneho znaku char.
    for row in range(len(state)):
        for col in range(len(state[row])):
            if state[row][col] == char:
                return row, col
    return None, None


def get_file_content_from_zip(path, file_name, archive_ext=".zip"):
    if ".zip" in path:
        f = None
        if ".zip" in os.path.basename(path):
            archive = zipfile.ZipFile(path, "r")
            for archive_file_path in archive.namelist():
                if archive_file_path.endswith(file_name):
                    f = archive.open(archive_file_path)
        else:
            archive = zipfile.ZipFile(path[:path.index(archive_ext) + len(archive_ext)], "r")
            f = archive.open(path[path.index(archive_ext) + len(archive_ext) + 1:], mode="r")
        if f is None:
            return None
        content = ""
        for line in codecs.iterdecode(f, ENCODING):
            content += line
        return content
    else:
        # Pokud je to soubor.
        if os.path.isdir(path):
            # Jedna se o slozku s konfiguracnimi souboru.
            f = open(path + file_name, encoding=ENCODING, mode="r")
        else:
            f = open(path, encoding=ENCODING, mode="r")
        content = f.read()
        f.close()
        return content
