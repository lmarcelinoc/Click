#music_agent.py

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Set up Spotify client
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
))

def play_music(search_query):
    results = spotify.search(q=search_query, type='track', limit=1)
    track = results['tracks']['items'][0] if results['tracks']['items'] else None
    if track:
        print(f"Playing {track['name']} by {track['artists'][0]['name']}")
        # In a real application, you would send a command to play this track
    else:
        print("No tracks found.")

if __name__ == "__main__":
    # Example usage
    play_music("Let it be")

