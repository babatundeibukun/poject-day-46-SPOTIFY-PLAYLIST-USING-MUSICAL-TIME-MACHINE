from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

date = input("What year you would like to travel to in YYYY-MM-DD format? ")
URL = f"https://www.billboard.com/charts/hot-100/{date}/"
Client_ID="CREATE YOUR CLINET ID"
Client_Secret = "CREATE YOURS"

response = requests.get(URL)
billboard_web_page = response.text
soup = BeautifulSoup(billboard_web_page, "html.parser")
music_list =[music.getText().strip() for music in soup.find_all(name="h3",id="title-of-a-story",class_="a-no-trucate")]
#print(music_list)


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=Client_ID,
        client_secret=Client_Secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]


song_names = music_list
SONG_URIS = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    #print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        SONG_URIS.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

song_uris=SONG_URIS
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)