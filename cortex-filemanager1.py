#!/usr/bin/env python3
"""Minimal org.freedesktop.FileManager1 service for cortex-linux."""
import subprocess, sys, os
try:
    import dbus, dbus.service, dbus.mainloop.glib
    from gi.repository import GLib
except Exception:
    sys.exit(0)

BUS='org.freedesktop.FileManager1'
PATH='/org/freedesktop/FileManager1'
IFACE='org.freedesktop.FileManager1'

class FM(dbus.service.Object):
    @dbus.service.method(IFACE, in_signature='ass', out_signature='')
    def ShowItems(self, uris, startup_id):
        for u in uris:
            p=u.replace('file://','')
            if os.path.isdir(p):
                subprocess.Popen(['cortex'], cwd=p)
            else:
                subprocess.Popen(['cortex'], cwd=os.path.dirname(p) or '/')
    @dbus.service.method(IFACE, in_signature='ass', out_signature='')
    def ShowFolders(self, uris, startup_id):
        self.ShowItems(uris, startup_id)
    @dbus.service.method(IFACE, in_signature='ass', out_signature='')
    def ShowItemProperties(self, uris, startup_id):
        self.ShowItems(uris, startup_id)

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus=dbus.SessionBus()
name=dbus.service.BusName(BUS, bus)
FM(bus, PATH)
GLib.MainLoop().run()
