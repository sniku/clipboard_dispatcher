#!/usr/bin/python
# -*- coding: utf8 -*-
import dbus

bus = dbus.SessionBus()
obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")

current = purple.PurpleSavedstatusGetType(purple.PurpleSavedstatusGetCurrent())
status = purple.PurpleSavedstatusNew("", current)

purple.PurpleSavedstatusSetMessage(status, "dbus test 2")
purple.PurpleSavedstatusActivate(status)
#im = purple.PurpleGetIms()[0]
#purple.PurpleGetConversations()
#purple.PurpleConvImSend(im, "dbus test to rzepak")
#purple.PurpleGetIms()

account = purple.PurpleAccountsGetAllActive()[0]

conv = purple.PurpleConversationNew(1, account, "rzepak@gmail.com")

convs = purple.PurpleGetConversations()
#
#
if conv:
    purple.PurpleConvImSend(purple.PurpleConvIm(conv), u"unicode test łöäåżąśęÖÅĄ".encode("utf8"))
else:
    print "no converstion created :-( Pidgin disconnected?"