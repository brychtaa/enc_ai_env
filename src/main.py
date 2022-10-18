# file: main.py
# author: Adam Brychta
from example.run_example import run_example


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--map", type=str, required=False)
    parser.add_argument("--config", type=str, required=False)

    return parser.parse_args()


def main(args):
    if args.map is None:
        # Lze definovat primo soubor, slozku se souborem, zip archiv nebo soubor v zip archivu.
        # file_path_map = "../res/robot_cleaner.zip"
        # file_path_config = "../res/robot_cleaner.zip"
        file_path_map = "../res/robot_cleaner.zip/robot_cleaner/default.map"
        file_path_config = "../res/robot_cleaner.zip/robot_cleaner/env.json"
    else:
        file_path_map = args.map
        file_path_config = args.config
    run_example(file_path_config, file_path_map)


if __name__ == '__main__':
    main(parse_args())
