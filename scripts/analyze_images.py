import colorsys
import json
import os
from typing import List, Tuple

import numpy as np
import numpy.typing as npt
import pandas as pd
import scipy.stats
from entity import AnalyzedImage, Playlist, PrimaryColor, YoutubeVideoItem
from PIL import Image
from sklearn.cluster import KMeans
from utils import calc_image_file_name, get_unixtime, write_to_json_file

# ************************************
# const values / properties
# **********************************/

# k_mean with n_clusters 2 is the best so far
ANALYZE_METHOD = "k_mean"  # "mean", "mode", "k_mean"

# ************************************
# functions
# **********************************/


def analyze_images(playlist: Playlist) -> List[AnalyzedImage]:
    json_file_path = f"{os.path.dirname(__file__)}/../output/video_json/{playlist.player}/video_list.json"

    analized_images = []
    with open(json_file_path, mode="r") as file:
        video_list = list(map(lambda item: YoutubeVideoItem.from_json(item), json.load(file)))

        video_list.reverse()

        for video in video_list:
            analized_images.append(analyze_image(playlist, video))

    return analized_images


def analyze_image(playlist: Playlist, video: YoutubeVideoItem) -> AnalyzedImage:
    print(f"analyzing video: {video.videoID}")

    images_dir_path = f"{os.path.dirname(__file__)}/../output/images/{playlist.player}"

    videoID = video.videoID
    unixtime = get_unixtime(video)
    image_filepath = calc_image_file_name(images_dir_path, unixtime, videoID)

    with Image.open(image_filepath) as image_file:
        color_matrix = np.array(image_file)
        w_size, h_size, n_color = color_matrix.shape
        color_matrix = color_matrix.reshape(w_size * h_size, n_color)

        rgb = None

        if ANALYZE_METHOD == "mean":
            rgb = mean(color_matrix)
        elif ANALYZE_METHOD == "mode":
            rgb = mode(color_matrix)
        elif ANALYZE_METHOD == "k_mean":
            rgb = k_mean(color_matrix)
        else:
            raise Exception("unsupported method")

        (hue, lightness, _) = colorsys.rgb_to_hls(rgb[0], rgb[1], rgb[2])
        hls = {"hue": hue, "lightness": lightness}

        Image.new("RGB", (100, 100), rgb).save(
            f"output/primary_color/{ANALYZE_METHOD}/{playlist.player}/{unixtime}_{videoID}.jpg"
        )

        return AnalyzedImage(videoID, video, rgb, hls, closest_primary_color(rgb))


def mean(color_matrix: npt.NDArray[Tuple[int, int, int]]) -> Tuple[int, int, int]:
    color_mean = np.mean(color_matrix, axis=0)
    color_mean = color_mean.astype(int)
    return tuple(color_mean)


def mode(color_matrix: npt.NDArray[Tuple[int, int, int]]) -> Tuple[int, int, int]:
    color_code = ["{:02x}{:02x}{:02x}".format(*elem) for elem in color_matrix]
    mode, _ = scipy.stats.mode(color_code)
    r = int(mode[0][0:2], 16)
    g = int(mode[0][2:4], 16)
    b = int(mode[0][4:6], 16)
    return (r, g, b)


def k_mean(color_matrix: npt.NDArray[Tuple[int, int, int]]) -> Tuple[int, int, int]:
    # grouping each pixel's colors into two clusters
    cluster = KMeans(n_clusters=2, max_iter=300, random_state=0)
    cluster.fit(X=color_matrix)
    centers = cluster.cluster_centers_.astype(int, copy=False)
    # pick the center closer to the center of all pixels
    mindist = np.sqrt(np.power((centers - color_matrix.mean(axis=0)), 2).sum(axis=1)).min()
    idx = np.where(np.sqrt(np.power((centers - color_matrix.mean(axis=0)), 2).sum(axis=1)) == mindist)[0][0]
    return tuple(cluster.cluster_centers_.astype(int, copy=False)[idx])


def closest_primary_color(rgb: Tuple[int, int, int]) -> PrimaryColor:
    index = [pc for pc in PrimaryColor]
    distances = np.array([distance(rgb, pc) for pc in PrimaryColor])
    return pd.DataFrame(distances, index=index, columns=["cnt"]).idxmin()[0]


def distance(point: Tuple[int, int, int], primary_color: PrimaryColor) -> float:
    pc = np.array([primary_color.r, primary_color.g, primary_color.b])
    ans = np.sqrt(np.power((point - pc), 2).sum())
    return ans


# ************************************
# main
# **********************************/


def main() -> None:

    for playlist in Playlist:
        analyzed_images_json_file_paths = (
            f"{os.path.dirname(__file__)}/../output/analyzed_video_json/{playlist.player}/analyzed_video_list.json"
        )

        videos = analyze_images(playlist)
        write_to_json_file(analyzed_images_json_file_paths, videos)


if __name__ == "__main__":
    main()
