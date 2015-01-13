#!/usr/bin/python
# -*- coding: utf8 -*-

import json
import subprocess
from handlers import SkypeClient, PidginClient
from time import sleep
from dbus.mainloop.glib import DBusGMainLoop



def handle_dispatched_object(dispatched_obj):
    if dispatched_obj['action']['type'] == 'pidgin':
        PidginClient().dispatch_message(dispatched_obj['action']['target'], dispatched_obj['payload']['content'])
    elif dispatched_obj['action']['type'] == 'skype':
        SkypeClient().dispatch_message(dispatched_obj['action']['target'], dispatched_obj['payload']['content'])
    else:
        print "unknown action type", dispatched_obj['action']['type'], 'skipping'
        print dispatched_obj


def run_daemon():
    last_clip = None
    DBusGMainLoop(set_as_default=True)

    while True:
        sleep(1)

        try:
            clip = subprocess.Popen(["timeout", "5", "xclip", "-selection", "clipboard", "-o"], stdout=subprocess.PIPE).communicate()[0]
        except:
            # some kind of IO exception - ignore.
            continue

        if last_clip is None:
            print "first run"
            pass
        elif last_clip == clip:
            #print "no change"
            pass
        else:
            print "detected change in the clipboard"
            try:
                dispatched_obj = json.loads(clip)
            except ValueError as e:
                # not a json string - some other content - skip
                pass
            else:
                #print dispatched_obj
                if type(dispatched_obj) is dict and 'format' in dispatched_obj and dispatched_obj['format'] == 'clipboard_dispatcher':
                    handle_dispatched_object(dispatched_obj)
                else:
                    # Some other json content - skip
                    pass

        last_clip = clip


if __name__ == '__main__':
    run_daemon()
