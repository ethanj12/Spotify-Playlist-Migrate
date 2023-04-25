<div align="center">
   <img src="https://user-images.githubusercontent.com/85595934/234146324-f1891c8e-4a6b-4bf4-9cfa-627ca098f8e7.png">

This program uses the Spotify and Youtube API to structure and convert Spotify playlists to Youtube Playlists. This is done so the user can have all of the music videos of their songs from their playlist in one place, with almost every one of them being the official video if it exists.

# How to use
<ol align="left">
   <li>First you must create a Spotify Developer Account and register an app with a client ID and a client secret in order to use the app.</li>
   <li>Add the client id and client secret to your enviroment variable of your system (tutorial here):
   WINDOWS: https://www.youtube.com/watch?v=IolxqkL7cD8&ab_channel=CoreySchafer
   MAC/LINUX: https://www.youtube.com/watch?v=5iWhQWVXosU&t=0s&ab_channel=CoreySchafer
   Name these variables spotify_api_client_id and spotify_api_client_secret respectively.</li>
   <li>Make sure the playlist you want to copy is public</li>
   <li>Run convert_to_spotify.py, inputting username and the playlist you want to copy</li>
   <li>Login to your youtube account when prompted</li>
   <li>Choose how many songs you would like to copy over</li>
   <li>Go to your Youtube account and ensure that the playlists were added</li>
</ol>

# WARNING ABOUT QUOTAS

Through the Youtube API, there is a certain amount of quota allowance a day. Almost any call to the API uses quota, so use it sparingly. There is 10,000 quota per day, but to create a playlist costs 50 quota, and each song added after that is 150 quota (searching-100 quota and adding to playlist-50 quota). This means that per day, there is only 66 songs that are able to be added to your playlist. Please be kind and think of others before adding songs!

# Example Spotify Playlist
![Screenshot 2023-03-14 225339](https://user-images.githubusercontent.com/85595934/225196015-41401ce2-2291-48f0-b14a-2d4ba4037d32.png)
  
# Converting some Spotify Playlists to Youtube
<img src=https://user-images.githubusercontent.com/85595934/234144692-f970373e-bf2d-42df-bd8a-d24ee590eb9a.gif width=800px>

</div>
