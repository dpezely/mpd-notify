#! /bin/bash
NOTIFY=~/bin/mpd-notify/notify.py
current=$(mpc -f "%artist% ~ %album% ~ %title%" current)
if [ -z "$current" ]; then
    $NOTIFY "MPD playback stopped" "$(date +'%I:%M %p')"
else
    artist=$(echo $current | sed 's/ ~ .* ~ .*$//')
    album=$(echo $current | sed 's/^[^~]* ~ //' | sed 's/ ~ [^~]*$//')
    song=$(echo $current | sed 's/^.* ~ .* ~ //')
    $NOTIFY "$artist" "$album" "$song"
fi
