import requests
from bs4 import BeautifulSoup

URL = 'https://www.billboard.com/charts/hot-100/'

users_date = input("Which year would you like to travel to? Type the date in this format YYYY-MM-DD: ")
website_info = requests.get(url=URL+users_date+'/')

soup = BeautifulSoup(website_info.text, 'html.parser')
song_name_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_name_spans]

print(song_names)