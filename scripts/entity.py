from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Tuple


class PrimaryColor(Enum):
    """
    PrimaryColor is enum that holds rgb data for each 10 major colors
    """

    R = ("red", 1000, 255, 0, 0)
    RY = ("red_yellow", 2000, 243, 123, 0)
    Y = ("yellow", 3000, 242, 226, 0)
    YG = ("yellow_green", 4000, 84, 236, 0)
    G = ("green", 0, 5000, 197, 0)
    BG = ("blue_green", 6000, 0, 165, 131)
    B = ("blue", 7000, 0, 86, 212)
    PB = ("purple_blue", 8000, 47, 0, 234)
    P = ("purple", 9000, 142, 0, 207)
    RP = ("red_purple", 10000, 244, 0, 180)
    # DEBUG = ("debug", 0, 0, 0)

    def __init__(self, code: str, order: int, r: int, g: int, b: int):
        self.code = code
        self.order = order
        self.r = r
        self.g = g
        self.b = b

    @classmethod
    def find_by_code(cls, code: str) -> "PrimaryColor":
        for pc in PrimaryColor:
            if pc.code == code:
                return pc

        raise Exception("invalid code is passed")


class Playlist(Enum):
    """
    # How to find playlist_id:
    1. get channel id: https://support.google.com/youtube/answer/3250431?hl=en&sjid=17154660641541136582-AP
    2. replace the suffix: UC with UU
    """
    PONPOKO = ("ponpoko", "UU1EB8moGYdkoZQfWHjh7Ivw")
    PEANUTS_KUN = ("peanuts_kun", "UUmgWMQkenFc72QnYkdxdoKA")
    EMIMIYA = ("emimiya", "UU7nveTHQ4hYw8_xRrfeNUdw")

    def __init__(self, player: str, playlist_id: str):
        self.player = player
        self.playlist_id = playlist_id


@dataclass
class Thumbnail:
    url: str
    width: int
    height: int

    @classmethod
    def from_json(cls, json: Dict[str, Any]) -> "Thumbnail":
        return Thumbnail(url=str(json["url"]), width=int(json["width"]), height=int(json["height"]))


@dataclass
class YoutubeVideoItem:
    """
    YoutubeVideoItem is data model for youtube api's response
    """

    title: str
    videoID: str
    publishedAt: str
    position: int
    thumbnailHigh: Thumbnail
    thumbnailMedium: Thumbnail
    thumbnailDefault: Thumbnail

    @classmethod
    def from_json(cls, json: Dict[str, Any]) -> "YoutubeVideoItem":
        return YoutubeVideoItem(
            title=str(json["title"]),
            videoID=str(json["videoID"]),
            position=int(json["position"]),
            publishedAt=str(json["publishedAt"]),
            thumbnailHigh=Thumbnail.from_json(json["thumbnailHigh"]),
            thumbnailMedium=Thumbnail.from_json(json["thumbnailMedium"]),
            thumbnailDefault=Thumbnail.from_json(json["thumbnailDefault"]),
        )

    @classmethod
    def from_response(cls, item: Dict[str, Any]) -> "YoutubeVideoItem":
        return YoutubeVideoItem(
            title=str(item["snippet"]["title"]),
            videoID=str(item["contentDetails"]["videoId"]),
            position=int(item["snippet"]["position"]),
            publishedAt=str(item["contentDetails"]["videoPublishedAt"]),
            thumbnailHigh=Thumbnail.from_json(item["snippet"]["thumbnails"]["high"]),
            thumbnailMedium=Thumbnail.from_json(item["snippet"]["thumbnails"]["medium"]),
            thumbnailDefault=Thumbnail.from_json(item["snippet"]["thumbnails"]["default"]),
        )


@dataclass
class AnalyzedImage:
    videoID: str
    details: YoutubeVideoItem
    rgb: Tuple[int, int, int]
    hls: Dict[str, float]
    primaryColor: PrimaryColor

    @classmethod
    def from_json(cls, json: Dict[str, Any]) -> "AnalyzedImage":
        return AnalyzedImage(
            videoID=str(json["videoID"]),
            rgb=json["rgb"],
            hls=json["hls"],
            details=YoutubeVideoItem.from_json(json["details"]),
            primaryColor=PrimaryColor.find_by_code(json["primaryColor"]["code"]),
        )
