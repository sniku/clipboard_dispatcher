# -*- coding: utf8 -*-

# implemented using http://vmiklos.hu/bitlbee-skype/public_api_ref.html

def send_message(skype_dbus_handler, skype_name, message):
    message = message.encode("utf8")

    chat = skype_dbus_handler.send("CHAT create {}".format(skype_name))
    chat_id = chat.split()[1]
    skype_dbus_handler.send("OPEN CHAT {}".format(chat_id))
    msg = "CHATMESSAGE {} {}".format(chat_id, message)
    skype_dbus_handler.send(msg)


# send_message("sad.manikin", u"unicode test öäþåÞŁÖĄŻĘĄ".encode("utf8"))