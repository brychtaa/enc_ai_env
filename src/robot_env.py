# file: robot_env.py
# author: Adam Brychta

from src.env import Env, get_char_pos

DIRT = "dirt"
DOCK = "dock"
ROBOT = "robot"
WALL = "wall"


class Direction:
    NORTH = "north"
    SOUTH = "south"
    WEST = "west"
    EAST = "east"


class RobotEnv(Env):
    def __init__(self):
        super().__init__()
        self.env_object_robot_on_dirt_east = None
        self.env_object_robot_on_dirt_west = None
        self.env_object_robot_on_dirt_south = None
        self.env_object_robot_on_dirt_north = None
        self.env_object_robot_east = None
        self.env_object_robot_west = None
        self.env_object_robot_south = None
        self.env_object_robot_north = None
        self.env_object_dock = None
        self.env_object_robot_docked = None
        self.env_object_dirt = None
        self.env_object_floor = None
        self.env_object_wall = None

        # Pole uchovavajici vsechny reprezentace robota.
        self.env_object_robot_arr = []
        self.env_object_robot_on_dirt_arr = []

    def init(self, file_path_config):
        super(RobotEnv, self).init(file_path_config)
        self.env_object_wall = self.get_env_object_type_name("wall")
        self.env_object_floor = self.get_env_object_type_name("floor")
        self.env_object_dirt = self.get_env_object_type_name("dirt")
        self.env_object_robot_docked = self.get_env_object_type_name("robot_docked")
        self.env_object_dock = self.get_env_object_type_name("dock")
        self.env_object_robot_north = self.get_env_object_type_name("robot_north")
        self.env_object_robot_south = self.get_env_object_type_name("robot_south")
        self.env_object_robot_west = self.get_env_object_type_name("robot_west")
        self.env_object_robot_east = self.get_env_object_type_name("robot_east")
        self.env_object_robot_on_dirt_north = self.get_env_object_type_name("robot_on_dirt_north")
        self.env_object_robot_on_dirt_south = self.get_env_object_type_name("robot_on_dirt_south")
        self.env_object_robot_on_dirt_west = self.get_env_object_type_name("robot_on_dirt_west")
        self.env_object_robot_on_dirt_east = self.get_env_object_type_name("robot_on_dirt_east")

        # Zalezi na poradi v poli pro spravnou rotaci robota. Rotace do prava +1, do leva -1.
        self.env_object_robot_arr.append(self.env_object_robot_north)
        self.env_object_robot_arr.append(self.env_object_robot_east)
        self.env_object_robot_arr.append(self.env_object_robot_south)
        self.env_object_robot_arr.append(self.env_object_robot_west)

        self.env_object_robot_on_dirt_arr.append(self.env_object_robot_on_dirt_north)
        self.env_object_robot_on_dirt_arr.append(self.env_object_robot_on_dirt_east)
        self.env_object_robot_on_dirt_arr.append(self.env_object_robot_on_dirt_south)
        self.env_object_robot_on_dirt_arr.append(self.env_object_robot_on_dirt_west)

    def get_pos_robot(self):
        for env_object in self.env_object_robot_arr:
            row_robot, col_robot = get_char_pos(self.state, env_object.char)
            if row_robot is not None:
                return row_robot, col_robot
        for env_object in self.env_object_robot_on_dirt_arr:
            row_robot, col_robot = get_char_pos(self.state, env_object.char)
            if row_robot is not None:
                return row_robot, col_robot
        row_robot, col_robot = get_char_pos(self.state, self.env_object_robot_docked.char)
        if row_robot is not None:
            return row_robot, col_robot
        return None, None

    def rotate(self, right):
        row_robot, col_robot = self.get_pos_robot()
        char_robot = self.state[row_robot][col_robot]
        env_object_robot = self.get_env_object_type_char(char_robot)

        if DOCK in env_object_robot.name:
            return

        # Offset pro rotaci.
        if right:
            offset = 1
        else:
            offset = -1

        if DIRT in env_object_robot.name:
            # Je na spine.
            index = find_pos_arr(self.env_object_robot_on_dirt_arr, env_object_robot) + offset
            if index >= len(self.env_object_robot_arr):
                index = 0
            self.state[row_robot][col_robot] = self.env_object_robot_on_dirt_arr[index].char
        else:
            index = find_pos_arr(self.env_object_robot_arr, env_object_robot) + offset
            if index >= len(self.env_object_robot_arr):
                index = 0
            self.state[row_robot][col_robot] = self.env_object_robot_arr[index].char

    def move(self):
        # Aktualni poloha agenta.
        row_robot, col_robot = self.get_pos_robot()
        if row_robot is None:
            return
        row_new = None
        col_new = None
        env_object_robot = self.get_env_object_type_char(self.state[row_robot][col_robot])

        # Najde souradnice kam se robot posunuje.
        if (Direction.NORTH in env_object_robot.name) or (env_object_robot.name == self.env_object_robot_docked.name):
            row_new = row_robot - 1
            col_new = col_robot
        elif Direction.EAST in env_object_robot.name:
            row_new = row_robot
            col_new = col_robot + 1
        elif Direction.SOUTH in env_object_robot.name:
            row_new = row_robot + 1
            col_new = col_robot
        elif Direction.WEST in env_object_robot.name:
            row_new = row_robot
            col_new = col_robot - 1

        # Zkontroluje zda je souradnice validni.
        if row_new < 0 or row_new >= len(self.state) or col_new < 0 or col_new >= len(self.state[row_new]):
            return

        # Zkontroluje, zda je policko na ktere se chce robot presunout traversable.
        place_new = self.state[row_new][col_new]
        env_object_type_new = self.get_env_object_type_char(place_new)
        if not env_object_type_new.traversable:
            # Na policko nelze vstoupit.
            print("not traversable")
            return

        # Nahradi svoji pozici spravnym znakem.
        env_object_type_act = self.get_env_object_type_char(self.state[row_robot][col_robot])
        env_object_type_replace = None
        if env_object_type_act.name == "robot_docked":
            env_object_type_replace = self.env_object_dock
        elif DIRT in env_object_type_act.name:
            env_object_type_replace = self.env_object_dirt
        elif ROBOT in env_object_type_act.name:
            env_object_type_replace = self.env_object_floor

        if env_object_type_replace is None:
            return

        # Zjisti na jake policko se zmeni cil.
        env_object_type_replace2 = None
        if env_object_type_new.name == "floor":
            if (Direction.NORTH in env_object_robot.name) or (
                    env_object_robot.name == self.env_object_robot_docked.name):
                env_object_type_replace2 = self.env_object_robot_north
            elif Direction.EAST in env_object_robot.name:
                env_object_type_replace2 = self.env_object_robot_east
            elif Direction.SOUTH in env_object_robot.name:
                env_object_type_replace2 = self.env_object_robot_south
            elif Direction.WEST in env_object_robot.name:
                env_object_type_replace2 = self.env_object_robot_west
        if env_object_type_new.name == DIRT:
            if (Direction.NORTH in env_object_robot.name) or (DOCK in env_object_robot.name):
                env_object_type_replace2 = self.env_object_robot_on_dirt_north
            elif Direction.EAST in env_object_robot.name:
                env_object_type_replace2 = self.env_object_robot_on_dirt_east
            elif Direction.SOUTH in env_object_robot.name:
                env_object_type_replace2 = self.env_object_robot_on_dirt_south
            elif Direction.WEST in env_object_robot.name:
                env_object_type_replace2 = self.env_object_robot_on_dirt_west
        if env_object_type_new.name == "dock":
            env_object_type_replace2 = self.env_object_robot_docked

        if env_object_type_replace2 is None:
            return

        # Nahradi pozici robota objektem pod nim.
        self.state[row_robot][col_robot] = env_object_type_replace.char
        # Nahradi policko na ktere robot vjede.
        self.state[row_new][col_new] = env_object_type_replace2.char

    def clean(self):
        row_robot, col_robot = self.get_pos_robot()
        if row_robot is None:
            return

        env_object_robot = self.get_env_object_type_char(self.state[row_robot][col_robot])

        # Vycisti policko.
        if DIRT in env_object_robot.name:
            if Direction.NORTH in env_object_robot.name:
                self.state[row_robot][col_robot] = self.env_object_robot_north.char
            elif Direction.EAST in env_object_robot.name:
                self.state[row_robot][col_robot] = self.env_object_robot_east.char
            elif Direction.SOUTH in env_object_robot.name:
                self.state[row_robot][col_robot] = self.env_object_robot_south.char
            elif Direction.WEST in env_object_robot.name:
                self.state[row_robot][col_robot] = self.env_object_robot_west.char


def find_pos_arr(env_object_arr, env_obj):
    for index in range(len(env_object_arr)):
        if env_object_arr[index].name == env_obj.name:
            return index
    return None


robot_world = RobotEnv()


def move_forward(state):
    robot_world.state = state
    robot_world.move()
    return robot_world.state


def rotate_left(state):
    robot_world.state = state
    robot_world.rotate(False)
    return robot_world.state


def rotate_right(state):
    robot_world.state = state
    robot_world.rotate(True)
    return robot_world.state


def clean(state):
    robot_world.state = state
    robot_world.clean()
    return robot_world.state


def turn_off(_):
    return None
