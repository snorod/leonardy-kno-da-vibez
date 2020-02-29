import requests
import json

def spotify_search(keyword, auth_token):
    search_url = 'https://api.spotify.com/v1/search'
    search_headers = {'Authorization': 'Bearer ' + auth_token}
    search_params = {'q': keyword, 'type': 'track', 'market': 'US', 'limit': 1}
    r = requests.get(headers = search_headers, url = search_url, params = search_params)
    data = r.json()
    uri = data['tracks']['items'][0]['uri']
    return uri

def spotify_play(uri, auth_token):
    play_url = 'https://api.spotify.com/v1/me/player/play'
    play_headers = {'Authorization': 'Bearer ' + auth_token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
    play_params = {'device_id': '12dbaf0b832b408c8a44a8377217075ba5d05a91'}
    play_payload = {'uris': [uri]}
    r = requests.put(headers = play_headers, url = play_url, params = play_params, data = json.dumps(play_payload))

keyword = "circles"
auth_token = 'BQDKhMibXlXjqJTAySNVK6qWe-f84vveZITvW2_2eXLjfh_0Jh-BHk_jrcOMyEGU38vg7G9PGl4uhM8Ug_GvRfXT7HAa8OrDChhpZtUx4d5kER6moYtEvoTS8aLgtFp1kF-RNmNfWoMXsyggxoxHUtP76pHdghUbZal5-iE'
uri = spotify_search(keyword, auth_token)
spotify_play(uri, auth_token)
