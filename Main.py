import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from Keys import CLIENT_ID, SPOTIFY_SECRET

#define constants
BILLBOARD_URL = 'https://www.billboard.com/charts/hot-100/'

#query the user for the date and request the website information
users_date = input("Which year would you like to travel to? Type the date in this format YYYY-MM-DD: ")
website_info = requests.get(url=BILLBOARD_URL + users_date + '/')

#scrape the site with beautiful soup
soup = BeautifulSoup(website_info.text, 'html.parser')
song_name_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_name_spans]

#login to spotify with spotipy
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               scope="playlist-modify-private",
                                               client_secret=SPOTIFY_SECRET,
                                               redirect_uri="https://example.com/callback",
                                               ))
#read and save the user id from the authentication
user_id = sp.current_user()["id"]

#search the songs by uri
year = users_date.split("-")[0]
song_uris = []
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#cretae the new Playlist with the URIs found
playlist = sp.user_playlist_create(user_id,f"100 songs of year {year}", public=False, collaborative=False, description=f"Top Billboard 100 songs of year {year}")
print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
