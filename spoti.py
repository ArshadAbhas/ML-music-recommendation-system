import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time
import numpy as np

# Spotify credentials
client_id = "0054a24f2fc643c69d56d020dd5f70be"
client_secret = "98b4a4b772ad4eca934a92ca60c246a0"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# List of artist names
artists = ["Micheal Jackson", "Kendrick Lamar", "Hip Hop Tamizha", "Anirudh Ravichander", 
           "Yuvan Shankar Raja", "Sam C.S.", "Vijay Antony", "Bruno Mars", "Alan Walker", "Marshmello","A R Rahman"]

# Data structure to store results
spotify_albums = {
    'artist': [], 'album': [], 'track_number': [], 'id': [], 'name': [], 'uri': [], 'popularity': [],
    'acousticness': [], 'danceability': [], 'energy': [], 'instrumentalness': [], 
    'liveness': [], 'loudness': [], 'speechiness': [], 'tempo': [], 'valence': []
}

def album_songs(uri, album_name, artist_name):
    try:
        tracks = sp.album_tracks(uri)
        for track in tracks['items']:
            track_info = sp.track(track['id'])  # Fetch track details for popularity
            spotify_albums['artist'].append(artist_name)
            spotify_albums['album'].append(album_name)
            spotify_albums['track_number'].append(track['track_number'])
            spotify_albums['id'].append(track['id'])
            spotify_albums['name'].append(track['name'])
            spotify_albums['uri'].append(track['uri'])
            spotify_albums['popularity'].append(track_info['popularity'])
    except Exception as e:
        print(f"Error fetching tracks for album {album_name}: {e}")

def fetch_audio_features(uris):
    try:
        features = sp.audio_features(uris)
        for feature in features:
            if feature:  # Ensure feature data exists
                spotify_albums['acousticness'].append(feature.get('acousticness'))
                spotify_albums['danceability'].append(feature.get('danceability'))
                spotify_albums['energy'].append(feature.get('energy'))
                spotify_albums['instrumentalness'].append(feature.get('instrumentalness'))
                spotify_albums['liveness'].append(feature.get('liveness'))
                spotify_albums['loudness'].append(feature.get('loudness'))
                spotify_albums['speechiness'].append(feature.get('speechiness'))
                spotify_albums['tempo'].append(feature.get('tempo'))
                spotify_albums['valence'].append(feature.get('valence'))
            else:
                # Append NaN if features are not available
                spotify_albums['acousticness'].append(None)
                spotify_albums['danceability'].append(None)
                spotify_albums['energy'].append(None)
                spotify_albums['instrumentalness'].append(None)
                spotify_albums['liveness'].append(None)
                spotify_albums['loudness'].append(None)
                spotify_albums['speechiness'].append(None)
                spotify_albums['tempo'].append(None)
                spotify_albums['valence'].append(None)
    except Exception as e:
        print(f"Error fetching audio features: {e}")

# Loop through each artist and fetch data
for artist in artists:
    print(f"Fetching data for {artist}...")
    try:
        result = sp.search(q=artist, type='artist', limit=1)
        if not result['artists']['items']:
            print(f"No results found for {artist}")
            continue

        artist_uri = result['artists']['items'][0]['uri']
        artist_albums = sp.artist_albums(artist_uri, album_type='album')

        for album in artist_albums['items']:
            album_name = album['name']
            album_uri = album['uri']
            print(f"Fetching tracks for album: {album_name}")
            album_songs(album_uri, album_name, artist)
    except Exception as e:
        print(f"Error fetching data for {artist}: {e}")

# Fetch audio features in batches of 100
unique_uris = list(set(spotify_albums['uri']))
batch_size = 100
for i in range(0, len(unique_uris), batch_size):
    print(f"Fetching audio features for batch {i // batch_size + 1}")
    fetch_audio_features(unique_uris[i:i + batch_size])

# Convert the data into a DataFrame
dataframe = pd.DataFrame(spotify_albums)
print(f"Total tracks fetched: {len(dataframe)}")

# Remove duplicates and save to CSV
final_df = dataframe.sort_values('popularity', ascending=False).drop_duplicates('name').reset_index(drop=True)
print(f"Final unique tracks: {len(final_df)}")
final_df.to_csv("sample_music1.csv", index=False)
print("Data saved to sample_music.csv")
