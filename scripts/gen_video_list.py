import os
from typing import List

import requests
from entity import Playlist, YoutubeVideoItem
from utils import getenv_or_error, write_to_json_file

import typer

# ************************************
# const values / properties
# **********************************/

API_ENDPOINT = "https://youtube.googleapis.com/youtube/v3/playlistItems"
PART = "id,contentDetails,snippet,status"
YOUTUBE_API_KEY = getenv_or_error("YOUTUBE_API_KEY")


app = typer.Typer()

# ************************************
# functions
# **********************************/
def _get_video_list(playlist: Playlist) -> List[YoutubeVideoItem]:
    video_list: List[YoutubeVideoItem] = []
    page_token = ""
    sum = 0

    while True:
        print("fetching a page of playlist...")

        response = requests.get(
            f"{API_ENDPOINT}?part={PART}&playlistId={playlist.playlist_id}&key={YOUTUBE_API_KEY}&pageToken={page_token}",
            headers={"Accept": "application/json"},
        )
        if response.status_code != 200:
            raise Exception("failed to retrieve response")

        data = response.json()
        sum += len(data["items"])
        print(
            f"retrieved a page successfully. num of items in this page: {len(data['items'])}, "
            + f"(sum:{sum} / total:{data['pageInfo']['totalResults']})"
        )

        video_list = video_list + list(map(YoutubeVideoItem.from_response, data["items"]))

        if "nextPageToken" not in data or data["nextPageToken"] is None:
            break
        else:
            page_token = data["nextPageToken"]

    return video_list


@app.command()
def gen_video_list(target: str):
    if target == "ponpoko":
        playlists = [Playlist.PONPOKO]
    elif target == "emimiya":
        playlists = [Playlist.EMIMIYA]
    else:
        raise Exception("invalid target is passed")

    print(f"target: {target}. playlists: {playlists}")

    for playlist in playlists:
        list = _get_video_list(playlist)
        json_file_path = f"{os.path.dirname(__file__)}/../output/video_json/{playlist.player}/video_list.json"
        write_to_json_file(json_file_path, list)



# ************************************
# main
# **********************************/
if __name__ == "__main__":
    app()

