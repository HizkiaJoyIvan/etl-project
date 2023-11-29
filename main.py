from pipeline.extractspotify import extract_from_spotify
from pipeline.extracttrends import extract_from_google_trends
from pipeline.transform import transform_trends, transform_spotify, transform_merge



if __name__ == "__main__":
    # extract_from_spotify("https://api.spotify.com/v1/playlists/37i9dQZEVXbKpV6RVDTWcZ")
    # extract_from_google_trends()
    s = transform_spotify("extracted_spotify_data.csv")
    t = transform_trends("extracted_trends_data.csv")
    data = transform_merge(s, t)
    print(data)

