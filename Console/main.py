import base64
import requests
import datetime
from states import States
from gamemodes import Gamemodes
from bs4 import BeautifulSoup

from lyricsgenius import Genius

# spotify api stuff
spotify_auth_url = 'https://accounts.spotify.com/api/token'
spotify_client_id = None
spotify_client_secret = None
spotify_token = None

# genius api stuff
genius_auth_url = 'https://api.genius.com/oauth/authorize'
genius_client_id = None
genius_client_secret = None
genius_token = None
genius = None

# might be useful? not sure
genTime = None
# spotify playlist as a json
playlist_json = None


# Load secrets
def load_secrets():
    global spotify_client_id, spotify_client_secret, genius_client_id, genius_client_secret, genius_token, genius
    with open('secrets') as f:
        spotify_client_id = f.readline().strip()
        spotify_client_secret = f.readline().strip()
        genius_client_id = f.readline().strip()
        genius_client_secret = f.readline().strip()
        genius_token = f.readline().strip()
    genius = Genius(access_token=genius_token, remove_section_headers=True)


# generate a spotify token and save it under spotify_token
def generate_spotify_token():
    auth_headers = {
        'Authorization': 'Basic ' + base64.b64encode((spotify_client_id + ':' + spotify_client_secret).encode('utf-8')).decode('utf-8')
    }
    auth_data = {
        'grant_type': 'client_credentials'
    }
    auth_response = requests.post(spotify_auth_url, headers=auth_headers, data=auth_data)

    if auth_response.status_code == 200:
        global spotify_token, genTime
        spotify_token = auth_response.json().get('access_token')
        genTime = datetime.datetime.now()
        update_headers()
    else:
        print('Error:', auth_response.status_code, auth_response.text)


# generate a genius token and save it under genius_token
def generate_genius_token():
    return


def update_headers():
    global playlist_headers
    playlist_headers = {
        'Authorization': 'Bearer ' + spotify_token
    }


def fetch_id(playlist_id):
    # fetches json data from spotify api
    url = "https://api.spotify.com/v1/playlists/" + str(playlist_id) + "/tracks?offset=0&limit=100"
    response = requests.get(url, headers=playlist_headers)

    if response.status_code == 200:
        return response.json()
    else:
        print('Error:', response.status_code, response.text)
        return None

def getLyrics(idx, name, artist):
    parsed_name = name.replace(" ", "").lower()
    parsed_artist = artist.replace(" ", "").lower()
    song = genius.search_song(title=parsed_name, artist=parsed_artist)
    if song != None:
        playlist_json['items'][idx]['track']['validlyrics'] = True
        playlist_json['items'][idx]['track']['lyrics'] = song.lyrics
    else:
        playlist_json['items'][idx]['track']['validlyrics'] = False
        playlist_json['items'][idx]['track']['lyrics'] = ""




def play(mode, url):
    last_slash_index = url.rfind("/")
    playlist_id = url[last_slash_index + 1: url.find("?", last_slash_index)]

    playlist_data = fetch_id(playlist_id)

    if playlist_data:
        filtered_data = {
            "items": [
                {
                    "track": {
                        "artists": item['track']['artists'],
                        "explicit": item['track']['explicit'],
                        "external_ids": item['track']['external_ids'],
                        "id": item['track']['id'],
                        "name": item['track']['name']
                    }
                }
                for item in playlist_data['items']
            ],
            "limit": playlist_data['limit'],
            "next": playlist_data['next'],
            "offset": playlist_data['offset'],
            "previous": playlist_data['previous'],
            "next": playlist_data['next']
        }

        global playlist_json
        playlist_json = filtered_data

        songs_array = playlist_json['items']
        for i in range(len(songs_array)):
            print(songs_array[i]['track']['name'] + " - " + songs_array[i]['track']['artists'][0]['name'])
            getLyrics(i, songs_array[i]['track']['name'], songs_array[i]['track']['artists'][0]['name'])
            print(playlist_json['items'][i]['track']['lyrics'])

        mode = mode.lower()
        return States.FREEINPUT  # TODO ACTUALLY IMPLEMENT THIS, THIS IS PLACEHOLDER
        if mode == "ctl":
            return Gamemodes.CTL
    else:
        # Handle the case where fetching playlist data fails
        return States.FREEINPUT


def handle_free_input(user_input):
    user_input_lower = user_input.lower()
    if user_input_lower == "!help":
        # Handle help command logic
        print("!help - Shows all commands.")
        print("!quit - Exits the program.")
        print("!settings - Shows settings")
        return States.FREEINPUT

    elif user_input_lower == "!quit":
        # Handle quit command logic
        print("Quitting the program...")
        return States.QUIT

    elif user_input_lower == "!settings":
        # Handle settings command logic
        print("Opening settings...")
        return States.SETTINGSMENU

    elif user_input_lower.startswith("!play"):
        _, mode, url = user_input.split(maxsplit=2)
        play_response = play(mode, url)
        return play_response

    else:
        print("Invalid command. Type !help for assistance.")

    return


def handle_settings_menu():
    # Add logic for handling settings menu
    return


def main():
    load_secrets()
    generate_spotify_token()
    current_state = States.FREEINPUT

    while current_state != States.QUIT:
        if current_state == States.FREEINPUT:
            current_state = handle_free_input(input("Enter a command."))


if __name__ == "__main__":
    main()
