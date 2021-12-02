import json
import os

import requests
from entity import Playlist, YoutubeVideoItem
from utils import calc_image_file_name, get_unixtime


# ************************************
# functions
# **********************************/
def get_images(image_dir_path: str, json_file_path: str) -> None:
    with open(json_file_path, mode="r") as file:
        video_list = list(map(lambda item: YoutubeVideoItem.from_json(item), json.load(file)))

        for video in video_list:
            fetch_thumbnail(image_dir_path, video)


def fetch_thumbnail(image_dir_path: str, video: YoutubeVideoItem) -> None:
    videoID = video.videoID
    unixtime = get_unixtime(video)
    small_thumbnail_url = video.thumbnailMedium.url

    response = requests.get(small_thumbnail_url)
    if response.status_code != 200:
        raise Exception(f"failed to fetch image: url = {small_thumbnail_url}")

    print(calc_image_file_name(image_dir_path, unixtime, videoID))

    with open(calc_image_file_name(image_dir_path, unixtime, videoID), mode="wb") as fout:
        fout.write(response.content)


# ************************************
# main
# **********************************/
def main() -> None:
    for playlist in Playlist:
        images_dir_path = f"{os.path.dirname(__file__)}/../output/images/{playlist.player}"
        json_file_path = f"{os.path.dirname(__file__)}/../output/video_json/{playlist.player}/video_list.json"

    get_images(images_dir_path, json_file_path)


if __name__ == "__main__":
    main()
