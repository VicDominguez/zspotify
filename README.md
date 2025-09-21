<div align="center">
    <img src="https://user-images.githubusercontent.com/12180913/138040605-c9d46e45-3830-4a4b-a7ac-c56bb0d76335.png">
    <h3 align="center">ZSpotify</h3>
    <p>A fork of ZSpotify, a Spotify downloader.</p>
</div>

## Table of Contents

- [🤔 What is this project?](#-what-is-this-project)
- [🚀 Getting Started](#-getting-started)
- [💙 Contributing](#-contributing)

## 🤔 What is this project?

This project is a fork of Zspotify, adding following features:

- User can configure if it wants to use prefix on downloaded songs.
- Retry mechanism when download failed.
- Synchronization of local files with playlist status.
- Support to copy a song from other folders if exist instead of download.
- Multi playlist download.
- Synchronization of previously downloaded playlists.

Note: This project is provided under the principles of **fair use**. It must **not** be used to share, or
distribute copyrighted content illegally.
The author does not support piracy in any form, so users are solely responsible for how they use this project.

## 🚀 Getting Started

- Install ffmpeg. It can be installed via apt for Debian-based distros or by downloading the binaries
  from [ffmpeg.org](https://ffmpeg.org) and placing them in your %PATH% in Windows. Mac users can install it
  with [Homebrew](https://brew.sh) by running `brew install ffmpeg`.
- Python 3.9-3.12. Python 3.13 removed [audioop](https://peps.python.org/pep-0594/), module used by PyDub dependency.
  Until fix on PyDub
  or replacement, Python 3.13 or upper is not supported.
- Install dependencies via [requirements.txt](requirements.txt).
- Execute :)

### Command line usage

```
Basic command line usage:
  python zspotify <track/album/playlist/episode/artist url>   Downloads the track, album, playlist or podcast episode specified as a command line argument. If an artist url is given, all albums by specified artist will be downloaded. Can take multiple urls.

Extra command line options:
  -p, --playlist       Downloads a saved playlist from your account
  -ls, --liked-songs   Downloads all the liked songs from your account
  -s, --search         Loads search prompt to find then download a specific track, album or playlist
  -ns, --no-splash     Suppress the splash screen when loading.
  -sy, --sync          Updates all playlists previously downloaded.

Options that can be configured in zs_config.json:
  ROOT_PATH                 Change this path if you don't like the default directory where ZSpotify saves the music
  ROOT_PODCAST_PATH         Change this path if you don't like the default directory where ZSpotify saves the podcasts

  SKIP_EXISTING_FILES       Set this to false if you want ZSpotify to overwrite files with the same name rather than skipping the song
  SKIP_FILE_WITHOUT_ID      Set this to false if you want ZSpotify to download file with a different name if id is not registered rather than add id and skip the song

  PREFIX                    Set this to true if you want ZSpotify to add prefix on song file when downloading playlist or album

  MUSIC_FORMAT              Can be "mp3" or "ogg", mp3 is required for track metadata however ogg is slightly higher quality as it is not transcoded.

  FORCE_PREMIUM             Set this to true if ZSpotify isn't automatically detecting that you are using a premium account

  ANTI_BAN_WAIT_TIME        Change this setting if the time waited between bulk downloads is too high or low
  GENERAL_ERROR_RETRIES     Integer with the number of retries to do when suffering general error on song download
  OVERRIDE_AUTO_WAIT        Change this to true if you want to completely disable the wait between songs for faster downloads with the risk of instability

  SYNC_FILES_WITH_PLAYLIST  Enable this option if you want to remove songs that are not part of your playlist anymore
```

### Docker Usage

```
Pull the official docker image (automatically updates):
  docker pull cooper7692/zspotify-docker
Or build the docker image yourself from the Dockerfile:
  docker build -t zspotify .
Create and run a container from the image:
  docker run --rm -v "$PWD/ZSpotify Music:/ZSpotify Music" -v "$PWD/ZSpotify Podcasts:/ZSpotify Podcasts" -it zspotify
```

We recommend using ZSpotify with a burner account.

Alternatively, there is a configuration option labled ```DOWNLOAD_REAL_TIME```, this limits the download speed to the
duration of the song being downloaded thus not appearing suspicious to Spotify.
This option is much slower and is only recommended for premium users who wish to download songs in 320kbps without
buying premium on a burner account.

**Use ZSpotify at your own risk**, the developers of ZSpotify are not responsible if your account gets banned.

### My credentials file is not working, how can I fix it?

If your credentials.json file is not working, please have a look to the
following [issue](https://github.com/kokarare1212/librespot-python/issues/277).

## 💙 Contributing

Any contributions you make are **greatly appreciated**, so if you have any idea of how to make this project better,
please [create a pull request](https://github.com/VicDominguez/zspotify/pulls).
Also, if you find any bug, please [create an issue](https://github.com/VicDominguez/zspotify/issues/new).
