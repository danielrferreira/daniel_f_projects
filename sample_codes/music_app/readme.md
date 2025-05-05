# Music Explorer

**Music Explorer** is an interactive Streamlit app that lets you explore songs based on audio features such as danceability, energy, and acousticness. You can visualize how songs deviate from the "average vibe", discover standout or unusual tracks, and even get personalized song suggestions based on your mood.

## Features

- **Visual Analysis** of a song's features against the overall distribution
- **Top Obvious Songs**: Find songs that are most similar to the average
- **Top Weird Songs**: Discover songs that stand out the most
- **Pick Music by Vibe**: Use sliders to define your mood and get recommendations

## Data Requirements

The app expects a CSV file with the following columns:

- Audio features:
  - `danceability`
  - `energy`
  - `loudness`
  - `speechiness`
  - `acousticness`
  - `liveness`
  - `valence`
- Metadata:
  - `song`
  - `band_singer`
  - `uri` (Spotify track URI)
  - `songurl` (unique song identifier)
  - `lyrics` (optional)

Place this file as `data_sources/input_df.csv`.

##  How to Run

A deployed version is coming in a different repo, but if you want to run it locally you can:

1. Download the py file, requirements and data folder.

2. Install dependencies:
  ```bash
  pip install -r requirements.txt

3. Launch the app:
  ```bash
  streamlit run music_distances_app.py
