# import utils
# spotify_tracks = utils.get_spotify_tracks('4fwiA5ORtmUeWEhM6l3xzf')

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

proxy_ip = {
    'https': 'http://127.0.0.1:7890',
    'http': 'http://127.0.0.1:7890'
}
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="bfe25b230848448fa2f5150c3b43fb0c",
                                                           client_secret="2a712208bf844a60ab6e8d1e9653f0d5"))

results = sp.search(q='weezer', limit=20)
for idx, track in enumerate(results['tracks']['items']):
    print(idx, track['name'])