
"""
A GUI interface using jbaiter's pyomxplayer to control omxplayer

INSTALLATION
***
  *  TBOPlayer requires avconv, youtube-dl, and also the python libraries requests, gobject2, gtk2, pexpect and ptyprocess to be installed in order to work.
  *
  *  -------------------------
  *
  *  To install TBOPlayer and all required libraries, you can simply use the following command from tboplayer directory:
  *
  *      chmod +x setup.sh 
  *      ./setup.sh
  *
  *  -------------------------
  *
  *  See README.md file for more details on installation
  *  
  
OPERATION
Menus
====
 Track - Track - add tracks (for selecting multiple tracks, hold ctrl when clicking) or directories or URLs, edit or remove tracks from the current playlist
 Playlist - save the current playlist or open a saved one or load youtube playlist
 OMX - display the track information for the last played track (needs to be enabled in options)
 Options -
    Audio Output - play sound to hdmi or local output, auto does not send an audio option to omxplayer.
    Mode - play the Single selected track, Repeat the single track, rotate around the Playlist starting from the selected track, randomly play a track from the Playlist.
    Initial directory for tracks - where Add Track starts looking.
    Initial directory for playlists - where Open Playlist starts looking
    Enable subtitles
    OMXPlayer location - path to omxplayer binary
    OMXplayer options - add your own (no validation so be careful)
    Download from Youtube - defines whether to download video and audio or audio only from Youtube (other online video services will always be asked for "video and audio")
    Download actual media URL [when] - defines when to extract the actual media from the given URL, either upon adding the URL or when playing it
    Youtube video quality - lets you choose between "small", "medium" and "high" qualities (Youtube only feature)
    youtube-dl location - path to youtube-dl binary
    Start/End track paused - Pauses the track both in the beginning and in the end of the track
    Autoplay on start up - If TBOPlayer has just been opened and has some file in the playlist, automatically satrt playing the first file in the list
    Forbid windowed mode - if enabled will make videos always show in full screen, disabling the video window mode and video progress bar - useful if you're using tboplayer through a remote desktop
    Debug - prints some debug text to the command line

  *  See README.md file for more details on operation in the OPERATION section

TODO (maybe)
--------
sort out black border around some videos
gapless playback, by running two instances of pyomxplayer
read and write m3u and pls playlists


PROBLEMS
---------------
I think I might have fixed this but two tracks may play at the same time if you use the controls quickly, you may need to SSH in form another computer and use top -upi and k to kill the omxplayer.bin

"""

import sys
import os
import dbus
from gi.repository import GLib

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/lib')

from dbusinterface import TBOPlayerDBusInterface
from tboplayer import TBOPlayer

# ***************************************
# MAIN
# ***************************************

if __name__ == "__main__":
    dbusif_tboplayer = None
    try:
        bus = dbus.SessionBus()
        bus_object = bus.get_object(TBOPLAYER_DBUS_OBJECT, TBOPLAYER_DBUS_PATH, introspect = False)
        dbusif_tboplayer = dbus.Interface(bus_object, TBOPLAYER_DBUS_INTERFACE)
    except:
        pass

    if dbusif_tboplayer is None:
        bplayer = TBOPlayer()
        TBOPlayerDBusInterface(bplayer)
        glib_loop = GLib.MainLoop()
        def refresh_player():
            try:
                bplayer.root.update()
                GLib.timeout_add(66, refresh_player)
            except:
                glib_loop.quit()
        def start_glib():
            glib_loop.run()
        GLib.timeout_add(66, refresh_player)
        bplayer.root.after(65, start_glib)
        bplayer.root.mainloop()
    elif len(sys.argv[1:]) > 0:
        dbusif_tboplayer.openFiles(sys.argv[1:])
    exit()

