# Spotify to Youtube App

This program uses the Spotify and Youtube API to structure and convert Spotify playlists to Youtube Playlists. This is done so the user can have all of the music videos of their songs from their playlist in one place, with almost every one of them being the official video if it exists.

# How to use

1. First you must create a Spotify Developer Account and register an app with a client ID and a client secret in order to use the app.
2. Add the client id and client secret to your enviroment variable of your system (tutorial here):
   WINDOWS: https://www.youtube.com/watch?v=IolxqkL7cD8&ab_channel=CoreySchafer
   MAC/LINUX: https://www.youtube.com/watch?v=5iWhQWVXosU&t=0s&ab_channel=CoreySchafer
   Name these variables spotify_api_client_id and spotify_api_client_secret respectively.
3.  Make sure the playlist you want to copy is public
4.  Run convert_to_spotify.py, inputting username and the playlist you want to copy
5.  Login to your youtube account when prompted
6.  Choose how many songs you would like to copy over
7.  Go to your Youtube account and ensure that the playlists were added

# WARNING ABOUT QUOTAS

Through the Youtube API, there is a certain amount of quota allowance a day. Almost any call to the API uses quota, so use it sparingly. There is 10,000 quota per day, but to create a playlist costs 50 quota, and each song added after that is 150 quota (searching-100 quota and adding to playlist-50 quota). This means that per day, there is only 66 songs that are able to be added to your playlist. Please be kind and think of others before adding songs!

# Example Spotify Playlist
![Screenshot 2023-03-14 225339](https://user-images.githubusercontent.com/85595934/225196015-41401ce2-2291-48f0-b14a-2d4ba4037d32.png)
  
# Converting some Spotify Playlists to Youtube
![Gif of Spotify Creation](https://user-images.githubusercontent.com/85595934/225198373-93929f86-486f-4f64-81a3-4040bc1292d0.gif)

#Final Youtube Video Playlist
![Screenshot 2023-03-14 232841](https://user-images.githubusercontent.com/85595934/225198755-c5fb5806-9683-4076-9e16-0e6db2ccebb5.png)



