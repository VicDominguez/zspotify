import os

from tqdm import tqdm

from const import ITEMS, ID, TRACK, NAME, PREFIX, ROOT_PATH, SYNC_FILES_WITH_PLAYLIST
from playlist_info import is_playlist_on_playlist_file, update_playlist_info, save_playlist_info, \
    get_playlist_ids, purge_playlists_id
from track import download_track
from utils import fix_filename, get_directory_song_filenames, purge_songs_id
from zspotify import ZSpotify

MY_PLAYLISTS_URL = 'https://api.spotify.com/v1/me/playlists'
PLAYLISTS_URL = 'https://api.spotify.com/v1/playlists'


def get_all_playlists():
    """ Returns list of users playlists """
    playlists = []
    limit = 50
    offset = 0

    while True:
        resp = ZSpotify.invoke_url_with_params(MY_PLAYLISTS_URL, limit=limit, offset=offset)
        offset += limit
        playlists.extend(resp[ITEMS])
        if len(resp[ITEMS]) < limit:
            break

    return playlists


def get_playlist_songs(playlist_id):
    """ returns list of songs in a playlist """
    songs = []
    offset = 0
    limit = 100

    while True:
        resp = ZSpotify.invoke_url_with_params(f'{PLAYLISTS_URL}/{playlist_id}/tracks', limit=limit, offset=offset)
        offset += limit
        songs.extend(resp[ITEMS])
        if len(resp[ITEMS]) < limit:
            break

    return songs


def get_playlist_info(playlist_id):
    """ Returns information scraped from playlist """
    resp = ZSpotify.invoke_url(f'{PLAYLISTS_URL}/{playlist_id}?fields=name,owner(display_name)&market=from_token')
    return resp['name'].strip(), resp['owner']['display_name'].strip()


def download_playlist(playlist):
    """Downloads all the songs from a playlist"""

    playlist_songs = [song for song in get_playlist_songs(playlist[ID]) if song[TRACK][ID]]
    p_bar = tqdm(playlist_songs, unit='song', total=len(playlist_songs), unit_scale=True)
    enum = 1

    root_directory = os.path.join(os.path.dirname(__file__), ZSpotify.get_config(ROOT_PATH))
    sanitized_playlist_name = fix_filename(playlist[NAME].strip())
    download_directory = os.path.join(root_directory, (sanitized_playlist_name + '/'))

    actual_songs_ids = []

    playlist_folder = is_playlist_on_playlist_file(playlist[ID])

    if playlist_folder is None:
        save_playlist_info(playlist[ID], sanitized_playlist_name)
    else:
        if playlist_folder != sanitized_playlist_name:
            update_playlist_info(playlist[ID], sanitized_playlist_name)

    for song in p_bar:
        downloaded_id = download_track(song[TRACK][ID], download_directory, prefix=ZSpotify.get_config(PREFIX),
                                       prefix_value=str(enum), disable_progressbar=True)
        if downloaded_id is not None:
            actual_songs_ids.append(downloaded_id)
        p_bar.set_description(song[TRACK][NAME])
        enum += 1

    # Remove files that are not part of the playlist
    if ZSpotify.get_config(SYNC_FILES_WITH_PLAYLIST):
        # Remove entries that aren't part of the list anymore
        purge_songs_id(download_directory, actual_songs_ids)

        # Read filenames of actual playlist songs
        keep_files = get_directory_song_filenames(download_directory)
        keep_files.append('.song_ids')

        # Remove file if is not on keep_files
        for filename in os.listdir(download_directory):
            file_path = os.path.join(download_directory, filename)

            if os.path.isfile(file_path) and filename not in keep_files:
                print('\n###   DELETING:', filename, '(SONG NOT IN PLAYLIST)   ###')
                os.remove(file_path)


def download_from_user_playlist():
    """ Select which playlist(s) to download """
    playlists = get_all_playlists()

    # From 1 to n to make it more user-friendly, but this offset needs to be removed later on
    count = 1
    for playlist in playlists:
        print(str(count) + ': ' + playlist[NAME].strip())
        count += 1

    print('\n> SELECT A PLAYLIST BY ID')
    print('> SELECT A RANGE BY ADDING A DASH BETWEEN BOTH ID\'s')
    print('> SELECT MULTIPLE ENTRIES OR RANGES USING COMMAS')
    print('> For example, type 10 to get one playlist, 10-20 to get every playlist from 10 to 20 (inclusive) \n'
          'or 1,5,15-25 to get playlists 1,5 and every playlist from 15 to 25 (inclusive) \n')

    # Obtain input removing whitespaces
    raw_input = input('ID(s): ').replace(' ', '')
    # Avoid duplicates using a set
    playlist_choices = set()

    # Split via comma
    for part in raw_input.split(','):
        # Check if part is a range or single number
        # In any case, user input needs to be reduced by one
        if '-' in part:
            start, end = map(int, part.split('-'))
            playlist_choices.update(range(start - 1, end))
        else:
            playlist_choices.add(int(part) - 1)

    for playlist_number in playlist_choices:
        # Obtain playlist from index and download it
        playlist = playlists[playlist_number]
        print(f'Downloading {playlist[NAME].strip()}')
        download_playlist(playlist)

    print('\n**All playlists have been downloaded**\n')


def sync_playlists():
    print('Synchronizing playlists...')

    print("Purging file")
    purge_playlists_id()

    for playlist_id in get_playlist_ids():
        name, username = get_playlist_info(playlist_id)
        playlist_info = {ID: playlist_id, NAME: name}
        print(f'Updating {name}..')
        download_playlist(playlist_info)

    print('\n**All playlists have been synchronized**\n')
