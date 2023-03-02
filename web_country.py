"""
Lab_2, Task_1
"""
import os
import csv
import json
import base64
import folium
import fastapi
import requests
from dotenv import load_dotenv
from geopy.geocoders import Nominatim

load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')


def get_token() -> str:
    """
    The function return token
    :return: something
    """
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_bases64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_bases64,
        'Content-type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': "client_credentials"}
    result = requests.post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    tok = json_result["access_token"]
    return tok


token = get_token()


def get_auth_header(token_):
    return {'Authorization': 'Bearer ' + token_}


# def search_for_artist(token_, artist_name):
#     """
#     The function do something
#     :param artist_name:
#     :param token_: I don`t know
#     :return: something
#     """
#     url = 'https://api.spotify.com/v1/search'
#     headers = get_auth_header(token_)
#     query = f'?q={artist_name}&type=artist&limit=1'

#     query_url = url + query
#     result = requests.get(query_url, headers=headers)
#     json_result = json.loads(result.content)['artists']['items']
#     if len(json_result) == 0:
#         print('No artist with this name')
#         return None
#     return json_result[0]
def search_for_artist(token_: str, name: str) -> dict:
    """
    Gets json file for artist
    """
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token_)
    query = f'?q={name}&type=track&limit=1'

    q_url = url + query
    result = requests.get(q_url, headers=headers)
    j_file = json.loads(result.content)

    if len(j_file) == 0:
        return 'There is no artist with such name'

    return j_file['tracks']['items']


def get_songs_by_artist(token_, artist_id: str):
    url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=us'
    headers = get_auth_header(token_)
    result = requests.get(url, headers=headers)
    json_result = json.loads(result.content)[0]['tracks']
    return json_result


def get_json_file(name_of_artist: str) -> str:
    """
    The function return json file of artist`s information
    :param name_of_artist: name of artist
    :return: dictionary of information
    """
    return search_for_artist(token, name_of_artist)


def get_artist_id(name_of_artist: str) -> str:
    """
    The function fu=ind artist ID by name
    :param name_of_artist: name o artist
    :return: ID
    >>> get_artist_id("Queen")
    '1dfeR4HaWDbWqFHLkxsg1d'
    """
    return get_json_file(name_of_artist)[0]['id']


def get_list_of_songs(name_of_artist: str) -> list:
    """
    The function find number of top track of artist
    :param name_of_artist: name of artist
    :param count: number of songs
    :return: songs
    >>> get_list_of_songs("Queen")[0]
    '1. Bohemian Rhapsody - Remastered 2011'
    """
    songs = get_songs_by_artist(token, get_artist_id(name_of_artist))
    return [f'{idx + 1}. {song["name"]}' for idx, song in enumerate(songs)]


def get_genres_of_artist(name_of_artist: str):
    """
    The function find genre of artist
    :return: list of genres
    >>> get_genres_of_artist("Rammstein")
    ['alternative metal', 'german metal', 'industrial', 'industrial metal', 'industrial rock', 'neue deutsche harte', 'nu metal']
    """
    return get_json_file(name_of_artist)['genres']


def available_markets(artist_name: str):
    """
    The function do something
    :param artist_name:
    :return:
    >>> len(available_markets("Жадан і Собаки"))
    183
    """
    url = 'https://api.spotify.com/v1/search'
    query = f"?q=artist:{artist_name}&type=track&limit=1"
    query_url = url + query
    headers = get_auth_header(token)
    result = requests.get(query_url, headers=headers)
    json_result = json.loads(result.content)
    return json_result['tracks']['items'][0]['available_markets']


def take_coordinate(list_of_information: list) -> list:
    """
    The function find coordinate by location
    :param list_of_information: list with all needed information
    :return: coordinate
    # >>> (take_coordinate(find_location('locations.list')[:100]))
    # >>> take_coordinate(find_location('film_loc')[:100])
    """
    result = []
    for line in list_of_information[:10]:
        if line == 'XK':
            continue
        geolocator = Nominatim(user_agent="my_app_name", timeout=100)
        try:
            location = geolocator.geocode(line, timeout=100)
            result += [[location.latitude] + [location.longitude]]
        except AttributeError:
            continue
    return result


def create_map(artist_name: str):
    list_of_filtered_location = take_coordinate(search_for_artist(token, artist_name)[0]['album']['available_markets'])
    m = folium.Map(location=[49.8397, 24.0297], zoom_start=5)
    for i in list_of_filtered_location:
        try:
            folium.Marker(location=[i[0], i[1]],
                          icon=folium.Icon(color='maroon')).add_to(m)
        except IndexError:
            continue
    return m.save('map.html')


res = input('Enter artists_name: >>> ')
print(create_map(res))
