import dbus
from base_handler import BaseHandler


class PidginClient(BaseHandler):

    def init_handler(self):
        bus = dbus.SessionBus()
        obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
        return dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")

    def send_message(self, contact, message):
        message = message.encode("utf8")
        account = self.handler.PurpleAccountsGetAllActive()[0]
        conv = self.handler.PurpleConversationNew(1, account, contact)
        if conv:
            self.handler.PurpleConvImSend(self.handler.PurpleConvIm(conv), message)
        else:
            print "no converstion created :-( Pidgin disconnected?"

