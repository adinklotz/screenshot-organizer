import re
from pathlib import Path
import os
import shutil
import json
import urllib.request
import itertools

def main():
    screenshots = Path('D:/Google Drive/Pictures/Screenshots')
    captures = screenshots / 'Captures'
    steam = screenshots / 'Steam'
    mappings = MappingsManager()
    for file, game_name in itertools.chain(captures_generator(captures), steam_generator(steam)):
        game_name = mappings.map_name(clean_name(game_name))
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

def steam_generator(steam_screenshots_path):
    extensions = (".png", ".jpg")
    steam_ids = None
    for file in steam_screenshots_path.iterdir():
        extension = os.path.splitext(file.name)[1]
        if extension not in extensions:
            continue
        if steam_ids == None:
            steam_ids = load_steam_ids()
        id = file.name.split("_")[0]
        try:
            name = steam_ids[id]
        except KeyError:
            # Update the list, in case it's a game that was added since the list was downloaded
            steam_ids = update_steam_ids()
            try:
                # If it's still not there, just skip it
                name = steam_ids[id]
            except KeyError:
                continue
        yield file, name

def load_steam_ids():
    """
    Gets the steam IDs dictionary from disk if there, downloads it if not

    :return: A dictionary of (string) Steam IDs as keys and corresponding game names as values
    :rtype: Dictionary<String, String>
    """
    steam_ids_json = Path(__file__).parent / "steam_ids.json"
    if steam_ids_json.exists():
        with open(steam_ids_json, encoding="utf-8") as file:
            steam_ids_dict = json.load(file)
        return steam_ids_dict 
    else:
        return update_steam_ids()

def update_steam_ids():
    """
    Downloads the list of all games from the Steam api, and converts it into a dictionary from keys to names

    :return: A dictionary of (string) Steam IDs as keys and corresponding game names as values
    :rtype: Dictionary<String, String>
    """
    with urllib.request.urlopen("https://api.steampowered.com/ISteamApps/GetAppList/v0002/") as url:
        raw_steam_data = json.loads(url.read().decode('utf-8'))

    # Steam provides the data in the form {'applist': {'apps': [{'appid':'1234', 'name':'Game 1'}, {'appid':'5678', 'name':'Game 2'}]}}
    # I want to convert it to just a dictionary of the form {'1234':'Game 1', '5678':'Game 2'}
    steam_ids_dict = {}
    for app in raw_steam_data['applist']['apps']:
        steam_ids_dict[str(app['appid'])] = app['name']

    steam_ids_json = Path(__file__).parent / "steam_ids.json"
    with open(steam_ids_json, 'w', encoding="utf-8") as file:
        json.dump(steam_ids_dict, file)
    return steam_ids_dict

def clean_name(name):
    # source https://stackoverflow.com/questions/1976007/what-characters-are-forbidden-in-windows-and-linux-directory-names
    pattern = re.compile(r'\/|<|>|:|"|\\|\||\?|\*|\.+$| +$')
    return pattern.sub('', name)

class MappingsManager:
    def __init__(self):
        with open('mappings.json', 'r') as file:
            self.mapping = json.load(file)
            
    def map_name(self, name):
        """
        Converts the name according to a JSON mapping
        Useful when the title Capture gets includes extra stuff.
        e.g. Control comes up as "Control 0.0.344.1879 (FINAL_release)"
        The JSON has a mapping of parsed names to nice names, allowing you to
        rename a game's folder, or have multiple names go into the same folder, etc.

        :param name: The game name parsed from the file
        :type name: String
        """

        return self.mapping.get(name, name)

if __name__ == "__main__":
    main()
