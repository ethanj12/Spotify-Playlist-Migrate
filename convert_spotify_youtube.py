import os

import youtube_class
import spotify_client

def get_spotify_client():
    spotify_client_id = os.environ.get("spotify_api_client_id")
    spotify_client_secret = os.environ.get("spotify_api_client_secret")

    spotify = spotify_client.SpotifyAPI(client_id=spotify_client_id, client_secret=spotify_client_secret)
    return spotify



spotify_client = get_spotify_client()
spotify_client.get_access_token()

username = input("Username: ")

id_playlists_of_user = spotify_client.get_playlists_id_user(f"{username}")
dict_playlist_name_to_id = spotify_client.make_dict_playlistname_playlistid_from_user(username)
option_value = 1
for key in dict_playlist_name_to_id:
    print(f"{key}-{option_value}")
    option_value += 1
playlist_selection = input("Which playlist would you like to pick: ")
spotify_playlist_id = str(id_playlists_of_user[int(playlist_selection) - 1])
youtube_search_terms = spotify_client.get_youtube_search_terms_from_playlist_id(spotify_playlist_id)


youtube = youtube_class.youtubeAPI()
youtube.create_client()
youtube_playlist_id = youtube.create_new_playlist()
youtube_search_terms = youtube_search_terms[0:50]
for song in youtube_search_terms:
    print(f"{song}")
    youtube_video_id = youtube.search_for_song(song)
    youtube.add_video_to_playlist(youtube_playlist_id, youtube_video_id)

