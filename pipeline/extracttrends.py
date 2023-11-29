# get top 50 spotify data for search query
import csv

csv_file_path = 'extracted_spotify_data.csv'

songnames = []

with open(csv_file_path, 'r') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    
    for row in csv_reader:
        combined_string = f"{row['name']}"
        songnames.append(combined_string)

# clean the song names
def clean_songname(string):
    from re import sub
    pattern = r'\([^)]*\)'
    result_string = sub(pattern, '', string)

    return result_string.split('-')[0].lower().strip()

songnames = [clean_songname(songname) for songname in songnames]

# group the song for 5 each query
queries = [",".join(f"{songname} lirik" for songname in songnames[i:i+5]) for i in range(0, len(songnames), 5)]


def fetch_from_api(query):
    import requests

    url = "https://serpapi.com/search"
    params = {
        'engine': 'google_trends',
        'q': query,
        'data_type': 'TIMESERIES',
        'api_key': 'ec37520e9a2d261158a0820a2504804a1ddedd38e18e2e119ce0e86baebc791f'
    }

    response = requests.get(url, params=params)
    return response

# initialize new csv data
import csv

timeline_data = fetch_from_api(queries[0]).json()['interest_over_time']['timeline_data']
initial_csv_data = [
    ["query"] + [timeline["date"] for timeline in timeline_data] # header
] + [
    [timeline_data[0]["values"][i]["query"]] + [timeline["values"][i]["extracted_value"] for timeline in timeline_data] for i in range(len(timeline_data[0]["values"]))
]

def extract_from_google_trends():
    with open("extracted_trends_data.csv", 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(initial_csv_data)
        for i, query in enumerate(queries[1:]):
            print(i, query)
        response = fetch_from_api(query).json()
        timeline_data = response['interest_over_time']['timeline_data']
        csv_writer.writerows([[timeline_data[0]["values"][i]["query"]] + [timeline["values"][i]["extracted_value"] for timeline in timeline_data] for i in range(len(timeline_data[0]["values"]))])