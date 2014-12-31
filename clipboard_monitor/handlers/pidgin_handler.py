import dbus

def send_message(contact, msg):
    print u'Sending "{}" to {}'.format(msg, contact)
    bus = dbus.SessionBus()
    obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
    purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")

    account = purple.PurpleAccountsGetAllActive()[0]

    conv = purple.PurpleConversationNew(1, account, contact)

    if conv:
        purple.PurpleConvImSend(purple.PurpleConvIm(conv), msg)
    else:
        print "no converstion created :-( Pidgin disconnected?"

