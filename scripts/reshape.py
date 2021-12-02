import json
import os

import numpy as np
from utils import write_to_json_file

# ************************************
# const values / properties
# **********************************/

WIDTH = 320
HEIGHT = 180

PICT_IMG_JSON_FILE_PATH = f"{os.path.dirname(__file__)}/../output/pict_img/{HEIGHT}x{WIDTH}/pict_img.json"

# ************************************
# functions
# **********************************/


def reshape() -> None:
    with open(PICT_IMG_JSON_FILE_PATH, mode="r") as file:
        data = np.array(json.load(file)).reshape(HEIGHT, WIDTH)
        print(data.shape)
        write_to_json_file(
            PICT_IMG_JSON_FILE_PATH, list(map(lambda row: list(row), list(np.array(data).reshape(HEIGHT, WIDTH))))
        )


# ************************************
# main
# **********************************/


def main() -> None:
    reshape()


if __name__ == "__main__":
    main()
