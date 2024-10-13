import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

scope = "user-library-read,playlist-read-private,playlist-modify-private"

os.environ["SPOTIPY_CLIENT_ID"] = ""
os.environ["SPOTIPY_CLIENT_SECRET"] = ""
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:1234"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_playlists()

playlistName = "Rueda Slow Eva BPM"

playlist = next(iter([x for x in results['items'] if x['name'] == playlistName]))
playlistId = playlist["id"]

items = sp.playlist_items(playlistId)

tracks = []

#for index,item in enumerate(items["items"]):

    #trackId = item["track"]["id"]

    # analysis = sp.audio_analysis(trackId)

    # bars = analysis["bars"]

    # secondsPerPar = 0
    # confidences = 0

    # for bar in bars:
    #     secondsPerPar = secondsPerPar + bar["duration"] * bar["confidence"]
    #     confidences = confidences + bar["confidence"]

    # secondsPerPar = secondsPerPar / confidences

    # bpm = 60 * 8 / secondsPerPar

    # tracks.append((trackId, bpm, index))

#tracks = sp.audio_features([x["track"]["id"] for x in items["items"]])

#print(items["items"][0])

newTracks = []


for index,item in enumerate(items["items"]):
    id = item["track"]["id"]
    track = sp.audio_features([id])


    bpm = track[0]['tempo']

    if bpm < 120:
        bpm *= 2



    newTracks.append((id, bpm, index, item["track"]["name"])) #item["track"]["track_number"]))

newTracks.sort(key=lambda track: track[1])

#print(len(newTracks))
#print(newTracks)

#for index,newTrack in enumerate(newTracks):
    #sp.playlist_reorder_items(playlistId, newTrack[2], index)

user = sp.current_user()["id"]

playlist2 = sp.user_playlist_create(user, playlistName + " bpm", False, False)
print(playlist2)

sp.playlist_add_items(playlist2["id"], [x[0] for x in newTracks])