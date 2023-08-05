"""
    VLC HTTP client it handles all communications with VLC's built-in http server. All VLC HTTP accepted commands are in
    their own methods. Each method has comments describing what that command does (based on the given documentation from
    the VLC developers) as well as the original command (some commands are given underscores to become more readable).
    Some methods utilize commands that aren't documented yet hardcoded in the HTTP mini server.

    VLC's Documentation:
        https://github.com/videolan/vlc/blob/master/share/lua/http/requests/README.txt
    VLC's HTTP Server Source code (at commands):
        https://github.com/videolan/vlc/blob/master/share/lua/intf/modules/httprequests.lua#L70

    Version:
        0.9.0
    License:
        BSD Simplified
    Notes:
        1. When executing a command the Response will have the status of VLC in it's response body if authentication
         succeeds this also means if you handled the command wrongly it won't respond with any issues.
    Authors:
        Dylan Hackworth <https://github.com/dylhack>
"""
import http.client

import requests

# All endpoints are in the requests directory of VLC's http module. See the GitHub for all the default endpoints
# https://github.com/videolan/vlc/tree/master/share/lua/http/requests
ENDPOINTS = {
    "status": "/requests/status.json",
    "playlist": "/requests/playlist.json",
    "commands": "/requests/status.json"
}


class Client:
    def __init__(self, address, port, password):
        self.address = address
        self.port = port
        self.auth = ('', password)
        self.connection = http.client.HTTPConnection(address, port)

    # Endpoint methods
    def get_status(self):
        """ Gets the status.json endpoint.

        :return: VLCStatus
        """
        response = self._request(ENDPOINTS['status'])
        # text/plain because.. https://github.com/videolan/vlc/blob/master/share/lua/intf/http.lua#L43
        if response.status_code == 200 and response.headers['content-type'] == 'text/plain':
            return response.json()
        else:
            raise response

    def get_playlist(self):
        """ Gets the playlist.json endpoint.

        :return: Response
        """
        response = self._request(ENDPOINTS['playlist'])
        # text/plain because.. https://github.com/videolan/vlc/blob/master/share/lua/intf/http.lua#L43
        if response.status_code == 200 and response.headers['content-type'] == 'text/plain':
            return response.json()
        else:
            raise response

    # Command methods
    def add_subtitle(self, uri):
        """ "add subtitle to currently playing file"
        command: addsubtitle

        :param uri: string
        :return: Response
        """
        return self.command('addsubtitle', ['val=%s' % uri])

    def aspect_ratio(self, new_ratio):
        """ "set aspect ratio. Must be one of the following values. Any other value will reset aspect ratio to default"
        command: aspectratio

        :param new_ratio: string
        :return: Response
        """
        return self.command('aspectratio', ['val=%s' % new_ratio])

    def audio_delay(self, delay_in_seconds):
        """ "set audio delay"
        command: audiodelay

        :param delay_in_seconds: integer
        :return: Response
        """
        return self.command('audiodelay', ['val=%d' % delay_in_seconds])

    def audio_track(self, val):
        """ "select the audio track (use the number from the stream)"
        command: audio_track


        :param val: string
        :return: Response
        """
        return self.command("audio_track", ['val=%s' % val])

    def chapter(self, val):
        """ "select the chapter"
        command: chapter

        :param val: string
        :return: Response
        """
        return self.command("chapter", ["val=%s" % val])

    def equalizer(self, band, val):
        """ "set the gain for a specific band"
        command: equalizer

        :param band: string
        :param val: integer
        :return: Response
        """
        if -20 <= val <= 20:  # ..."gain in dB, must be >=-20 and <=20"
            return self.command("equalizer", ["band=%s" % band, "val"])
        else:
            raise Exception("Val must be greater than -20 and less than 20.")

    def enable_eq(self, val):
        """ Enable the equalizer
        " 0 --  disables the equalizer"
        " 1 --  enables the equalizer"
        command: enableeq

        :param val: integer (1 or 0) 0: off, 1: on.
        :return: Response
        """
        if val == 0 or val == 1:
            return self.command('enableeq', ['val=%d' % val])
        else:
            raise Exception("Val must be equal to 0 or 1.")

    def pl_force_pause(self):
        """ "pause playback, do nothing if already paused"
        command: pl_forcepause

        :return: Response
        """
        return self.command('pl_forcepause')

    def pl_force_resume(self):
        """ "resume playback if paused, else do nothing"
        command: pl_forceresume

        :return: Response
        """
        return self.command('pl_forceresume')

    def fullscreen(self):
        """ "toggle fullscreen"
        command: fullscreen

        :return: Response
        """
        return self.command('fullscreen')

    def key(self, val):
        """ UNDOCUMENTED. Utilizes hot keys
        reference: https://github.com/videolan/vlc/blob/master/share/lua/intf/modules/httprequests.lua#L153
        command: key

        :param val: string
        :return: Response
        """
        return self.command('key', ['val=%s' % val])

    def in_enqueue(self, uri):
        """ add <uri> to playlist
        command: in_enqueue

        :param uri: string
        :return: Response
        """
        return self.command('in_enqueue', ['val=%s' % uri])

    def in_play(self, uri):
        """ "add <uri> to playlist and start playback"
        command: in_play

        :param uri: string
        :return: Response
        """
        return self.command('in_play', ['val=%s' % uri])

    def pl_play(self, media_id=None):
        """ "play playlist item <id>. If <id> is omitted, play last active item"
        command: pl_play

        :param media_id: integer
        :return: Response
        """
        if media_id is None:
            return self.command('pl_play')
        else:
            return self.command('pl_play', ['id=%d' % media_id])

    def pl_pause(self, media_id=None):
        """ "toggle pause. If current state was 'stop', play item <id>, if no <id> specified, play current item.
             If no current item, play 1st item in the playlist"
        command: pl_pause

        :param media_id: integer
        :return: Response
        """
        if media_id is None:
            return self.command('pl_pause')
        else:
            return self.command('pl_pause', ['id=%d' % media_id])

    def preamp(self, value_in_db):
        """ "sets the preamp value, must be >=-20 and <=20"
        command: preamp

        :param value_in_db: integer (>=-20 and <=20)
        :return: Response
        """
        if -20 <= value_in_db <= 20:
            return self.command('preamp', ['val=%d' % value_in_db])
        else:
            raise Exception("Value in db must be greater than -20 and less than 20.")

    def pl_delete(self, media_id):
        """ "delete item <id> from playlist"
        command: pl_delete
        NOTE: pl_delete is completely UNSUPPORTED

        :param media_id: integer
        :return: Response
        """
        return self.command('pl_delete', ['id=%d' % media_id])

    def pl_empty(self):
        """ empty playlist
        command: pl_empty

        :return: Response
        """
        return self.command('pl_empty')

    def pl_loop(self):
        """ "toggle loop" (as in current playlist)
        command: pl_loop

        :return: Response
        """
        return self.command('pl_loop')

    def pl_next(self):
        """ "jump to next item"
        command: pl_next

        :return: Response
        """
        return self.command('pl_next')

    def pl_previous(self):
        """ "jump to previous item"
        command: pl_previous

        :return: Response
        """
        return self.command('pl_previous')

    def pl_random(self):
        """ "toggle random playback"
        command: pl_random

        :return: Response
        """
        return self.command('pl_random')

    def pl_repeat(self):
        """ "toggle repeat" (as in current playing media)
        command: pl_repeat

        :return: Response
        """
        return self.command('pl_repeat')

    def pl_sd_add(self, val):
        """ "enable services discovery module <val>"
        command: pl_sd_add

        :param val: string
        :return: Response
        """
        return self.command('pl_sd_add', ['val=%s' % val])

    def pl_sd_remove(self, val):
        """ "disable services discovery module <val>"
        command: pl_sd_remove

        :param val: string
        :return:
        """
        return self.command('pl_sd_remove', ['val=%s' % val])

    def pl_sort(self, sort_mode, sort_id=0):
        """ "sort playlist using sort mode <val> and order <id>"
        command: pl_sort

        "If id=0 then items will be sorted in normal order, if id=1 they will be sorted in reverse order
        A non exhaustive list of sort modes:
        - 0 Id
        - 1 Name
        - 3 Author
        - 5 Random
        - 7 Track number "

        :return: Response
        """
        if sort_id == 0 or sort_id == 1:
            if (0 <= sort_mode >= 7) and (sort_mode != 0 and sort_mode % 2 == 0):
                self.command('pl_sort', ['id=%d' % sort_id, 'val=%d' % sort_mode])
            else:
                raise Exception("An invalid sort_mode was provided.")
        else:
            raise Exception("An invalid sort_id was provided. (sort_id == 0 or sort_id == 1)")

    def pl_stop(self):
        """ "stop playback"
        command: pl_stop

        :return: Response
        """
        return self.command('pl_stop')

    def rate(self, new_playback_rate):
        """ "set playback rate. must be > 0"
        command: rate

        :param new_playback_rate: integer
        :return: Response
        """
        if new_playback_rate > 0:
            self.command('rate', ['val=%d' % new_playback_rate])
        else:
            raise Exception('new_playback_rate must be grater than zero.')

    def seek(self, val):  # TODO: Accept different forms of values
        """ "seek to <val>"
        command: seek
        Allowed values are of the form:
            [+ or -][<int><H or h>:][<int><M or m or '>:][<int><nothing or S or s or ">]
            or [+ or -]<int>%
            (value between [ ] are optional, value between < > are mandatory)
        examples:
            1000 -> seek to the 1000th second
            +1H:2M -> seek 1 hour and 2 minutes forward
            -10% -> seek 10% back

        :param val: string
        :return: Response
        """
        return self.command('seek', ['val=%s' % val])

    def set_preset(self, preset_id):
        """ "set the equalizer preset as per the id specified "
        command: setpreset

        "<Displays the equalizer band gains.
        Band 0: 60 Hz, 1: 170 Hz, 2: 310 Hz, 3: 600 Hz, 4: 1 kHz,
        5: 3 kHz, 6: 6 kHz, 7: 12 kHz , 8: 14 kHz , 9: 16 kHz

        <Display the list of presets available for the equalizer"

        :return: Response
        """
        return self.command('setpreset', ['val=%d' % preset_id])

    def snapshot(self):
        """ UNDOCUMENTED (Executes snapshot functionality on VLC)
        command: snapshot

        :return: Response
        """
        return self.command('snapshot')

    def sub_delay(self, delay_in_seconds):
        """
        command: subdelay

        :return: Response
        """
        return self.command('subdelay', ['val=%d' % delay_in_seconds])

    def subtitle_track(self, val):
        """ "select the subtitle track (use the number from the stream)"
        command: subtitle_track

        :param val: integer
        :return: Response
        """
        return self.command('subtitle_track', ['val=%d' % val])

    def title(self, val):
        """ "select the title"
        command: title

        :param val: string
        :return: Response
        """
        return self.command('title', ['val=%s' % val])

    def video_track(self, val):
        """ "select the video track (use the number from the stream)"
        command: video_track

        :param val: integer
        :return: Response
        """
        return self.command('video_track', ['val=%d' % val])

    def volume(self, val):  # TODO: Account for +/- relative values
        """ "set volume level to <val> (can be absolute integer, percent or +/- relative value)"
        command: volume

        :param val: integer
        :return: Response
        """
        return self.command('volume', ['val=%d' % val])

    def command(self, command, query=None):
        """ Sends an HTTP request to execute a command. The VLCStatus will return if succeeded if it runs into an
        authentication error nothing will be returned.

        :param command: string
        :param query: string[] (Example: ["play=url", "key=value"])
        :return: Response
        """
        if query is None:
            query = []
        url = "http://%s:%d%s?command=%s" % (self.address, self.port, ENDPOINTS['commands'], command)
        for argument in query:
            url += '&%s' % argument
        response = requests.get(url, auth=self.auth)
        return response

    # Utility methods
    def _request(self, endpoint):
        """ A private method for sending requests to VLC's HTTP server.

        :param endpoint:
        :return: Response
        """
        url = 'http://%s:%d%s' % (self.address, self.port, endpoint)
        response = requests.get(url, auth=self.auth)
        return response
