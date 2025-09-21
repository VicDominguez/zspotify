import os.path

from const import ROOT_PATH
from zspotify import ZSpotify


def get_playlist_ids() -> list:
    """ Obtain all ids from .playlist_ids"""
    hidden_file_path = os.path.join(ZSpotify.get_config(ROOT_PATH), '.playlist_ids')

    if os.path.exists(hidden_file_path):
        # Read existing ids
        with open(hidden_file_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        result = [line.split(",")[0] for line in lines]
    else:
        result = []
    return result


def is_playlist_on_playlist_file(playlist_id: str) -> str | None:
    """ Check if playlist_id is on .playlist_ids. If is there, return name of the folder"""
    hidden_file_path = os.path.join(ZSpotify.get_config(ROOT_PATH), '.playlist_ids')

    if os.path.exists(hidden_file_path):
        # Read existing ids
        with open(hidden_file_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        # Dump file into key value
        data = {
            parts[0]: parts[1]
            for line in lines if "," in line
            for parts in [line.split(",")]
        }
        result = data.get(playlist_id)
    else:
        result = None
    return result


def purge_playlists_id():
    """ Remove lines in .playlists file if they aren't part of song_ids fetched from playlist """
    downloaded_playlists = [f.name for f in os.scandir(ZSpotify.get_config(ROOT_PATH)) if f.is_dir()]

    hidden_file_path = os.path.join(ZSpotify.get_config(ROOT_PATH), '.playlist_ids')
    hidden_file_path_tmp = os.path.join(ZSpotify.get_config(ROOT_PATH), '.playlist_ids_tmp')

    with open(hidden_file_path, 'r', encoding='utf-8') as fin, \
            open(hidden_file_path_tmp, 'w', encoding='utf-8') as fout:
        for line in fin.readlines():
            playlist_name = line.split(",")[1].strip()
            if playlist_name in downloaded_playlists:
                fout.write(line)
    os.replace(hidden_file_path_tmp, hidden_file_path)


def save_playlist_info(playlist_id, playlist_name):
    """ Appends playlist info to .playlist_ids file in root directory """

    hidden_file_path = os.path.join(ZSpotify.get_config(ROOT_PATH), '.playlist_ids')
    with open(hidden_file_path, "a", encoding="utf-8") as f:
        f.write(f"{playlist_id},{playlist_name}\n")


def update_playlist_info(playlist_id, old_playlist_name, new_playlist_name):
    """ Update playlist entry on .playlist_ids file and rename playlist folder """

    # Rename folder
    old_folder = os.path.join(ZSpotify.get_config(ROOT_PATH), old_playlist_name)
    new_folder = os.path.join(ZSpotify.get_config(ROOT_PATH), new_playlist_name)

    os.replace(old_folder, new_folder)

    # Update playlist file
    hidden_file_path = os.path.join(ZSpotify.get_config(ROOT_PATH), '.playlist_ids')
    hidden_file_path_tmp = os.path.join(ZSpotify.get_config(ROOT_PATH), '.playlist_ids_tmp')

    with open(hidden_file_path, 'r', encoding='utf-8') as fin, \
            open(hidden_file_path_tmp, 'w', encoding='utf-8') as fout:
        for line in fin.readlines():
            line_playlist_id = line.split(",")[1].strip()
            if line_playlist_id == playlist_id:
                fout.write(f"{playlist_id},{new_playlist_name}\n")
            else:
                fout.write(line)
    os.replace(hidden_file_path_tmp, hidden_file_path)
