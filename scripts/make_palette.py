import json
import os
from typing import List

import numpy as np
import pandas as pd
from entity import AnalyzedImage, Playlist
from utils import write_to_json_file

# ************************************
# const values / properties
# **********************************/


ANALYZED_IMAGES_JSON_FILE_PATHS = [
    f"{os.path.dirname(__file__)}/../output/analyzed_video_json/{playlist.player}/analyzed_video_list.json"
    for playlist in Playlist
]
COLOR_MAP_REPORT_FILE_PATH = f"{os.path.dirname(__file__)}/../output/report/color_map/report.json"

REPORT_FILE_PATH = f"{os.path.dirname(__file__)}/../output/report/summary/report.json"

# ************************************
# functions
# **********************************/


def load_videos() -> pd.DataFrame:
    videos = np.array(
        load_alanyzed_video_json(ANALYZED_IMAGES_JSON_FILE_PATHS[0])
        + load_alanyzed_video_json(ANALYZED_IMAGES_JSON_FILE_PATHS[1])
    )

    df = pd.DataFrame(
        videos,
        columns=["analyzed_video"],
        index=list(map(lambda video: video.videoID, videos)),
    )

    df["videoID"] = list(map(lambda video: video.videoID, df["analyzed_video"]))

    df["bin_hue"] = pd.cut(list(map(lambda video: video.hls["hue"], list(df["analyzed_video"]))), 12, labels=False)

    df["rgb"] = list(
        map(
            lambda video: f"#{int(video.rgb[0]):02x}{int(video.rgb[1]):02x}{int(video.rgb[2]):02x}",
            df["analyzed_video"],
        )
    )

    df["lightness"] = list(map(lambda video: video.hls["lightness"], df["analyzed_video"]))

    return df


def make_palette() -> None:
    videos = load_videos()

    color_mapping = []

    for key in videos.groupby("bin_hue").groups.keys():
        pics_in_same_group = videos.groupby("bin_hue").groups[key]
        pics_in_same_group_sorted = list(
            map(
                lambda item: {"videoID": item.videoID, "rgb": format_rgb(item.rgb)},
                list(videos.reindex(index=pics_in_same_group).sort_values("lightness")["analyzed_video"]),
            )
        )
        pics_in_same_group_sorted.reverse()
        color_mapping.append(pics_in_same_group_sorted)

    write_to_json_file(COLOR_MAP_REPORT_FILE_PATH, color_mapping)


def format_rgb(rgb: List[str]) -> str:
    return f"#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}"


def sort_by_primary_color(video: AnalyzedImage) -> int:
    return video.primaryColor.order


def sort_by_rgb(video: AnalyzedImage) -> int:
    r = int(video.rgb[0])
    g = int(video.rgb[1])
    b = int(video.rgb[2])
    return (r * 1000 + g) * 1000 + b


def sort_by_hls(video: AnalyzedImage) -> float:
    return video.hls["hue"]


def load_alanyzed_video_json(json_path: str) -> List[AnalyzedImage]:
    with open(json_path, mode="r") as file:
        return list(map(lambda item: AnalyzedImage.from_json(item), json.load(file)))


# ************************************
# main
# **********************************/


def main() -> None:
    make_palette()


if __name__ == "__main__":
    main()
