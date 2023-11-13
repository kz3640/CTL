import base64
import requests

auth_url = 'https://accounts.spotify.com/api/token'
client_id = ''
client_secret = ''
auth_headers = {
    'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode('utf-8')).decode('utf-8')
}
auth_data = {
    'grant_type': 'client_credentials'
}

currToken = 'BQC0WNDIh2JQuJZsNAjijyZHMlmO_V9pB_CwbBgY4fFKuuESpmO_xdjVvlkeCXNV9DsjFI7NBUdUYM7W_3x8PDqBx_1j2ZvYo9HfYDvqnIFokMz8XBA'
playlist_headers = {
    'Authorization': 'Bearer ' + currToken
}
def main():
    print("startup")
    #
    #auth_response = requests.post(auth_url, headers=auth_headers, data=auth_data)
    #if auth_response.status_code == 200:
    #    token = auth_response.json().get('access_token')
    #else:
    #    print('Error:', auth_response.status_code, auth_response.text)

    r = requests.get("https://api.spotify.com/v1/playlists/31dS7OuVUj0n8VG1JU8jTU", headers=playlist_headers)
    print(r.status_code)

    #testLyrics = open('Country Roads.txt')
    #for x in testLyrics.readlines():
    #   print(x, end="")

    #r=requests.get("https://api.spotify.com/v1/playlists/31dS7OuVUj0n8VG1JU8jTU/tracks?offset=0&limit=100", headers=playlist_headers)
    #print(r.status_code)

if __name__ == "__main__":
    main()