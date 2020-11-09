"""
Util functions.
"""
import pathlib
import pywal
import shutil
import os


def bytes_to_file(input_data, output_file):
    """Save bytes to a file."""
    pathlib.Path(output_file.parent).mkdir(parents=True, exist_ok=True)

    with open(output_file, "wb") as file:
        file.write(input_data)

def reload_pywal(image_path, cache_dir=pathlib.Path.home()/'.cache'/'wal',
                 color_count=8, cached_colors=[{}]):

    scheme_dir = os.path.join(cache_dir, "schemes")
    shutil.rmtree(scheme_dir, ignore_errors=True)

    image = pywal.image.get(image_path, cache_dir)

    # Return a dict with the palette.
    #
    # The last argument is 'quiet' mode. When set to true, no notifications
    # are displayed.
    colors = pywal.colors.get(image)

    if cached_colors[0] == colors:
        return
    cached_colors[0] = colors

    # Apply the palette to all open terminals.
    # Second argument is a boolean for VTE terminals.
    # Set it to true if the terminal you're using is
    # VTE based. (xfce4-terminal, termite, gnome-terminal.)
    print(colors)
    print(cache_dir)
    pywal.sequences.send(colors, cache_dir, True)

    # Export all template files.
    pywal.export.every(colors, cache_dir)

    # Reload xrdb, i3 and polybar.
    #pywal.reload.env("/etc/foo/custom.Xresources")

    # Reload individual programs.
    pywal.reload.i3()
    #pywal.reload.polybar()
    os.system('polybar-msg cmd restart')
    pywal.reload.xrdb()

