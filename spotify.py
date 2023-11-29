from dotenv import load_dotenv
import os
from requests import get, post
import base64
import json
import csv
import pandas as pd

load_dotenv()

client_secret = os.getenv("CLIENT_SECRET")
client_id = os.getenv("CLIENT_ID")

def get_token(): 
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    
    try:
        result.raise_for_status()  
        json_res = result.json()
        token = json_res.get("access_token")
        if token:
            return token
        else:
            print("Error: Access token not found in response.")
    except Exception as e:
        print(f"Error: {e}")
        print(result.text)

    return None

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

def search_for_artists(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    
    try:
        result.raise_for_status()  
        json_res = result.json()
        print(json_res)
    except Exception as e:
        print(f"Error: {e}")
        print(result.text)

def clean_data(data):
    bins = [0, 40, 70, 100]
    labels = ['low', 'medium', 'high']

    data['duration'] = data['duration'] / 60000
    data['popularity_category'] = pd.cut(data['popularity'], bins=bins, labels=labels)

    return data

def write_to_csv(data, filename):
    root = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(root, filename)

    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = data.columns  
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(data.to_dict('records'))  

def write_to_json(data, filename):
    root = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(root, filename)
    with open(file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)
        
token = get_token()

if token:
    data = extract("https://api.spotify.com/v1/playlists/37i9dQZEVXbKpV6RVDTWcZ", token)
    transformed_data = clean_data(data)
    write_to_csv(transformed_data, "data1.csv")
else:
    print("Unable to obtain token.")
