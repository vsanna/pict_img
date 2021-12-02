import json
import os

from entity import Playlist, YoutubeVideoItem
from PIL import Image
from utils import calc_image_file_name, get_unixtime

# ************************************
# const values / properties
# **********************************/


# ************************************
# functions
# **********************************/


def gen_tidy_thumbnails(playlist: Playlist) -> None:
    json_file_path = f"{os.path.dirname(__file__)}/../output/video_json/{playlist.player}/video_list.json"

    with open(json_file_path, mode="r") as file:
        video_list = list(map(lambda item: YoutubeVideoItem.from_json(item), json.load(file)))

        video_list.reverse()

        for video in video_list:
            gen_tidy_thumbnail(playlist, video)


def gen_tidy_thumbnail(playlist: Playlist, video: YoutubeVideoItem) -> None:
    print(f"generating tidy thumbnail: {video.videoID}")

    images_dir_path = f"{os.path.dirname(__file__)}/../output/images/{playlist.player}"

    videoID = video.videoID
    unixtime = get_unixtime(video)
    image_filepath = calc_image_file_name(images_dir_path, unixtime, videoID)

    with Image.open(image_filepath) as image_file:
        resized_image = image_file.resize((40, 40))
        resized_image.save(f"output/resized_images/tidy/{videoID}.jpg")


# ************************************
# main
# **********************************/


def main() -> None:
    for playlist in Playlist:
        gen_tidy_thumbnails(playlist)


if __name__ == "__main__":
    main()
