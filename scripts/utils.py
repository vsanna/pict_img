import json
import os
from datetime import datetime
from typing import Any, List

from entity import YoutubeVideoItem


def getenv_or_error(key: str) -> str:
    val = os.getenv(key)
    if val is None:
        raise BaseException(f"required environment variable({key}) is not set")
    return val


def get_unixtime(video: YoutubeVideoItem) -> int:
    return int(datetime.strptime(video.publishedAt, "%Y-%m-%dT%H:%M:%SZ").timestamp())


def calc_image_file_name(image_dir_path: str, unixtime: int, videoID: str) -> str:
    return f"{image_dir_path}/{unixtime}_{videoID}.jpg"


def write_to_json_file(file_path: str, items: List[Any]) -> None:
    content = json.dumps(
        items, ensure_ascii=False, indent=2, default=lambda o: o.__dict__ if hasattr(o, "__dict__") else str(o)
    )
    with open(file_path, mode="w") as file:
        file.write(content)
