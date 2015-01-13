# -*- coding: utf8 -*-

# implemented using http://vmiklos.hu/bitlbee-skype/public_api_ref.html
import dbus
from base_handler import BaseHandler
import libs.skypelib as skype


class SkypeClient(BaseHandler):

    def init_handler(self, *args, **kwargs):
        return skype.SkypeInterface(dbus.SessionBus(), "PythonSkypeTest")

    def send_message(self, skype_name, message):

        message = message.encode("utf8")

        chat = self.handler.send("CHAT create {}".format(skype_name))
        chat_id = chat.split()[1]
        self.handler.send("OPEN CHAT {}".format(chat_id))
        msg = "CHATMESSAGE {} {}".format(chat_id, message)
        self.handler.send(msg)
