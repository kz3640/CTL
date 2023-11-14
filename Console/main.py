import base64
import requests
import datetime
from states import States
from gamemodes import Gamemodes
from bs4 import BeautifulSoup

auth_url = 'https://accounts.spotify.com/api/token'
client_id = None
client_secret = None
token = None
genTime = None
playlist_json = None


# Load secrets
def load_secrets():
    global client_id, client_secret
    with open('secrets') as f:
        client_id = f.readline().strip()
        client_secret = f.readline().strip()


def generate_token():
    auth_headers = {
        'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode('utf-8')).decode('utf-8')
    }
    auth_data = {
        'grant_type': 'client_credentials'
    }
    auth_response = requests.post(auth_url, headers=auth_headers, data=auth_data)

    if auth_response.status_code == 200:
        global token, genTime
        token = auth_response.json().get('access_token')
        genTime = datetime.datetime.now()
        update_headers()
    else:
        print('Error:', auth_response.status_code, auth_response.text)


def update_headers():
    global playlist_headers
    playlist_headers = {
        'Authorization': 'Bearer ' + token
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


def validLyrics(page):
    soup = BeautifulSoup(page.content, "html.parser")
    if str(soup.title) == "<title>AZLyrics - Song Lyrics from A to Z</title>":
        return False
    return True


def cleanLyrics(dirty_lyrics):
    dirty_lyrics = dirty_lyrics.replace("<br>", "")
    dirty_lyrics = dirty_lyrics.replace("\\r", "")
    dirty_lyrics = dirty_lyrics.replace("\\'", "'")
    dirty_lyrics = dirty_lyrics.replace("\\n", "\n")
    dirty_lyrics = dirty_lyrics.replace("</div>", "")
    return dirty_lyrics


def parseLyrics(page):
    header = "<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->"
    footer = "<!-- MxM banner -->"
    content = str(page.content)
    start_index = content.find(header) + len(header)
    end_index = content.find(footer, start_index)
    dirty_lyrics = content[start_index:end_index]
    clean_lyrics = cleanLyrics(dirty_lyrics)
    return clean_lyrics


def scrape(idx, name, artist):
    parsedname = name.replace(" ", "").lower()
    parsedartist = artist.replace(" ", "").lower()
    url = "https://www.azlyrics.com/lyrics/" + parsedartist + "/" + parsedname + ".html"
    page = requests.get(url)
    if (validLyrics(page)):
        playlist_json['items'][idx]['track']['validlyrics'] = True
        playlist_json['items'][idx]['track']['lyrics'] = parseLyrics(page)
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
            scrape(i, songs_array[i]['track']['name'], songs_array[i]['track']['artists'][0]['name'])

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
    generate_token()
    current_state = States.FREEINPUT

    while current_state != States.QUIT:
        if current_state == States.FREEINPUT:
            current_state = handle_free_input(input("Enter a command."))


if __name__ == "__main__":
    main()
