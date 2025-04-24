from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json


def get_playlist_id(youtube, channel_id):
    channel_response = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()

    return channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]


def fetch_latest_content(channel_id, config):
    YOUTUBE_API_KEY = config["YOUTUBE_API_KEY"]
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=YOUTUBE_API_KEY
    )

    if not channel_id:
        print("Error: channel_id is required.")
        return None

    uploads_playlist_id = get_playlist_id(youtube, channel_id)

    try:
        playlist_response = youtube.playlistItems().list(
            part="snippet",
            playlistId=uploads_playlist_id,
            maxResults=1
        ).execute()

    except KeyError as e:
        print(
            f"KeyError: No se pudo encontrar la clave '{e.args[0]}' en latest_video")

    except HttpError as e:
        with open('error-log.json', 'a') as f:
            json.dump({
                "message": f"An HTTP error {e.resp.status} occurred: {e.content}"
            }, f, indent=4)
            f.write("\n")
        return {
            "error": True,
            "message": f"An HTTP error {e.resp.status} occurred: {e.content}"
        }
    except Exception as e:
        print(f"Ocurrió un error inesperado: {str(e)}")

    last_video = playlist_response["items"][0]
    return last_video
