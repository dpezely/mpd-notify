#! /bin/bash
set -e
NOTIFY=~/bin/mpd-notify/notify.py
CACHE=${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/mpc-current
while true
do
    # The idleloop command generates two lines of identical output,
    # so capture one to a cache to avoid duplicate notifications
    mpc idleloop player | while read
    do
	current=$(mpc -f "%artist% ~ %album% ~ %title%" current)
	if [[ -z "$current" ]]; then
            $NOTIFY "MPD playback stopped" "$(date +'%I:%M %p')"
	elif [[ ! -f $CACHE ]] || [[ "$current" != "$(cat $CACHE)" ]]; then
	    artist=$(echo $current | sed 's/ ~ .* ~ .*$//')
	    album=$(echo $current | sed 's/^[^~]* ~ //' | sed 's/ ~ [^~]*$//')
	    song=$(echo $current | sed 's/^.* ~ .* ~ //')
	    echo $current > $CACHE
            $NOTIFY "$artist" "$album" "$song"
	fi
    done
    sleep 2
done
