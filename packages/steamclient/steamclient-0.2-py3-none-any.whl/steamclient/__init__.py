import glob
import os
import re
import shutil
import winreg
import zlib

import requests

# Find the Steam install directory or raise an error
try: # 32-bit
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Valve\\Steams")
except FileNotFoundError:
    try: # 64-bit
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Wow6432Node\\Valve\\Steam")
    except FileNotFoundError as e:
        print("Failed to find Steam Install directory")
        raise(e)
STEAM_PATH = winreg.QueryValueEx(key, "InstallPath")[0]


class Game():
    def __init__(self, user_id, id, name):
        self.user_id = user_id
        self.id = id
        self.name = name
        
    def __repr__(self):
        return f"<Game {self.name} ({self.id})>"

    @property
    def logo(self):
        """ Returns path to logo on disk (might not exist) """
        return f"{STEAM_PATH}\\userdata\\{self.user_id}\\config\\grid\\{self.id}_logo.png"

    @property
    def grid(self):
        """ Returns path to cover art on disk (might not exist) """
        return f"{STEAM_PATH}\\userdata\\{self.user_id}\\config\\grid\\{self.id}p.png"

    @property
    def hero(self):
        """ Returns path to banner on disk (might not exist) """
        return f"{STEAM_PATH}\\userdata\\{self.user_id}\\config\\grid\\{self.id}_hero.png"
        
    def set_logo(self, filepath=None, url=None):
        """
        Copies an image to the custom artwork directory.
        Image can be either a file or a URL.

        :param filepath: File on disk
        :param url: URL of image.
        """
        if filepath is not None:
            shutil.copyfile(filepath, self.logo)
        elif url is not None:
            img = requests.get(url).content
            with open(self.logo, 'wb') as f:
                f.write(img)
    
    def set_grid(self, filepath=None, url=None):
        """
        Copies an image to the custom artwork directory.
        Image can be either a file or a URL.

        :param filepath: File on disk
        :param url: URL of image.
        """
        if filepath is not None:
            shutil.copyfile(filepath, self.grid)
        elif url is not None:
            img = requests.get(url).content
            with open(self.grid, 'wb') as f:
                f.write(img)

    def set_hero(self, filepath=None, url=None):
        """
        Copies an image to the custom artwork directory.
        Image can be either a file or a URL.

        :param filepath: File on disk
        :param url: URL of image.
        """
        if filepath is not None:
            shutil.copyfile(filepath, self.hero)
        elif url is not None:
            img = requests.get(url).content
            with open(self.hero, 'wb') as f:
                f.write(img)

class Shortcut(Game):
    def __init__(self, user_id, entry_id, name, exe, start_dir,
                 icon="", shortcut_path="", launch_options="",
                 hidden=False, allow_desktop_config=True, allow_overlay=True,
                 openvr=False, devkit=False, devkit_game_id="", 
                 last_play_time=b'\x00\x00\x00\x00', tags=[]):
        self._id = None # calculated below
        self.user_id = user_id
        self.entry_id = entry_id
        self.name = name
        self.exe = exe
        self.start_dir = start_dir
        self.icon = icon
        self.shortcut_path = shortcut_path
        self.launch_options = launch_options
        self.hidden = hidden
        self.allow_desktop_config = allow_desktop_config
        self.allow_overlay = allow_overlay
        self.openvr = openvr
        self.devkit = devkit
        self.devkit_game_id = devkit_game_id
        self.last_play_time = last_play_time
        self.tags = tags
    
    def __repr__(self):
        return f"<Shortcut {self.entry_id}: {self.name}>"

    def info(self):
        print(f"Shortcut {self.entry_id}")
        print(f"    id: {self.id}")
        print(f"    name: {self.name}")
        print(f"    exe: {self.exe}")
        print(f"    start_dir: {self.start_dir}")
        print(f'    icon: "{self.icon}"')
        print(f'    shortcut_path: "{self.shortcut_path}"')
        print(f'    launch_options: "{self.launch_options}"')
        print(f"    hidden: {self.hidden}")
        print(f"    allow_desktop_config: {self.allow_desktop_config}")
        print(f"    allow_overlay: {self.allow_overlay}")
        print(f"    openvr: {self.openvr}")
        print(f"    devkit: {self.devkit}")
        print(f"    devkit_game_id: {self.devkit_game_id}")
        print(f"    last_play_time: {self.last_play_time}")
        print(f"    tags: {self.tags}")

    @property
    def id(self):
        if self._id is None:
            s = self.exe + self.name
            self._id = str((zlib.crc32(s.encode()) & 0xffffffff) | 0x80000000)
        return self._id

class User():
    """ User object to store the ID """
    def __init__(self, id):
        """
        Construct a new User object

        :param id: The ID of the user
        """
        self.id = int(id)
        self._shortcuts = None
        self._games = None
    
    def __repr__(self):
        return f"<User {self.id}>"

    @property
    def shortcuts(self):
        """ Returns a list of Shortcut objects """
        return get_shortcuts(self.id)

    def games(self, libraries=None):
        """ Returns a list of Shortcut objects """
        return get_games(self.id, libraries)

def _read_id(f):
    """
    Helper function for decoding binary files.
    Reads the entry ID from the shortcut entry.
    
    :param f: Open file handler
    :returns: An int
    """
    buffer = b""
    while True:
        byte = f.read(1)
        if byte == b'\x00' or byte == b'':
            break
        buffer += byte
    return int(buffer.decode())

def _read_str(f):
    """
    Helper function for decoding binary files.
    Reads bytes up until the end of string delimiter or end of file.
    
    :param f: Open file handler
    :returns: A string
    """
    buffer = b""
    delimiter = b'\x00'
    while True:
        byte = f.read(1)
        if byte == delimiter or byte == b'':
            break
        buffer += byte
    return buffer

def _read_bool(f):
    """
    Helper function for decoding binary files.
    
    :param f: Open file handler
    :returns: A boolean
    """
    delimiter = b'\x00\x00\x00'
    b = f.read(1)
    assert(f.read(3) == delimiter)
    return True if b == b'\x01' else False

def _read_list(f):
    """
    Helper function for decoding binary files.
    Reads bytes up until the delimiter or end of file.
    
    :param f: Open file handler
    :returns: A list of strings
    """
    contents = []

    while True:
        byte = f.read(1)
        if byte == b'\x01':
            index = _read_str(f)
            contents.append(_read_str(f))
        elif byte == b'\x08':
            byte = f.read(1)
            if byte == b'\x08':
                break
            else:
                raise(Exception("_read_list() expected b'\\x08', read {byte}"))

    return contents

def get_games(user_id, libraries=None):
    """
    Get all of a user's installed games

    :param user_id: the user's ID number
    :param libraries: list of file paths, if None is given - they are all loaded 
    :returns: a list of Game objects
    """
    if libraries is None:
        libraries = get_libraries()

    games = []
    for library in libraries:
        pattern = library + "\\steamapps\\appmanifest_*.acf"
        app_manifests = glob.glob(pattern)
        for manifest in app_manifests:
            app_id = manifest.split('appmanifest_')[-1][:-4]
            name = "Unknown" # placeholder
            with open(manifest, 'r') as f:
                while True:
                    line = f.readline()
                    if '"name"' in line:
                        name = line.split('"')[3]
                        break
                    if line == "":
                        break
            games.append(Game(user_id, app_id, name))
    games.sort(key=lambda x: x.name)
    return games

def get_libraries():
    """ 
    Get a list of paths to all Steam Libraries from
    Steam\\steamapps\\libraryfolders.vdf

    :returns: a list of file paths
    """
    libraries = [STEAM_PATH]
    with open(f"{STEAM_PATH}\\steamapps\\libraryfolders.vdf", 'r') as f:
        lf = f.read()
        libraries.extend([fn.replace("\\\\", "\\") for fn in
            re.findall(r'^\s*"\d*"\s*"([^"]*)"', lf, re.MULTILINE)])
    return libraries

def get_shortcuts(user_id):
    """
    Get a user's non-steam Shortcuts from their shortcuts.vdf

    :param user_id: the user's ID number
    :returns: a list of Shortcut objects
    """

    shortcuts_vdf = f"{STEAM_PATH}\\userdata\\{user_id}\\config\\shortcuts.vdf"
    shortcuts = []
    with open(shortcuts_vdf, 'rb') as f:
        header = f.read(11)
        expected = b'\x00shortcuts\x00'
        if header != expected:
            raise Exception(f"Error: first 10 bytes of {shortcuts_vdf} ({header}) are not {expected}")

        # Loop through each shortcut entry
        while True:
            # Check if this is the end of the list
            byte = f.read(1)
            if byte == b'\x08':
                assert f.read(1) ==  b'\x08'
                break

            shortcut = {}
            
            shortcut['entryid'] = _read_id(f)

            # Loop through each variable in the entry
            while True:

                # Data type of the variable
                datatype = f.read(1)
                if datatype == b'\x00': # List
                    key = _read_str(f).decode().lower()
                    val = _read_list(f)
                    shortcut[key] = val
                    break # shortcut entry ends with a list
                elif datatype == b'\x01': # String
                    key = _read_str(f).decode().lower()
                    val = _read_str(f).decode()
                elif datatype == b'\x02': # Boolean
                    key = _read_str(f).decode().lower()
                    if key == "lastplaytime": # this key is weird - only 4 bytes
                        val = f.read(4)
                    else:
                        val = _read_bool(f)
                else:
                    print(datatype)
                    print(f.read(25))
                    raise(Exception(f"Unknown data type: {datatype}"))
                
                #print(f"datatype {datatype} setting {key} to {val}")
                shortcut[key] = val
            
            #print(f"Shortcut dict: {shortcut}")
            s = Shortcut(user_id=user_id,
                         entry_id=shortcut['entryid'], 
                         name=shortcut['appname'],
                         exe=shortcut['exe'],
                         start_dir=shortcut['startdir'],
                         icon=shortcut['icon'],
                         shortcut_path=shortcut['shortcutpath'],
                         launch_options=shortcut['launchoptions'],
                         hidden=shortcut['ishidden'],
                         allow_desktop_config=shortcut['allowdesktopconfig'],
                         allow_overlay=shortcut['allowoverlay'],
                         openvr=shortcut['openvr'],
                         devkit=shortcut['devkit'],
                         devkit_game_id=shortcut['devkitgameid'],
                         last_play_time=shortcut['lastplaytime']
                         )
            shortcuts.append(s)

    return shortcuts

def get_users():
    """
    Get all users that have logged in.

    :returns: a list of User objects (sorted by last login date)
    """
    path = f"{STEAM_PATH}\\userdata\\*"
    files = glob.glob(path)
    files.sort(key=os.path.getmtime, reverse=True)
    return [User(id=os.path.basename(f)) for f in files]
