import bs4
import requests
import spotipy
import spotipy.oauth2
import os
import re

client_id = os.environ.get('SPOTIFY_CLIENT_ID')
client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
redirect_uri = os.environ.get("URI")


def check_input(string):
    format_ = r"\d{4}-\d{2}-\d{2}"
    if not re.fullmatch(format_, string):
        print("Please input with right format")
        return False
    else:
        return True


def get_top_100():
    while True:
        date = input("Which date (YYYY-MM-DD): ")
        if check_input(date):
            break
    url = f"https://www.billboard.com/charts/hot-100/{date}"
    response = requests.get(url=url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    list_song = soup.select(selector=".o-chart-results-list-row-container li h3", class_="c-title")
    list_titles = [song.getText().strip() for song in list_song]
    return list_titles


def authenticate_spotify():
    username = "31ajvkpkkyoa6vov5noqtgwcd63m"
    sp = spotipy.Spotify(
        auth_manager=spotipy.oauth2.SpotifyOAuth(
            scope="playlist-modify-private",
            redirect_uri=redirect_uri,
            client_id=client_id,
            client_secret=client_secret,
            show_dialog=True,
            cache_path="token.txt",
            username=username,
        )
    )
    return sp


def create_and_add_song(sp, list_title):
    user_id = sp.current_user()["id"]
    list_song_uri = []
    for song_name in list_title:
        try:
            song = sp.search(q=f"track:{song_name}", type="track", limit=1)
            song_uri = song['tracks']['items'][0]['uri']
            list_song_uri.append(song_uri)
        except IndexError:
            continue

    playlist_name = "Test Playlist"
    description = "Just chill"
    playlist = sp.user_playlist_create(user=user_id,
                                       name=playlist_name,
                                       public=False,
                                       description=description)
    sp.playlist_add_items(playlist_id=playlist["id"], items=list_song_uri)


list_title = get_top_100()
sp_object = authenticate_spotify()
create_and_add_song(sp_object, list_title)
