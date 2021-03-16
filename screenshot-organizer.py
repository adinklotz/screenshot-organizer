import re
from pathlib import Path
import os
import shutil

def main():
    screenshots = Path('D:/Google Drive/Pictures/Screenshots')
    captures = screenshots / 'Captures'
    for file, game_name in captures_generator(captures):
        game_dir = screenshots / 'Games' / game_name
        game_dir.mkdir(exist_ok=True, parents=True)
        # Filepaths must be converted to strings because of a Python bug
        # in python <3.9, move breaks on Path objects
        shutil.move(str(file), str(game_dir))

def captures_generator(captures_path):
    pattern = re.compile(r'.*?(?= \d\d?_\d\d?_\d{4})')
    extensions = (".png", ".jpg")
    for file in captures_path.iterdir():
        extension = os.path.splitext(file.name)[1]
        if extension not in extensions:
            continue

        game_name = pattern.match(file.name).group(0)
        # Encode as ascii to remove unicode characters that can create glitches e.g. duplicate folders
        game_name = game_name.encode('ascii', 'ignore').decode()
        # Capture sometimes adds trailing underscores for some reason - I'd rather remove these
        game_name = game_name.replace("_ ", " ")
        # Windows directories can't end in a dot or a space
        game_name = re.sub(r'\.+$| +$', '', game_name)
        yield file, game_name

if __name__ == "__main__":
    main()
