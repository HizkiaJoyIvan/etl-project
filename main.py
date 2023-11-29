from src import spotify
from src import trends

spotify.extract_spotify_data()
spotify.transform_spotify_data()
trends.extract_trends_data()
trends.transform_trends_data()