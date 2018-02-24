"""
Get song info.
"""
import shutil
import os
import mpd
import pathlib

from . import brainz
from . import util


def init(port=6600):
    """Initialize mpd."""
    client = mpd.MPDClient()

    try:
        client.connect("localhost", port)
        return client

    except ConnectionRefusedError:
        print("error: Connection refused to mpd/mopidy.")
        os._exit(1)  # pylint: disable=W0212


def get_art(cache_dir, size, client):
    """Get the album art."""
    song = client.currentsong()

    if len(song) < 2:
        print("album: Nothing currently playing.")
        return

    file_name = f"{song['artist']}_{song['album']}_{size}.jpg".replace("/", "")
    file_name = cache_dir / file_name
    songdir  =  os.path.expanduser("~")+'/Music/'+'/'.join(song['file'].split('/')[:-1])

    for extension in ['.jpg','.jpeg','.png']:
        art_name = songdir+'/cover'+extension
        if os.path.exists(art_name): 
            shutil.copy(pathlib.Path(art_name), cache_dir / "current.jpg")
            print("album: Found local art.")
            break

    else:
        if file_name.is_file():
            shutil.copy(file_name, cache_dir / "current.jpg")
            print("album: Found cached art.")

        else:
            print("album: Downloading album art...")

            brainz.init()
            album_art = brainz.get_cover(song, size)

            if album_art:
                util.bytes_to_file(album_art, cache_dir / file_name)
                util.bytes_to_file(album_art, cache_dir / "current.jpg")

                print(f"album: Swapped art to {song['artist']}, {song['album']}.")
