"""
Lab_2, Task_2
"""
import os
import json
import base64
import requests
from dotenv import load_dotenv

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


def search_for_artist(token_, artist_name):
    """
    The function do something
    :param artist_name:
    :param token_: I don`t know
    :return: something
    """
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token_)
    query = f'?q={artist_name}&type=artist&limit=1'

    query_url = url + query
    result = requests.get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    if len(json_result) == 0:
        print('No artist with this name')
        return None
    return json_result[0]


def get_songs_by_artist(token_, artist_id: str):
    url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=us'
    headers = get_auth_header(token_)
    result = requests.get(url, headers=headers)
    json_result = json.loads(result.content)['tracks']
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
    return get_json_file(name_of_artist)['id']


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


def main(artist_name: str):
    """
    The function do something
    :param artist_name: name of artist
    :return: something
    >>> main('Queen')
    ('Queen', '1. Bohemian Rhapsody - Remastered 2011', '1dfeR4HaWDbWqFHLkxsg1d', \
['CA', 'US'], ['classic rock', 'glam rock', 'rock'])
    """
    return artist_name, get_list_of_songs(artist_name)[0], get_artist_id(artist_name), available_markets(artist_name), \
           get_genres_of_artist(artist_name)


name_of = input('Enter name of artist: >>> ')
print('1: Name of artist. \n2: The most popular song.'
      ' \n3: List of top 10 songs. \n4: Artist ID. \n5: Genres. \n6: All \n>>> ')
res = input('Chose one what do tou need: >>> ')

if res == '1':
    print(name_of)
if res == '2':
    print(get_list_of_songs(name_of)[0])
if res == '3':
    print(get_list_of_songs(name_of))
if res == '4':
    print(get_artist_id(name_of))
if res == '5':
    print(available_markets(name_of))
if res == '6':
    print(main(name_of))
else:
    print('Opps, number out of options')

# import timeit
# print(timeit.timeit())
