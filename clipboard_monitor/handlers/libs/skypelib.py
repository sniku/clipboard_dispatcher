#!/usr/bin/env python
# skype.py - A python interface to the Skype client
# Copyright (C) 2011 Trever Fischer <tdfischer@fedoraproject.org>
# Released under the terms of the LGPL
"""Python interface to the skype client API

The skype interface implements a text-based protocol over DBus.
To use this library, just create a SkypeInterface object:

    import skype
    import dbus

    # Skype will prompt the user, asking if they'll allow the "PythonSkypeTest" application access to the API
    # Constructor doesn't return until the user picks yes or no
    mySkype = skype.SkypeInterface(dbus.SessionBus(), "PythonSkypeTest")
    # Call the skype echo service
    mySkype.send("CALL test123")

The exciting bits are when you can listen for skype events and respond.
In order to do so, you need to extend the SkypeInterface class and implement
some object handlers.

    import skype
    import dbus
    import gobject
    from dbus.mainloop.glib import DBusGMainLoop

    class MySkypeInterface(skype.SkypeInterface):
        def __init__(self):
            super(MySkypeInterface, self).__init__(dbus.SessionBus(), "MySkypeInterface")

        def on_new_call(self, call):
            print "Got a new call between user and %s"%(call.partner_dispname)
            call.setUpdateHandler("status", self.on_call_status_change)

        def on_call_status_change(self, call, oldStatus):
            print "Call %r changed status from %s to %s"%(call, call.status, oldStatus)

    DBusGMainLoop(set_as_default = True)
    iface = MySkypeInterface()
    loop = gobject.MainLoop()
    loop.run()

The above example performs the following:

    * Initializes DBus to use the glib mainloop (needed for asynchronous property change notifications)
    * Registers with the Skype API
    * Implements a method to handle new call objects
    * Attaches a handler to any new calls, which gets called when the call's status changes
    * Prints out when the call status changes
    * Starts the glib mainloop

Complete documentation of objects and their properties is available at http://developer.skype.com/accessories

"""

__author__ = "Trever Fischer <tdfischer@fedoraproject.org>"
__version__ = "0.0.1"

import dbus.service
import dbus
import traceback
import logging
# For demo mode
from dbus.mainloop.glib import DBusGMainLoop
import gobject

_log = logging.getLogger("skype")

__all__ = ["SkypeMessage", "SkypeObject", "SkypeInterface"]

class SkypeMessage(object):
    """Represents the general structure of a skype API message"""
    def __init__(self, message):
        super(SkypeMessage, self).__init__()
        self.__raw = message
        args = message.split(" ")
        self.__command = args.pop(0)
        self.__args = args

    @property
    def raw():
        """The raw string"""
        return self.__raw

    @property
    def args():
        """Any and all arguments of the command"""
        return self.__args

    @property
    def command():
        """The command type of the message"""
        return self.__command

    def __str__(self):
        return self.raw

    def __repr__(self):
        return "<SkypeMessage %r>"%(self.raw)

class SkypeObject(object):
    """Represents an internal Skype object exposed via the interface
    
    Listen in on property updates via setUpdateHandler
    """
    def __init__(self, interface, typename, uid):
        super(SkypeObject, self).__init__()
        self.__iface = interface
        self.__type = typename
        self.__id = uid
        self.__values = {}
        self.__updateHandlers = {}

    @property
    def id(self):
        """The unique object identifier"""
        return self.__id

    @property
    def type(self):
        """The object type"""
        return self.__type

    def setUpdateHandler(self, propertyName, handler):
        """When the given property name is updated, the handler will be called.

        Handlers should have the following signature:
            handler(SkypeObject, oldvalue)
        """
        self.__updateHandlers[propertyName] = handler

    def refresh(self):
        """Refreshes all cached properties"""
        for name in self.__values:
            self.__update(name)

    def _update(self, msg):
        """Internal method. Updates properties given a SkypeMessage and calls update handlers"""
        name = msg.args[1].lower()
        oldValue = None
        value = ' '.join(msg.args[2:])
        if (name in self.__values):
            oldValue = self.__values[name]
        self.__values[name] = value
        if (not (oldValue is None) and not (oldValue == value) and (name in self.__updateHandlers) and not (self.__updateHandlers[name] is None)):
            self.__updateHandlers[name](self, oldValue)

    def __update(self, name):
        """Updates a specific property's cached value"""
        value = SkypeMessage(self.__iface.send("GET %s %s %s"%(self.__type, self.__id, name.upper())))
        self._update(value)

    def __getattr__(self, name):
        """Translates python properties to skype interface queries"""
        if (not (name in self.__values)):
            self.__update(name)
        return self.__values[name]

    def __repr__(self):
        return "<SkypeObject(%s,%s) at %d>"%(self.__type, self.__id, id(self))

class SkypeInterface(dbus.service.Object):
    """The python interface to the Skype client.
    
    When new objects are available in skype, this object's on_new_<type> method is called.

    Available object types:
        call - A VOIP call
        chatmessage - Single message within a text chat
        chat - Text chat session
        user - Skype user
        profile - Skype user profile
        chatmember - Member of a text chat
        voicemail - Skype VOIP voicemail
        sms - SMS Text message
        application - Global skype application
        group - A group contact
        filetransfer

    For details about what properties each object has, refer to the official skype documentation
    """
    def __init__(self, bus, name):
        """Creates a new SkypeInterface.

        Pass in a dbus.BusConnection and your client name
        """
        dbus.service.Object.__init__(self, bus, "/com/Skype/Client")
        skypeObj = bus.get_object("com.Skype.API", "/com/Skype")
        self.__skype = dbus.Interface(skypeObj, dbus_interface="com.Skype.API")
        self.send("NAME %s"%(name))
        self.send("PROTOCOL 7")
        self.__objects = {}

    @dbus.service.method(dbus_interface='com.Skype.API.Client')
    def Notify(self, message_text):
        """Recieves skype notifications"""
        _log.debug("<- %s", message_text)
        msg = SkypeMessage(message_text)
        obj = SkypeObject(self, msg.command, msg.args[0])
        try:
            self.on_message(msg)
        except Exception, e:
            _log.exception(e)

        obj._update(msg)

        if (obj.type not in self.__objects):
            self.__objects[obj.type] = {}

        if (obj.id in self.__objects[obj.type]):
            self.__objects[obj.type][obj.id]._update(msg)
            return

        self.__objects[obj.type][obj.id] = obj

        handlerName = "on_new_"+obj.type.lower()
        if (hasattr(self, handlerName)):
            func = getattr(self, handlerName)
            try:
                func(obj)
            except Exception, e:
                _log.exception(e)

    def on_message(self, message):
        """Implement to handle raw skype messages"""
        pass

    def send(self, cmd):
        """Sends a raw command via the Skype interface"""
        _log.debug("-> %s", cmd)
        return self.__skype.Invoke(cmd)


if (__name__ == "__main__"):
    DBusGMainLoop(set_as_default=True)
    logging.basicConfig(level=logging.DEBUG)
    SkypeInterface(dbus.SessionBus(), "skype.py")
    loop = gobject.MainLoop()
    loop.run()
