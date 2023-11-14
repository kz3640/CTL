import base64
import requests
import datetime
from states import States
from gamemodes import Gamemodes

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
    #fetches json data from spotify api
    url = "https://api.spotify.com/v1/playlists/"+str(playlist_id)+"/tracks?offset=0&limit=100"
    response = requests.get(url, headers=playlist_headers)

    if response.status_code == 200:
        return response.json()
    else:
        print('Error:', response.status_code, response.text)
        return None


def play(mode, url):
    last_slash_index = url.rfind("/")
    playlist_id = url[last_slash_index + 1: url.find("?", last_slash_index)]

    playlist_data = fetch_id(playlist_id)

    if playlist_data:
        global playlist_json
        playlist_json = playlist_data

        songs_array = playlist_json['items']
        for x in songs_array:
            print(x['track']['name'] +" - "+ x['track']['artists'][0]['name'])
        #TODO EITHER CONNECT MUSIXMATCH (PAID API) OR WEBSCRAPE FROM A SITE, PROBABLY SCRAPE
        #THINKING ABOUT SCRAPING FROM AZLYRICS.COM

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
