import os
import pickle
from sys import api_version
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import googleapiclient
from googleapiclient.discovery import build
from requests.api import request

#Below conttains directory of where to read/write pickle file for youtube credentials
PICKLE_FILE_DIRECTORY = "C:/Users/ethan/code/python/youtube_token.pickle" 


class youtubeAPI(object):
    youtube_credentials = None
    api_service_name = "youtube"
    api_version = "v3"
    client = None


    def __init__(self):
        super().__init__
        self.__load_token_from_pickle()

    # INPUTS:  None
    # OUTPUTS: sets youtube_credentials
    # DESC: Checks if there is a pickle file of the credentials of the user in the file
    #       located in the directory. This pickle file contains both the client ID
    #       and the client secret of the API, but for this project, they will not be
    #       included in the github repository. If you would like to use this code for
    #       your own project, look in header comments and the steps will be detailed there.
    #       If there is no pickle file, then it calls __get_new_oauth_token to write a pickle file
    #       with the credentials.
    def __load_token_from_pickle(self):
        print("Loading token from pickle")
        if os.path.exists(PICKLE_FILE_DIRECTORY):  # LINE FOR DIRECTORY
            print("Loading credientials")
            with open(PICKLE_FILE_DIRECTORY, "rb") as token:
                self.youtube_credentials = pickle.load(token)
        else:
            self.__get_new_oauth_token()

    # INPUTS:  MUST HAVE JSON OF YOUTUBE CREDENTIALS. CHECK HEADER FOR INFO TO GET
    # OUTPUTS: a pickle file set in the directory of choice
    # DESC: Gets a new oauth token and loads the credentials from that oauth token
    #       into a pickle file set on the user's computer. This pickle file will contain
    #       the users client ID and the user's secret ID. These are not stored in
    #       the repo, otherwise anyone could create new calls with it. Creates a 
    #       flow object and the uses the flow object and a local server to login
    #       to google and get an oauth token.
    def __get_new_oauth_token(self):
        print("Getting new OAuth token")
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json",
        scopes=["https://www.googleapis.com/auth/youtube"] 
        )
        flow.run_local_server(port=8080, prompt="consent", authorization_prompt_message="")

        credentials = flow.credentials
        with open(PICKLE_FILE_DIRECTORY, "wb") as f:  # CHANGE DIRECTORY HERE
            pickle.dump(credentials, f)

        self.__load_token_from_pickle()
        
    # INPUTS:  None
    # OUTPUTS: gets new access token for API calls
    # DESC: Renews the access token for fucntion calls to the API.
    #       Checks if user has youtube_credentials set or if the youtube_credentials
    #       are valid, and if they are not, calls __get_new_oauth_token in order
    #       to set youtube credentials. Checks if the credentials are expried
    #       or if the refresh token if they have a refresh token, and if the user
    #       does, then uses the refresh token to get a new access token.
    def __get_new_access_token(self):
        print("Getting new Access Token")
        if not self.youtube_credentials or not self.youtube_credentials.valid:
            if self.youtube_credentials.expired and self.youtube_credentials.refresh_token:
                self.youtube_credentials.refresh(Request())
            else:
                self.get_new_oauth_token()

    # INPUTS:  None
    # OUTPUTS: youtube client
    # DESC: Creates a youtube client to make API calls and adds this to the
    #       Youtube API object. Checks if credentials are valid and that they are set
    #       and then builds an instance to make function calls.
    def create_client(self):
        if not self.youtube_credentials:
            if not self.youtube_credentials.valid:
                self.__get_new_access_token()     
        self.client = build(self.api_service_name, self.api_version, credentials=self.youtube_credentials)

    # INPUTS:  Title to add to youtube playlist and username of user
    # OUTPUTS: Returns the ID of the playlist created
    # DESC: Creates a new playlist on youtube on the channel https://www.youtube.com/channel/UCXoVw6HmAxNC_oT_hWVD6JQ
    #       Passing in title of playlist is ideal, since it will allow you to find the 
    #       playlist you created easily. Returns the id of the playlist in order to add songs to it
    #       in later calls.
    #
    #       This function automatically another access token. Access tokens
    #       get used up quickly, and having it call for a new access token everytime is worth
    #       in order to maintain and not have to check everytime if the access token is still
    #       valid. If code would need to be faster, this line could be optimized to check
    #       if the access token is still valid, but this works fine for my purpose. 
    #
    #       EACH NEW PLAYLIST COSTS 50 QUOTA POINTS
    def create_new_playlist(self, title="Music Videos", username="Rick Astley"):
        self.__get_new_access_token()
        request = self.client.playlists().insert(
            part="snippet",
            body={
                "snippet": {
                    "title": f"{title}",
                    "description" : f"Playlist of videos for{username} that is located in their playlist of {title} on Spotify"
                }
            }
        )
        response = request.execute()
        return response['id']

     # INPUTS:  Search term to look up on Youtube
    # OUTPUTS: Video with highest views matching search results from youtube
    # DESC: Looks up the video ID with the search term. Search term in this instance and for
    #       my purpose is assumed to be "{song name} {song artist}". 
    #
    #       The video returned will
    #       be the highest viewed video fitting the search term. This is done in order
    #       to try and get the official youtube channel of the artist and promote and give
    #       views to the original artist. I have tested that if you do not put order="viewCount"
    #       in the API call, then sometimes it will not return the video from the original artist
    #       even if they do have a youtube channel. This was the best solution that I could
    #       find, but this could be a point of experimentation. 
    #
    #       This function automatically another access token. Access tokens
    #       get used up quickly, and having it call for a new access token everytime is worth
    #       in order to maintain and not have to check everytime if the access token is still
    #       valid. If code would need to be faster, this line could be optimized to check
    #       if the access token is still valid, but this works fine for my purpose. 

    #       EACH SEARCH USES 100 QUOTA POINTS (AKA A LOT!)
    def search_for_song(self, search_term):
        self.__get_new_access_token
        request = self.client.search().list(
            part="snippet",
            order="viewCount",
            q=f"{search_term}",
            type="video"
        )
        response = request.execute()

        return response['items'][0]['id']['videoId']

    # INPUTS:  Youtube id of playlist ot add song to; Youtube id of song to add to playlist
    # OUTPUTS: NONE
    # DESC: With playlist ID and song ID, adds song to playlist. Structures the API call
    #       and automatically gets a new access token every time is called. Access tokens
    #       get used up quickly, and having it call for a new access token everytime is worth
    #       in order to maintain and not have to check everytime if the access token is still
    #       valid. If code would need to be faster, this line could be optimized to check
    #       if the access token is still valid, but this works fine for my purpose. 
    #
    #       EACH ADD VIDEO COSTS 50 QUOTA POINTS
    def add_video_to_playlist(self, playlist_id, song_id):
        self.__get_new_access_token()
        request = self.client.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": f"{playlist_id}",
                    "resourceId" : {
                        "kind": "youtube#video",
                        "videoId": f"{song_id}"
                    }
                }
            }
        )
        response = request.execute()