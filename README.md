# Valo-YT

![Python](https://img.shields.io/badge/Python-3670A0?style=flat&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![Valorant](https://img.shields.io/badge/Valorant-FA4454?style=flat&logo=valorant&logoColor=white)
![YouTube](https://img.shields.io/badge/YouTube-FF0000?style=flat&logo=youtube&logoColor=white)

A Flask backend that **ties a Valorant player's match history to their YouTube livestream** — so you can line up what happened in-game with the moment it happened on stream.

Given a YouTube stream and a Riot ID, it pulls the stream's timing via [`chat_downloader`](https://github.com/xenova/chat-downloader) and the player's matches via the [`valo_api`](https://github.com/rairYT/valorant-api) (unofficial Valorant API), then correlates them by timestamp.

## API

```
GET /api/<video_id>/
```

Returns the correlated match/stream data for that video (results are cached per `video_id` under `cache/` so repeat requests are instant).

## Run

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Provide a `config.json` with your Valorant API key (see `backend/test.py` for the expected fields: `api_key`, plus a player's `name`/`tag`/`region`/`platform`).

## Layout

```
backend/
  main.py   # Flask API — correlate stream timing with Valorant matches
  test.py   # standalone experiment / reference for the correlation logic
```
