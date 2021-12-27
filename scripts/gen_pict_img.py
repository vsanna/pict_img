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

WIDTH = 320
HEIGHT = 180

TARGET_VIDEOS = {
    # review on 2020
    "b5VxEOiHvdY": {"player": "ponpoko", "unixtime": "1608613742"},
    # ponpoko in a pinch
    "Kbfrw9yFGx0": {"player": "ponpoko", "unixtime": "1597370406"},
    # ponpoko vs peanuts kun
    "IgBtOvlj2X8": {"player": "ponpoko", "unixtime": "1612070712"},
    # gachi
    "n8msiA8RNxg": {"player": "ponpoko", "unixtime": "1575162009"},
    # Season1/vol1
    "s-jGOeYdKt8": {"player": "peanuts_kun", "unixtime": "1499140878"},
    # virtuafreak live
    "_nXnvHit0R4": {"player": "peanuts_kun", "unixtime": "1619413214"},
    # gumi
    "9VhrJCbr58A": {"player": "peanuts_kun", "unixtime": "1592881215"},
    # tohpea 2020
    "BVC-dRCz-4A": {"player": "peanuts_kun", "unixtime": "1608876007"},
    # demo
    # "p3nYromZQiQ": {"player": "ponpoko", "unixtime": "1520873861"},
}


ANALYZED_IMAGES_JSON_FILE_PATHS = [
    f"{os.path.dirname(__file__)}/../output/analyzed_video_json/{playlist.player}/analyzed_video_list.json"
    for playlist in Playlist
]

# ************************************
# functions
# **********************************/


def load_alanyzed_video_json(json_path: str) -> List[AnalyzedImage]:
    with open(json_path, mode="r") as file:
        return list(map(lambda item: AnalyzedImage.from_json(item), json.load(file)))


def make_video_df() -> pd.DataFrame:
    videos = np.array(
        load_alanyzed_video_json(ANALYZED_IMAGES_JSON_FILE_PATHS[0])
        + load_alanyzed_video_json(ANALYZED_IMAGES_JSON_FILE_PATHS[1])
    )
    df = pd.DataFrame(videos, columns=["analyzed_video"], index=list(map(lambda video: video.videoID, videos)))
    df["rgb"] = list(
        map(
            lambda video: f"#{int(video.rgb[0]):02x}{int(video.rgb[1]):02x}{int(video.rgb[2]):02x}",
            df["analyzed_video"],
        )
    )

    return df.sort_values("rgb")


def gen_pict_img(player: str, videoID: str, unixtime: str, pict_img_json_file_path: str) -> None:
    videos = make_video_df()

    image_filepath = f"{os.path.dirname(__file__)}/../output/images/{player}/{unixtime}_{videoID}.jpg"

    with Image.open(image_filepath) as image_file:
        resized_image = image_file.resize((WIDTH, HEIGHT))
        resized_image.save(f"output/resized_images/{HEIGHT}x{WIDTH}/{videoID}.jpg")

        color_matrix = np.array(image_file)
        w_size, h_size, n_color = color_matrix.shape
        color_matrix = color_matrix.reshape(w_size * h_size, n_color)

        pict_map = [find_closest_pic(i, color_matrix, videos) for i in range(len(color_matrix))]

        write_to_json_file(
            pict_img_json_file_path, list(map(lambda row: list(row), list(np.array(pict_map).reshape(HEIGHT, WIDTH))))
        )


def find_closest_pic(i: int, color_matrix: npt.NDArray[Tuple[int, int, int]], videos: pd.DataFrame) -> PrimaryColor:
    print(f"finding {i}th of {WIDTH*HEIGHT} pixel's closest img...")

    rgb = color_matrix[i]
    index = [video.videoID for video in list(videos["analyzed_video"])]
    distances = np.array([distance(rgb, video) for video in list(videos["analyzed_video"])])
    return pd.DataFrame(distances, index=index).idxmin()[0]


def distance(point: Tuple[int, int, int], video: AnalyzedImage) -> float:
    pc = np.array([int(video.rgb[0]), int(video.rgb[1]), int(video.rgb[2])])
    ans = np.sqrt(np.power((point - pc), 2).sum())
    return ans


# ************************************
# main
# **********************************/


def main() -> None:
    for videoID in TARGET_VIDEOS:
        player = TARGET_VIDEOS[videoID]["player"]
        unixtime = TARGET_VIDEOS[videoID]["unixtime"]

        Path(f"{os.path.dirname(__file__)}/../output/pict_img/{HEIGHT}x{WIDTH}/{videoID}").mkdir(
            parents=True, exist_ok=True
        )
        pict_img_json_file_path = (
            f"{os.path.dirname(__file__)}/../output/pict_img/{HEIGHT}x{WIDTH}/{videoID}/pict_img.json"
        )

        gen_pict_img(player, videoID, unixtime, pict_img_json_file_path)


if __name__ == "__main__":
    main()
