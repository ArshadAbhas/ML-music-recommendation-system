import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load the data and model
@st.cache_data
def load_data():
    df = pd.read_csv("sample_music.csv")  # Replace with your dataset file name
    df_scaled = np.load("df_scaled.npy")   # Replace with your scaled features file
    return df, df_scaled

@st.cache_resource
def load_model():
    knn = joblib.load("knn_model.pkl")  
    return knn

def recommend_songs_multiple(song_names, df, df_scaled, knn, num_recommendations=10):
    # Check if all songs are in the dataset
    missing_songs = [song for song in song_names if song not in df['name'].values]
    if missing_songs:
        return f"These songs are not found in the dataset: {', '.join(missing_songs)}"

    # Get indices of the input songs
    song_indices = [df[df['name'] == song].index[0] for song in song_names]

    # Calculate the average features of the input songs
    average_features = np.mean(df_scaled[song_indices], axis=0).reshape(1, -1)

    # Find similar songs using KNN
    distances, indices = knn.kneighbors(average_features, n_neighbors=(num_recommendations + len(song_names)))

    # Get recommended songs, excluding the input songs themselves
    recommended_indices = [idx for idx in indices.flatten() if idx not in song_indices][:num_recommendations]
    recommended_songs = df.iloc[recommended_indices]

    return recommended_songs[['artist', 'name']]

# Streamlit app
st.title("Music Recommendation System")
st.write("Find songs similar to your favorites!")

# Load resources
df, df_scaled = load_data()
knn = load_model()

# User input for song names
song_names = st.text_input("Enter song names (comma-separated):")

if song_names:
    # Split and trim input song names
    song_list = [song.strip() for song in song_names.split(',')]

    # Recommend songs
    recommendations = recommend_songs_multiple(song_list, df, df_scaled, knn)

    if isinstance(recommendations, str):
        st.error(recommendations)
    else:
        st.write("Recommended Playlist:")
        st.dataframe(recommendations)

