#! /usr/bin/python

# Requires:
# sudo apt-get install python-notify

# OPTIONAL: Anything to do with PATHS is only necessary if you have
# album cover/art image files and want to see those displayed as the
# optional component in notifications.

import sys
import os
import pynotify

if len(sys.argv) == 1:
    print "Usage: ./notify.py <artist> <album>"
    sys.exit(1)

if not pynotify.init("MPD status"):
    sys.exit(1)

# In case you have additional folders such as for FLAC that might
# otherwise introduce dupulicate audio tracks, just list the subset of
# paths to search here:
HOME = os.environ['HOME']
PATHS = (HOME+"/Music/mp3/",
         HOME+"/Music/generated-mp3/")

artist = "unknown artist"
album = "unknown album"
song = "unknown song"
if len(sys.argv) > 1: artist = sys.argv[1]
if len(sys.argv) > 2: album = sys.argv[2]
if len(sys.argv) > 3: song = sys.argv[3]

file_path = None
if PATHS:
    cover_path = artist + "-" + album + "/cover"
    for ext in (".png", ".jpg", ".jpeg", ".gif", ".svg"):
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
    print file_path
    notify = pynotify.Notification(artist+":\n"+album, song, "file://" + file_path)
else:
    notify = pynotify.Notification(artist+":\n"+album, song)

notify.show()
