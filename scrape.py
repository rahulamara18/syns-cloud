import spotipy
import requests
import base64
import datetime
from json import dump
from spotipy.oauth2 import SpotifyClientCredentials

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

name = input("Name: ")
artist_id = input("ID: ")

artist = spotify.artist(artist_id)

data = {
    "name": name,
    "full_name": artist["name"],
    "genre": artist["genres"][0],
    "image": base64.b64encode(requests.get(artist["images"][0]["url"]).content).decode(
        "utf-8"
    ),
    "albums": [],
}

for album in spotify.artist_albums(artist_id, album_type="album")["items"]:
    res = input(f"{album['name']} y/n: ").lower()
    if res == "n":
        continue

    album_data = {
        "name": album["name"],
        "year": album["release_date"][:4],
        "image": base64.b64encode(
            requests.get(album["images"][0]["url"]).content
        ).decode("utf-8"),
        "tracks": [],
    }
    for song in spotify.album_tracks(album["id"])["items"]:
        seconds, ms = divmod(song["duration_ms"], 1000)
        minutes, seconds = divmod(seconds, 60)
        length = f"{minutes}:{seconds:02}"

        album_data["tracks"].append({"name": song["name"], "length": length})

    data["albums"].append(album_data)

with open(f"./src/static/artists/{name}.json", "w") as f:
    dump(data, f)
