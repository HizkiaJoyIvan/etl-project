from dotenv import load_dotenv
import os
from requests import get, post
import base64

load_dotenv()

client_secret = os.getenv("CLIENT_SECRET")
client_id = os.getenv("CLIENT_ID")

print(client_secret, client_id)

def get_token(): 
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_base64), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic" + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = get(url, headers=headers)
    json_res = json.loads(result.content)
    token = json_res["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

token = get_token()