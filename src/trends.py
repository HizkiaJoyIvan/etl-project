from dotenv import load_dotenv
import os
import csv
import requests
import json
import pandas as pd

load_dotenv()
API_KEY = os.getenv("TRENDS_API_KEY")

def fetch_from_api(query):
    url = "https://serpapi.com/search"
    params = {
        'engine': 'google_trends',
        'q': query,
        'data_type': 'TIMESERIES',
        'api_key': API_KEY
    }

    response = requests.get(url, params=params)
    return response

def clean_songname(string):
    from re import sub
    pattern = r'\([^)]*\)'
    result_string = sub(pattern, '', string)

    return result_string.split('-')[0].lower().strip()

def read_spotify_file(filename):
    root = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(root, filename)
 
    songnames = []

    with open(file_path, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        
        for row in csv_reader:
            combined_string = f"{row['name']}"
            songnames.append(combined_string)
   
    songnames = [clean_songname(songname) for songname in songnames]
    
    return songnames

def write_to_json(data, filename):
    root = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(root, filename)
    with open(file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

def read_json_file(filename):
    root = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(root, filename)
    
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

def write_to_csv(data, filename):
    root = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(root, filename)

    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = data.columns  
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(data.to_dict('records'))  


def extract_trends_data():
    songnames = read_spotify_file("../data/processed/spotify.csv")

    # group the song for 5 each query
    queries = [",".join(f"{songname} lirik" for songname in songnames[i:i+5]) for i in range(0, len(songnames), 5)]
    for index, query in enumerate(queries):
        data = fetch_from_api(query).json()
        write_to_json(data, f"../data/raw/trends{index}.json")
 
def transform_json_trends(data):
    df = pd.json_normalize(data, "values", ["timestamp"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
    df["timestamp"] = df["timestamp"].dt.strftime("%Y/%m/%d")
 
    df = df.pivot(index="query", columns="timestamp", values="extracted_value")
    df = df.reset_index().rename_axis(columns=None)
 
    return df
 
def transform_trends_data():
    df = pd.DataFrame()
 
    for i in range(10):
        try:
            data = read_json_file(f"../data/raw/trends{i}.json")['interest_over_time']['timeline_data']
            df = pd.concat([df, transform_json_trends(data)], ignore_index=True)
        except Exception as e:
            print(f"Error: {e}")
            continue
  
    write_to_csv(df, "../data/processed/trends.csv")
 
        