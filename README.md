MPD Notification Scripts
========================

MPD is the Music Player Daemon <https://www.musicpd.org/>
which may be controlled via `mpc` at the shell command-line.

This trivial Bash script and companion Python program provide desktop
notifications via `dbus` on Linux to show current song as it changes.

It's a simple setup with minimal number of dependencies compared to more
full featured music players but is often all that's wanted; e.g., less
running, less to do for longer batter life on a laptop computer.

## Usage:

Get dependencies, on Debian/Ubuntu:

	sudo apt-get install mpd mpc python3 python3-notify2

Install into a subdirectory known by your $PATH environment variable, such as:

- `/usr/local/bin/`
- `~/bin/`

Revise music, playlists subdirectories:

	sudo vi /etc/mpd.conf
	sudo systemctl start mpd

Load music library:

	mpc update --wait
	mpc ls
	mpc load your_favourite_playlist

Start this script in background:

	./notify.py --repeat &

or

	./notify.py -r &
    
(See also Unix manual page for `nohup(1)`.)

Start playing music:

	mpc play

To see a notification sooner than later:

	mpc next

## Keyboard Shortcuts

If `mpd` is your primary music player, consider these keyboard shortcuts
available on many contemporary laptop computer keyboards.

System Settings -> Keyboard -> Shortcuts

- /usr/bin/mpc prev => Fn `<audio prev>`
- /usr/bin/mpc toggle => Fn `<audio play>`
- /usr/bin/mpc next => Fn `<audio next>`
- /usr/local/bin/notify.py => Fn `<audio status>`
