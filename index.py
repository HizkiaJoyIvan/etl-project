from dotenv import load_dotenv
import os
from requests import get, post
import base64
import json

load_dotenv()

client_secret = os.getenv("CLIENT_SECRET")
client_id = os.getenv("CLIENT_ID")

print(client_secret, client_id)

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

def basic_extraction(url, token, artist_name):
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

token = get_token()

if token:
    basic_extraction("https://api.spotify.com/v1/browse/categories/toplists/playlists", token, "Hindia")
else:
    print("Unable to obtain token.")
