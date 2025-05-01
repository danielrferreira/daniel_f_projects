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

1. Install dependencies:
   ```bash
   pip install -r requirements.txt

2. Launch the app:
  ```bash
  streamlit run app.py
