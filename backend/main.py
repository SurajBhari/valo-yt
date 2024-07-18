from flask import Flask, request, jsonify
from chat_downloader.sites import YouTubeChatDownloader
from chat_downloader import ChatDownloader
import requests
from datetime import datetime, timedelta, timezone
import valo_api as vapi
import urllib
import os
import json


app = Flask(__name__)


@app.route("/api/<video_id>/")
def api(video_id):
    if video_id +".json" in os.listdir("cache"):
        with open(f"cache/{video_id}.json") as f:
            return jsonify(json.load(f))

    with open("config.json") as f:  
        config = json.load(f)
    try:
        api_key = config['api_key']
    except KeyError:
        return jsonify({"error": "API Key not found"})
    vid = YouTubeChatDownloader().get_video_data(video_id=video_id)
    if vid['author_id'] not in config:
        return jsonify({"error": "Author not found"})
    channel_id = vid['author_id']
    start_time = vid['start_time']  / 1000000 # start time in seconds
    end_time = vid['end_time'] / 1000000 # end time in seconds

    _id = config[channel_id]
    url = f"https://api.henrikdev.xyz/valorant/v1/lifetime/matches/{_id['region']}/{_id['name']}/{_id['tag']}"
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
    # store these kill events in cache so that we don't have to do this again
    if local:
        if "cache" not in os.listdir():
            os.mkdir("cache")
        with open(f"cache/{video_id}.json", "w+") as f:
            json.dump(kill_events, f, indent=4)
    return jsonify(kill_events)


local = False
if __name__ == "__main__":
    local = True
    app.run(port=80, host="0.0.0.0")
