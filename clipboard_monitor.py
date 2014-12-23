#!/usr/bin/python
# -*- coding: utf8 -*-
import json
import subprocess
from time import sleep
import dbus

last_clip = None

def send_pidgin_message(contact, msg):
    print u'Sending "{}" to {}'.format(msg, contact)
    bus = dbus.SessionBus()
    obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
    purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")

    account = purple.PurpleAccountsGetAllActive()[0]

    conv = purple.PurpleConversationNew(1, account, contact)

    # msg = "Chrome dispatcher plugin test: " + msg

    if conv:
        purple.PurpleConvImSend(purple.PurpleConvIm(conv), msg)
    else:
        print "no converstion created :-( Pidgin disconnected?"


while True:

    clip = subprocess.Popen(["xclip","-selection", "clipboard", "-o"], stdout=subprocess.PIPE).communicate()[0]

    #http://stackoverflow.com/questions/764360/a-list-of-string-replacements-in-python
    # mapping = { "'":'', ',':'', '"':'', ';':'', '(':'', ')':'', '.':'', '-':' '}
    # for k, v in mapping.iteritems():
    #     tag = tag.replace(k, v)

    #Camelcase, remove spaces, and append Caesar tag
    #tag=tag.title().replace(' ','')+"_"

    # print clip

    sleep(1)

    if last_clip is None:
        print "first run"
        pass
    elif last_clip == clip:
        print "no change"
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
                send_pidgin_message(dispatched_obj['action']['target'], dispatched_obj['payload']['content'])
            else:
                # Some other json content - skip
                pass

    last_clip = clip



