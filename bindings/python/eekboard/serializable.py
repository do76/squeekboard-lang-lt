# vim:set et sts=4 sw=4:
#
# ibus - The Input Bus
#
# Copyright (c) 2007-2010 Peng Huang <shawn.p.huang@gmail.com>
# Copyright (c) 2007-2010 Red Hat, Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA  02111-1307  USA

__all__ = (
        "Serializable",
        "serialize_object",
        "deserialize_object",
    )

import dbus
import gobject

__serializable_name_dict = dict()

def serializable_register(classobj):
    # if not issubclass(classobj, Serializable):
    #     raise "%s is not a sub-class of Serializable" % str(classobj)
    __serializable_name_dict[classobj.__NAME__] = classobj

def serialize_object(o):
    if isinstance(o, Serializable):
        l = [o.__NAME__]
        o.serialize(l)
        return dbus.Struct(l)
    else:
        return o

def deserialize_object(v):
    if isinstance(v, tuple):
        struct = list(v)
        type_name = struct.pop(0)
        type_class = __serializable_name_dict[type_name]
        o = type_class()
        o.deserialize (struct)
        return o
    return v

class SerializableMeta(gobject.GObjectMeta):
    def __init__(cls, name, bases, dict_):
        super(SerializableMeta, cls).__init__(name, bases, dict_)
        if "__NAME__" in cls.__dict__:
            serializable_register(cls)

class Serializable(gobject.GObject):
    __metaclass__ = SerializableMeta
    __gtype_name__ = "PYEekSerializable"
    __NAME__ = "EekSerializable"
    def __init__(self):
        super(Serializable, self).__init__()

    def serialize(self, struct):
        pass

    def deserialize(self, struct):
        pass

__serializable_name_dict["EekSerializable"] = Serializable