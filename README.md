<!--<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green" /><img src="https://img.shields.io/badge/Spotify-1ED760?&style=for-the-badge&logo=spotify&logoColor=white" />-->

# CTL

CTL is a Console application written in Python that allows users to play complete the lyrics. This project is unfinished.

## Build and Run

To build and run the program, change to the src/Console directory and execute the following command:



```bash
python3 main.py
```

After the program is running, you can start a game by typing the following:

```bash
!play CTL spotify-playlist-link
```

## API Keys

This project requires the use of the [Spotify API](https://developer.spotify.com/documentation/web-api/tutorials/getting-started), and the [Genius API](https://docs.genius.com/).

Your client id's and secret id's should be placed in a text file named "secrets" in the Console directory and formatted as follows. Currently the Genius Token also needs to be manually placed.

```bash
spotify-client-id-here
spotify-secret-id-here
genius-client-id-here
genius-secret-id-here
genius-token
```

## Training Data

Training data for the LLM should be placed in a .csv file with values as the header of lyrics.

## Progress

Check out the [TODO](https://github.com/kz3640/CTL/blob/main/TODO.md).


## Issues
