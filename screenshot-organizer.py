import re
from pathlib import Path
import os
import shutil

def main():
    screenshots = Path('D:/Google Drive/Pictures/Screenshots')
    captures = screenshots / 'Captures'
    pattern = re.compile(r'.*?(?= \d\d?_\d\d?_\d{4})')
    extensions = (".png", ".jpg")
    for file in captures.iterdir():
        extension = os.path.splitext(file.name)[1]
        if extension not in extensions:
            continue

        game_name = pattern.match(file.name).group(0)
        # Encode as ascii to remove unicode characters that can create glitches e.g. duplicate folders
        game_name = game_name.encode('ascii', 'ignore').decode()
        # Capture sometimes adds trailing underscores for some reason - I'd rather remove these
        game_name = game_name.replace("_ ", " ")

        game_dir = screenshots / 'Test' / game_name
        game_dir.mkdir(exist_ok=True, parents=True)
        # print('Copy from %s to %s' % (file.name, game_dir))
        shutil.copy2(file, game_dir)



if __name__ == "__main__":
    main()
