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
playlist = None

#load secrets
with open('secrets') as f:
    client_id = f.readline().strip()
    client_secret = f.readline().strip()
auth_headers = {
    'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode('utf-8')).decode('utf-8')
}
auth_data = {
    'grant_type': 'client_credentials'
}
playlist_headers = {
    'Authorization': 'Bearer ' + ""
}

def genToken():
    auth_response = requests.post(auth_url, headers=auth_headers, data=auth_data)
    if auth_response.status_code == 200:
        global token
        global genTime
        token = auth_response.json().get('access_token')
        genTime = datetime.datetime.now()
        updateHeaders()
    else:
        print('Error:', auth_response.status_code, auth_response.text)

def updateHeaders():
    global playlist_headers
    playlist_headers = {
        'Authorization': 'Bearer ' + token
    }

def fetchID(playlist_id):
    url = "https://api.spotify.com/v1/playlists/" + playlist_id + "/tracks?offset=0&limit=100"
    r = requests.get(url, headers=playlist_headers)
    return r
def play(mode, url):
    last_slash_index = url.rfind("/")
    playlist_id = url[last_slash_index + 1 : url.find("?", last_slash_index)]
    global playlist
    playlist = fetchID(playlist_id)
    print("ERROR CODE " + str(playlist.status_code))
    mode = mode.lower()
    return States.FREEINPUT#TODO ACTUALLY IMPLEMENT THIS, THIS IS PLACEHOLDER
    if mode == "CTL":
        return Gamemodes.CTL

def handleFreeInput(user_input):
    user_input_lower = user_input.lower()
    if user_input_lower == "!help":
        print("!help - Shows all commands.")
        print("!quit - Exits the program.")
        print("!settings - Shows settings")
        return States.FREEINPUT
        # Handle help command logic

    elif user_input_lower == "!quit":
        print("Quitting the program...")
        return States.QUIT
        # Handle quit command logic

    elif user_input_lower == "!settings":
        print("Opening settings...")
        return States.SETTINGSMENU
        # Handle settings command logic

    elif user_input_lower.startswith("!play"):
        # Split the input into command and arguments
        _, mode, url = user_input.split(maxsplit=2)

        # Handle the play command with mode and URL
        play_response = play(mode, url)
        return play_response

    else:
        print("Invalid command. Type !help for assistance.")

    return

def handleSettingsMenu():
    return
def main():
    genToken()
    current_state = States.FREEINPUT
    playlist_url = ""
    while(current_state != States.QUIT):
        if(current_state == States.FREEINPUT):
            current_state = handleFreeInput(input("Enter a command."))




if __name__ == "__main__":
    main()