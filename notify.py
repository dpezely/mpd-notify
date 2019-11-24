#! /usr/bin/env python3

# Requires:
# sudo apt-get install python3-notify2

# OPTIONAL: Anything to do with PATHS is only necessary if you have
# album cover/art image files and want to see those displayed as the
# optional component in notifications.

import sys
import os
import re
import notify2 as pynotify

# If `mpc` isn't in your $PATH, specify fully qualified path here:
MPC = "mpc"

# In case you have additional folders such as for FLAC that might
# otherwise introduce dupulicate audio tracks, just list the subset of
# paths to search here:
HOME = os.environ['HOME']
PATHS = (HOME+"/Music/mp3/",
         HOME+"/Music/generated-mp3/")

ALBUM_COVER_FILE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".svg")

if not pynotify.init("MPD status"):
    print("Unable to initialize dbus Notifications")
    sys.exit(1)

RS='^'                          # ASCII Record Separator 0x5e 
CURRENT = f'''{MPC} -f "%artist%{RS}%album%{RS}%title%{RS}" status current'''
LOOPER = f'''{MPC} idleloop player'''

SONG_NUMBER_REGEX = re.compile(r'''#\d{1,}/\d{1,} ''')

def mpc_loop():
    while True:
        process_status(get_status())
        with os.popen(LOOPER) as f:
            f.read(7)           # Consumes "player\n"
            process_status(get_status())

def mpc_once():
    process_status(get_status())

def get_status():
    current = None
    with os.popen(CURRENT) as f:
        current = f.read()
    return current

def process_status(current):
    if current is None:
        notify = pynotify.Notifications("Unable to get status from MPD",
                                        "Probably misconfigured:\n"
                                        + sys.argv[0])
    elif current[:11] == "volume: n/a":
        notify = pynotify.Notification("MPD playback has stopped")
    else:
        artist, album, song, status = current.split(RS)
        duration = status.split('\n')[1]
        duration = SONG_NUMBER_REGEX.sub('', duration)
        file_path = None
        if PATHS:
            cover_path = artist + "-" + album + "/cover"
            for ext in ALBUM_COVER_FILE_EXTENSIONS:
                for path in PATHS:
                    attempt_path = path + cover_path + ext
                    if os.path.exists(attempt_path):
                        file_path = attempt_path
                        break
                    else:
                        attempt_path = path + cover_path + ext.upper()
                        if os.path.exists(attempt_path):
                            file_path = attempt_path
                            break
                if file_path:
                    break

        if file_path:
            notify = pynotify.Notification(artist+":\n"+album,
                                           song+"\n"+duration,
                                           "file://" + file_path)
        else:
            notify = pynotify.Notification(artist+":\n"+album,
                                           song+"\n"+duration)

    notify.show()

def run():
    if len(sys.argv) > 1 and (sys.argv[1] == '--repeat' or
                              sys.argv[1] == '-r'):
        try:
            mpc_loop()
        except KeyboardInterrupt:
            pass
    else:
        mpc_once()

if __name__ == '__main__':
    run()
