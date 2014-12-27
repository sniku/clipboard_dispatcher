#!/usr/bin/python
# -*- coding: utf8 -*-
import json
import subprocess
from handlers import skype_handler, pidgin_handler
from time import sleep
import dbus
import handlers.libs.skypelib as skype
from dbus.mainloop.glib import DBusGMainLoop

last_clip = None
DBusGMainLoop(set_as_default=True)

skype_dbus_handler = skype.SkypeInterface(dbus.SessionBus(), "PythonSkypeTest")

def handle_dispatched_object(dispatched_obj):
    if dispatched_obj['action']['type'] == 'pidgin':
        pidgin_handler.send_message(dispatched_obj['action']['target'], dispatched_obj['payload']['content'])
    elif dispatched_obj['action']['type'] == 'skype':
        skype_handler.send_message(skype_dbus_handler, dispatched_obj['action']['target'], dispatched_obj['payload']['content'])
    else:
        print "unknown action type", dispatched_obj['action']['type'], 'skipping'
        print dispatched_obj

while True:

    clip = subprocess.Popen(["xclip", "-selection", "clipboard", "-o"], stdout=subprocess.PIPE).communicate()[0]
    sleep(1)

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
            print dispatched_obj
            if 'format' in dispatched_obj and dispatched_obj['format'] == 'clipboard_dispatcher':
                print type(dispatched_obj['payload']['content'])
                handle_dispatched_object(dispatched_obj)
            else:
                # Some other json content - skip
                pass

    last_clip = clip



