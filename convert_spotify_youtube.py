#        CONVERT_SPOTIFY_YOUTUBE.py
# ------------------------------------------
# Uses the youtube class and the spotify_client class in order to make
# make API calls to both the Spotify and Youtube API And convert songs
# on any public spotify playlist into a youtube playlist. This is done in
# order to try and provide a playlist with each of the songs music video
# in a easy to access place. The only thing that a user needs is the username
# of the owner of the playlist and know the name of the playlist. One of the big
# limitation of this program is that the youtube API only allows for 10,000 "quota points"
# per day, and each addition of a song to a playlist uses 150 quota points. 
import os
import youtube_class
import spotify_client

# INPUTS:  None
# OUTPUTS: returns spotify_client object used to make API calls
# DESC: Must set your spotify secret and and spotify client ID's in the environment 
#       of your computer. A easy tutorial for this in windows is here:
#       https://www.youtube.com/watch?v=IolxqkL7cD8&ab_channel=CoreySchafer
#       Spotify does not have a structured way client, so we have to create our
#       own in order to model API calls. In order to get Spotify ID and 
#       a Spotify secret, follow the tutorial in the readme of the repository.
def get_spotify_client():
    spotify_client_id = os.environ.get("spotify_api_client_id")
    spotify_client_secret = os.environ.get("spotify_api_client_secret")
    

    spotify = spotify_client.SpotifyAPI(client_id=spotify_client_id, client_secret=spotify_client_secret)
    
    spotify.get_access_token()  # Needed to make API calls

    return spotify

# INPUTS:  username to look up on spotify
# OUTPUTS: returns list with index 0 being id and index 1 being name of playlist
#          (not a tuple in case in future, want more info about playlist in this call)
# DESC: This logic handles selecting the playlist from the user's all available playlist
#       and then getting the ID and the name of that playlist. The user will ahve a choice
#       between all of their avaiable playlist, and the choices and their corresponding
#       index will be printed to the screen. The user then selects a playlist, and the
#       spotify_client object then gets the ID and the name of the playlist from the list
#       that was returned with the original call of make_dict_playlistname_playlistid_from_user()
def get_playlist_of_user(username):
    id_playlists_of_user = spotify_client.get_playlists_id_user(f"{username}")
    dict_playlist_name_to_id = spotify_client.make_dict_playlistname_playlistid_from_user(username)
    list_of_playlist_names = spotify_client.get_playlists_name_user(username)

    option_value = 1
    for key in dict_playlist_name_to_id:
        print(f"{key}-{option_value}")
        option_value += 1
    playlist_selection = get_user_input("Which playlist would you like to pick (number): ", "int")

    spotify_playlist_id = str(id_playlists_of_user[playlist_selection - 1])
    spotify_playlist_name = str(list_of_playlist_names[playlist_selection - 1])
    playlist_id_and_playlist_name = [spotify_playlist_id, spotify_playlist_name]
    return playlist_id_and_playlist_name

# INPUTS:  none
# OUTPUTS: a youtube client class with oauth token set, ready for API calls
# DESC: Creates a youtube_client object, then prepares that object for function
#       calls by setting an oauth token. Does this through a pickle file or through
#       a local webserver and logging in through google. GO to create_client() for
#       full details on what is done.
def create_youtube_client():
    youtube = youtube_class.youtubeAPI()
    youtube.create_client()
    return youtube

# INPUTS:  the youtube client; the search terms of the user (list); id of playlist to add
#          songs from search term to
# OUTPUTS: adds all songs in youtube_search_terms to playlist
# DESC: For each song in youtube_search_terms, the function searches for the song
#       on youtube, gets the video ID of that song, and then makes a call on the
#       youtube client in order to add that video to the playlist located on the channel
#       that you authorized.
#
#       WARNING: EACH SONG USES 150 QUOTA POINTS. USE SPARINGLY AND ONLY WHEN NECESSARY
def add_songs_to_playlist(youtube_client, youtube_search_terms, youtube_playlist_id):
    for song in youtube_search_terms:
        print(f"{song}")
        youtube_video_id = youtube_client.search_for_song(song)
        youtube_client.add_video_to_playlist(youtube_playlist_id, youtube_video_id)

# INPUTS:  message for console for input, target type of input
# OUTPUTS: an input from user with type "type"
# DESC: Gets an input from the user and returns the input in the 
#       type that is passed to it. For this project, the only two
#       types that we need from the user and int and string, but we could easily
#       extend this if we needed more types.
def get_user_input(message, type):
    ret = input(message)
    if type == "int": #Do not have to worry if type == str, input returns a str
        try:
            ret = int(ret)
            return ret
        except:
            print("Please enter an integer")
            get_user_input(message, type)
    return ret



spotify_client = get_spotify_client()
#Start using Spotify Client
username = get_user_input("Username: ", str)
spotify_playlist_to_search = get_playlist_of_user(username)
spotify_playlist_to_search_id = spotify_playlist_to_search[0]  # Used to get sogns and artists for search terms
spotify_playlist_to_search_name = spotify_playlist_to_search[1]  # Used to name playlist on Youtube
youtube_search_terms = spotify_client.get_youtube_search_terms_from_playlist_id(spotify_playlist_to_search_id)
#Finsihed with Spotify client
#Start calls to the Youtube API
youtube = create_youtube_client()
youtube_playlist_id = youtube.create_new_playlist(spotify_playlist_to_search_name, username)
number_of_songs_to_add = get_user_input("How many songs would you like added from your playlist?: ", "int")
youtube_search_terms = youtube_search_terms[0:number_of_songs_to_add] 
add_songs_to_playlist(youtube, youtube_search_terms, youtube_playlist_id)
print(f"You can find your new playlist at this link: https://www.youtube.com/playlist?list={youtube_playlist_id}")