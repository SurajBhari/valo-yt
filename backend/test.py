from chat_downloader.sites import YouTubeChatDownloader
from chat_downloader import ChatDownloader
import requests
from datetime import datetime, timedelta, timezone
import valo_api as vapi
import urllib

import json

with open("config.json") as f:  
    config = json.load(f)

api_key = config['api_key']

stream_id = "XUa_l4ffgPA"
name = "Harsh"
tag = "khel"
region = "ap"
platform = "pc"   


# get stream start time 

vid = YouTubeChatDownloader().get_video_data(video_id=stream_id)
with open("vid.json", "w+") as f:
    json.dump(vid, f, indent=4)
start_time = vid['start_time']  / 1000000 # start time in seconds
end_time = vid['end_time'] / 1000000 # end time in seconds

print(f"Stream started at {start_time} and ended at {end_time}")

url = f"https://api.henrikdev.xyz/valorant/v1/lifetime/matches/{region}/{name}/{tag}"
encoded_url = urllib.parse.quote(url, safe=':/')
r = requests.get(url=encoded_url, headers={'Authorization': api_key}, params={"mode": "competitive"})
if r.status_code != 200:
    print("Error")
    print(r.text)
    exit()

data = r.json()

# save this to json file
matches_played = []
match_ids = []
for match in data['data']:
    print("NEW MATCH ALERT")
    match_start_at = match['meta']['started_at']
    match_start_at = datetime.strptime(match_start_at, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp() + 19800 # this is weird. but this work. so i am gonna leave it here
    if match_start_at > end_time:
        continue
    if match_start_at < start_time:
        break
    print(f"Match started at {match_start_at}")
    puuid = match['stats']['puuid']
    match['meta']['unix_time'] = match_start_at
    matches_played.append(match)
    match_id = match['meta']['id']
    match_ids.append(match_id)
    

kill_events = []
for mid in match_ids:
    url = f"https://api.henrikdev.xyz/valorant/v2/match/{mid}"
    r = requests.get(url=url, headers={'Authorization': api_key})
    if r.status_code != 200:
        print("Error")
        print(r.text)
        exit()
    data = r.json()
    for kill in data['data']['kills']:
        if kill['killer_puuid'] == puuid:
            print(f"Killed {kill['victim_display_name']}")
            kill_events.append(kill)


