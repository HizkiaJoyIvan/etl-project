from requests import get
import pandas as pd

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def extract(url, token):
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    
    try:
        result.raise_for_status()  
        data = result.json()

        names = []
        names = []
        albums = []
        artists = []
        popularities = []
        durations = []
        tracks = data.get("tracks", {}).get("items", [])
        for track in tracks:
            names.append(track["track"]["name"])
            albums.append(track["track"]["album"]["name"])
            artists.append(track["track"]["artists"][0]["name"])
            popularities.append(track["track"]["popularity"])
            durations.append(track["track"]["duration_ms"])
        
        track_dict = {
            "name": names,
            "album": albums,
            "artist": artists,
            "popularity": popularities,
            "duration": durations
        }

        track_df = pd.DataFrame(track_dict, columns=["name", "album", "artist", "popularity", "duration"])

        return track_df
    except Exception as e:
        print(f"Error: {e}")