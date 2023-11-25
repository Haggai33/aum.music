import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
REDIRECT_URI = 'http://localhost:8888/callback'

# Initialize Spotify API client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope='user-follow-read user-follow-modify'))

def get_all_followed_artists(sp):
    """Retrieve all artists the user is currently following."""
    followed_artists = set()
    results = sp.current_user_followed_artists(limit=50)

    while results:
        artists = results['artists']
        for item in artists['items']:
            followed_artists.add(item['id'])

        if artists['next']:
            results = sp.next(artists)
        else:
            break

    return followed_artists

def get_playlist_artist_ids(sp, playlist_id):
    """Retrieve all artist IDs from a playlist."""
    artist_ids = set()
    results = sp.playlist_tracks(playlist_id)

    while results:
        for item in results['items']:
            track = item['track']
            if track:
                for artist in track['artists']:
                    artist_ids.add(artist['id'])

        if results['next']:
            results = sp.next(results)
        else:
            break

    return artist_ids

def follow_new_artists_in_playlist(sp, playlist_url):
    playlist_id = playlist_url.split('/')[-1].split('?')[0]
    followed_artist_ids = get_all_followed_artists(sp)
    playlist_artist_ids = get_playlist_artist_ids(sp, playlist_id)

    new_artists = []
    for artist_id in playlist_artist_ids:
        if artist_id not in followed_artist_ids:
            sp.user_follow_artists([artist_id])
            artist_info = sp.artist(artist_id)
            new_artists.append(artist_info['name'])

    return new_artists

def main():
    while True:
        playlist_url = input("Enter the Spotify playlist URL (or 'q' to quit): ")
        if playlist_url.lower() == 'q':
            break

        new_artists = follow_new_artists_in_playlist(sp, playlist_url)

        if new_artists:
            print("New artists added to your follow list:")
            for artist in new_artists:
                print(artist)
        else:
            print("You are already following all the artists in this playlist.")

if __name__ == "__main__":
    main()
