import requests
import json
from requests.auth import HTTPBasicAuth
from easy_spotify.artist import Artist


class Spotify:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = self.get_access_token()

    def __repr__(self):
        return "Spotify API Wrapper"

    def get_access_token(self):
        token_url = 'https://accounts.spotify.com/api/token'
        auth = HTTPBasicAuth(self.client_id, self.client_secret)
        data = {'grant_type': 'client_credentials'}
        request_token = requests.post(token_url, data, auth=auth)
        if request_token:
            if request_token.ok:
                return json.loads(request_token.text)['access_token']
            else:
                print(f"Request token not ok, error code: {request_token.status_code}")
        print(f"Token Access Failed.")
        exit()

    def _make_request(self, url, parameters=None):
        headers = {'Authorization': 'Bearer ' + self.token}
        data = requests.get(url, headers=headers, params=parameters)
        if data.ok:
            return data
        print(f"Request failed to {url}. Error type: {data.status_code}")
        return None

    def get_artist_object(self, artist_id):
        artist_info = self.get_artist_info_from_id(artist_id)
        artist_albums = self.get_albums_from_id(artist_id)
        artist_top_tracks = self.get_artist_top_tracks_from_id(artist_id, True)
        if artist_info and artist_albums:
            artist = Artist(artist_info["name"], artist_id, artist_info["followers"], artist_info["genres"],
                            artist_info["popularity"], artist_info["image_link"], artist_albums, artist_top_tracks)
            return artist
        print("Unable to create artist object.")
        return None

    def get_artist_id(self, search_query):
        artist_id_data = self._make_request("https://api.spotify.com/v1/search",
                                            {"query": search_query, "type": "artist", "limit": 1})
        if artist_id_data:
            artist_id_json = artist_id_data.json()
            if artist_id_json["artists"]["total"] == 0:
                print("No artist was found.")
                return None
            return artist_id_json["artists"]["items"][0]["id"]
        print("Request failed. No artist id was obtained.")
        return None

    def get_track_id(self, search_query):
        track_id_data = self._make_request("https://api.spotify.com/v1/search",
                                            {"query": search_query, "type": "track", "limit": 1})
        if track_id_data:
            track_id_json = track_id_data.json()
            if track_id_json["tracks"]["total"] == 0:
                print("No track was found.")
                return None
            return track_id_json["tracks"]["items"][0]["id"]

    def get_multiple_track_id(self, search_queries):
        track_ids = []
        for query in search_queries[:20]:
            track_id = self.get_track_id(query)
            track_ids.append(track_id)
        return track_ids

    def get_artist_info_from_name(self, artist_name):
        artist_id = self.get_artist_id(artist_name)
        if artist_id:
            return self.get_artist_info_from_id(artist_id)
        return None

    def get_artist_info_from_id(self, artist_id):
        artist_info_data = self._make_request(f"https://api.spotify.com/v1/artists/{artist_id}")
        if artist_info_data:
            artist_info_json = artist_info_data.json()
            followers = artist_info_json["followers"]["total"]
            genres = artist_info_json["genres"]
            image_link = artist_info_json["images"][0]["url"]
            popularity = artist_info_json["popularity"]
            name = artist_info_json["name"]
            return {"name": name, "genres": genres, "image_link": image_link,
                    "popularity": popularity, "followers": followers}
        print("Request failed. No artist information was obtained.")
        return None

    def get_albums_from_id(self, artist_id, just_id_and_name=False):
        artist_albums_data = self._make_request(f"https://api.spotify.com/v1/artists/{artist_id}/albums")
        if artist_albums_data:
            artist_albums = []
            for album in artist_albums_data.json()["items"]:
                album_id = album["id"]
                album_name = album["name"]
                if just_id_and_name:
                    artist_albums.append({"id": album_id, "name": album_name})
                else:
                    artist_name = album["artists"][0]["name"]
                    release_date = album["release_date"]
                    total_tracks = album["total_tracks"]
                    album_cover = album["images"][0]["url"]
                    artist_albums.append({"artist": artist_name, "id": album_id, "name": album_name,
                                          "release_date": release_date, "total_tracks": total_tracks,
                                          "cover": album_cover})
            return artist_albums
        print("Request failed. No albums were obtained.")
        return None

    def get_albums_from_name(self, artist_name, just_id_and_name=False):
        artist_id = self.get_artist_id(artist_name)
        if artist_id:
            return self.get_albums_from_id(artist_id, just_id_and_name)
        return None

    def get_artist_top_tracks_from_id(self, artist_id, just_id_and_name=False):
        top_tracks_data = self._make_request(f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks",
                                             {"market": "US"})
        if top_tracks_data:
            artist_tracks = []
            for track in top_tracks_data.json()["tracks"]:
                track_id = track["id"]
                track_name = track["name"]
                if just_id_and_name:
                    artist_tracks.append({"id": track_id, "name": track_name})
                else:
                    album_name = track["album"]["name"]
                    is_explicit = track["explicit"]
                    duration = track["duration_ms"]
                    track_artists = []
                    for artist in track["artists"]:
                        track_artists.append({"name": artist["name"], "id": artist["id"]})
                    artist_tracks.append({"id": track_id, "track_name": track_name, "artists": track_artists,
                                          "album_name": album_name, "is_explicit": is_explicit, "duration": duration})
            return artist_tracks
        return None

    def get_artist_top_tracks_from_name(self, artist_name, just_id_and_name=False):
        artist_id = self.get_artist_id(artist_name)
        if artist_id:
            return self.get_artist_top_tracks_from_id(artist_id, just_id_and_name)
        return None
    
    def get_tracks_of_album(self, album_id):
        tracks_data = self._make_request(f"https://api.spotify.com/v1/albums/{album_id}/tracks", {"limit": 50})
        if tracks_data:
            tracks = []
            for track in tracks_data.json()["items"]:
                track_name = track["name"]
                track_id = track["id"]
                artists = []
                for artist in track["artists"]:
                    artists.append({"name": artist["name"], "id": artist["id"]})
                tracks.append({"name": track_name, "id": track_id, "artists": artists})
            return tracks
        return None

    def get_track_audio_features(self, track_id):
        audio_features_data = self._make_request(f"https://api.spotify.com/v1/audio-features/{track_id}")
        if audio_features_data:
            return audio_features_data.json()
        return None

    def get_related_artists(self, artist_id):
        related_artists_data = self._make_request(f"https://api.spotify.com/v1/artists/{artist_id}/related-artists")
        if related_artists_data:
            related_artists = []
            for artist in related_artists_data.json()["artists"]:
                artist_name = artist["name"]
                artist_id = artist["id"]
                related_artists.append({"name": artist_name, "id": artist_id})
            return related_artists
        return None

    def get_multiple_tracks_audio_features(self, tracks_id):
        id_string = ""
        for track_id in tracks_id:
            id_string += track_id + ","
        audio_features_data = self._make_request(f"https://api.spotify.com/v1/audio-features/?ids={id_string[:-1]}")
        if audio_features_data:
            return audio_features_data.json()
        return None

    def get_track_info(self, track_id):
        track_info_data = self._make_request(f"https://api.spotify.com/v1/tracks/{track_id}")
        if track_info_data:
            track_info_json = track_info_data.json()
            name = track_info_json["album"]["artists"][0]["name"]
            artist_id = track_info_json["album"]["artists"][0]["id"]
            song = track_info_json["name"]
            image = track_info_json["album"]["images"][1]
            return {"name": name, "artist_id": artist_id, "song": song, "image": image}

    def get_multiple_tracks_info(self, tracks_id):
        id_string = ""
        for track_id in tracks_id:
            id_string += track_id + ","
        track_info_data = self._make_request(f"https://api.spotify.com/v1/tracks/?ids={id_string[:-1]}")
        if track_info_data:
            tracks_info = []
            tracks = track_info_data.json()["tracks"]
            for track in tracks:
                name = track["album"]["artists"][0]["name"]
                artist_id = track["album"]["artists"][0]["id"]
                song = track["name"]
                image = track["album"]["images"][1]
                tracks_info.append({"name": name, "artist_id": artist_id, "song": song, "image": image})
            return tracks_info
        return None


spotify = Spotify("ec89b6ab05d444c7a1f958daf52e9f79", "fffeda3a63324af4988a25982d016fed")
h = spotify.get_multiple_track_id(["Look at her now", "Lover", "Baby", "Hello"])
a = spotify.get_multiple_tracks_info(h)
print(a)

