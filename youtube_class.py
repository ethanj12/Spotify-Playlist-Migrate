import os
import pickle
from sys import api_version
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import googleapiclient
from googleapiclient.discovery import build
from requests.api import request




class youtubeAPI(object):
    youtube_credentials = None
    api_service_name = "youtube"
    api_version = "v3"
    client = None


    def __init__(self):
        super().__init__
        self.__load_token_from_pickle()

    def __load_token_from_pickle(self):
        print("Loading token from pickle")
        if os.path.exists("C:/Users/ethan/code/python/youtube_token.pickle"):
            print("Loading credientials")
            with open("C:/Users/ethan/code/python/youtube_token.pickle", "rb") as token:
                self.youtube_credentials = pickle.load(token)
        else:
            self.__get_new_oauth_token()


    def __get_new_oauth_token(self):
        print("Getting new OAuth token")
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json",
        scopes=["https://www.googleapis.com/auth/youtube"] 
        )
        flow.run_local_server(port=8080, prompt="consent", authorization_prompt_message="")

        credentials = flow.credentials
        with open("C:/Users/ethan/code/python/youtube_token.pickle", "wb") as f:
            pickle.dump(credentials, f)

        self.__load_token_from_pickle()

    def create_client(self):
        if not self.youtube_credentials:
            if not self.youtube_credentials.valid:
                self.__get_new_access_token()     
        self.client = build(self.api_service_name, self.api_version, credentials=self.youtube_credentials)

    def __get_new_access_token(self):
        print("Getting new Access Token")
        if not self.youtube_credentials or not self.youtube_credentials.valid:
            if self.youtube_credentials and self.youtube_credentials.expired and self.youtube_credentials.refresh_token:
                self.youtube_credentials.refresh(Request())
            else:
                self.get_new_oauth_token()

    def create_new_playlist(self, title="Music Videos", desc="test desc"):
        self.__get_new_access_token()
        request = self.client.playlists().insert(
            part="snippet",
            body={
                "snippet": {
                    "title": f"{title}",
                    "description" : f"{desc}"
                }
            }
        )
        response = request.execute()
        return response['id']
        
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

