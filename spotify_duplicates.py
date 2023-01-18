#!/usr/bin/env python3

import requests

#Insert your API key here
api_key = "BQBurKQfvpH3jjw2OLwH6X3kRjVi7zhJhzu3gyiyx8am8J6sr2VnhjTtcey3KSqfsR1DEjbJEHyQSfxztjTRG5b5My_7WH2KfzWus5-3UbtROe4w1qZNjglHvnwYTQPevChjNA21-YyHqMDoLEGe1VUWS6f9xcY9CeuRMlUmSk18rBcCyvMW8w"

#Insert the Spotify playlist ID here
playlist_id = "6ar2svv2tpgkdvTTgWYnzF"

#Endpoint for getting the tracks in a playlist
endpoint = f"https://api.spotify.com/v1/playlists/6ar2svv2tpgkdvTTgWYnzF/tracks"

#Header for authentication
headers = {
    "Authorization": f"Bearer {api_key}"
}

# Set to store seen tracks
seen_tracks = set()
# Set to store duplicate tracks
duplicate_tracks = set()
# Keep track of the offset for pagination
offset = 0
# Dictionary to store track information
track_info = {}

while True:
    endpoint = f"https://api.spotify.com/v1/playlists/6ar2svv2tpgkdvTTgWYnzF/tracks?offset={offset}"
    try:
        #Get the tracks in the playlist
        response = requests.get(endpoint, headers=headers)
        #Check the status code
        if response.status_code != 200:
            print("Error: ", response.status_code)
            print("response content: ", response.content)
            break
        else:
            #Parse the response
            data = response.json()
            #Iterate through the tracks
            for item in data["items"]:
                track_uri = item["track"]["uri"]
                track_name = item["track"]["name"]
                artist_name = item["track"]["artists"][0]["name"]
                # Store the track information in the dictionary
                track_info[track_uri] = {"name": track_name, "artist": artist_name}
                #Check if the track has already been seen
                if track_uri in seen_tracks:
                    duplicate_tracks.add(track_uri)
                else:
                    seen_tracks.add(track_uri)
            
            # Increase the offset for pagination        
            offset += len(data["items"])
            # If there are no more items to retrieve, break the loop
            if len(data["items"]) == 0:
                break
    except requests.exceptions.RequestException as e:
        print("Error: ", e)

if len(duplicate_tracks) == 0:
    print("No duplicates found.")
else:
    print("Duplicates found:")
    for duplicate in duplicate_tracks:
        print("Track URI:", duplicate)
        print("Track Name:", track_info[duplicate]["name"])
        print("Artist Name:", track_info[duplicate]["artist"])
        print("\n")