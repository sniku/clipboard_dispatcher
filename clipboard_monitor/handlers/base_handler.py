from abc import abstractmethod
import dbus


class BaseHandler(object):
    """
    Subclass this class to implement your handler
    """

    handler = None

    @abstractmethod
    def init_handler(self, *args, **kwargs):
        pass

    def _init_handler(self):
        try:
            BaseHandler.handler = self.init_handler()
        except Exception as e:
            print e

    @abstractmethod
    def send_message(self, *args, **kwargs):
        pass


    def dispatch_message(self, *args):
        #print self.handler
        try:
            self.send_message(*args)
        except dbus.exceptions.DBusException as e:
            # failed to send. Try to initialize the handler again
            self.init_handler()
            try: # try again
                self.send_message(*args)
            except Exception as e:
                print e
        except Exception as e:
            print e

    def __init__(self):
        self._init_handler()