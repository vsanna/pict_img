import json
import os
from pathlib import Path
from typing import List, Tuple

import numpy as np
import numpy.typing as npt
import pandas as pd
from entity import AnalyzedImage, Playlist, PrimaryColor
from PIL import Image
from utils import write_to_json_file

# ************************************
# const values / properties
# **********************************/

# 32 : 18 = 16: 9 =

IMAGE_NAMES = [
    # "kenmochitoya_test.jpg",
    "kenmochitoya.jpg",
    "kenmochitoya2.jpg",
]


ANALYZED_IMAGES_JSON_FILE_PATH = f"{os.path.dirname(__file__)}/../output/analyzed_video_json/peanuts_kun/analyzed_video_list.json"

# ************************************
# functions
# **********************************/


def load_alanyzed_video_json(json_path: str) -> List[AnalyzedImage]:
    with open(json_path, mode="r") as file:
        return list(map(lambda item: AnalyzedImage.from_json(item), json.load(file)))


def make_video_df() -> pd.DataFrame:
    videos = np.array(
        load_alanyzed_video_json(ANALYZED_IMAGES_JSON_FILE_PATH)
    )
    df = pd.DataFrame(videos, columns=["analyzed_video"], index=list(map(lambda video: video.videoID, videos)))
    df["rgb"] = list(
        map(
            lambda video: f"#{int(video.rgb[0]):02x}{int(video.rgb[1]):02x}{int(video.rgb[2]):02x}",
            df["analyzed_video"],
        )
    )

    return df.sort_values("rgb")


def gen_pict_img(image_name: str) -> None:
    videos = make_video_df()

    pict_img_json_file_path = f"{os.path.dirname(__file__)}/../output/pict_img/kenmochitoya/{image_name}/pict_img.json"
    image_filepath = f"{os.path.dirname(__file__)}/../output/images/kenmochitoya/{image_name}"

    with Image.open(image_filepath) as image_file:
        color_matrix = np.array(image_file)
        w_size, h_size, n_color = color_matrix.shape
        color_matrix = color_matrix.reshape(w_size * h_size, n_color)

        pict_map = [find_closest_pic(i, color_matrix, videos) for i in range(len(color_matrix))]

        write_to_json_file(
            pict_img_json_file_path, list(map(lambda row: list(row), list(np.array(pict_map).reshape(w_size, h_size))))
        )


def find_closest_pic(i: int, color_matrix: npt.NDArray[Tuple[int, int, int]], videos: pd.DataFrame) -> PrimaryColor:
    rgb = color_matrix[i]
    index = [video.videoID for video in list(videos["analyzed_video"])]
    distances = np.array([distance(rgb, video, i) for video in list(videos["analyzed_video"])])
    return pd.DataFrame(distances, index=index).idxmin()[0]


def distance(point: Tuple[int, int, int], video: AnalyzedImage, index: int) -> float:
    pc = np.array([int(video.rgb[0]), int(video.rgb[1]), int(video.rgb[2])])
    ans = np.sqrt(np.power((point - pc), 2).sum())
    return ans


# ************************************
# main
# **********************************/


def main() -> None:
    for image_name in IMAGE_NAMES:
        gen_pict_img(image_name)


if __name__ == "__main__":
    main()
