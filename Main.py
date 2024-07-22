import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

BILLBOARD_URL = 'https://www.billboard.com/charts/hot-100/'
SPOTIFY_CLIENT_ID = '596bf299646e45d6907c4ec604f08e3d'
SPOTIFY_SECRET = '5534d23bbce047dfa90e4301a129778e'

users_date = input("Which year would you like to travel to? Type the date in this format YYYY-MM-DD: ")
website_info = requests.get(url=BILLBOARD_URL + users_date + '/')

soup = BeautifulSoup(website_info.text, 'html.parser')
song_name_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_name_spans]

#print(song_names)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               scope="playlist-modify-private",
                                               client_secret=SPOTIFY_SECRET,
                                               redirect_uri="https://example.com/callback",
                                               ))

user_id = sp.current_user()["id"]
print(user_id)

year = users_date.split("-")[0]
song_uris = []
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user_id,f"100 songs of year {year}", public=False, collaborative=False, description=f"Top Billboard 100 songs of year {year}")
print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
