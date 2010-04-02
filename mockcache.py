# Copyright (c) 2010 Lunant <http://lunant.net/>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
"""The Python dictionary-based mock memcached client library. It does not
connect to any memcached server, but keeps a dictionary and stores every cache
into there internally. It is a just emulated API of memcached client only for
tests. It implements expiration also. NOT THREAD-SAFE.

    try:
        import memcache
    except ImportError:
        import warnings
        import mockcache as memcache
        warnings.warn("imported mockcache instead of memcache; cannot find "
                      "memcache module")

    mc = memcache.Client(["127.0.0.1:11211"])

This module and other memcached client libraries have the same behavior.

    >>> from mockcache import Client
    >>> mc = Client()
    >>> mc
    <mockcache.Client {}>
    >>> mc.get("a")
    >>> mc.get("a") is None
    True
    >>> mc.set("a", "1234")
    1
    >>> mc.get("a")
    '1234'
    >>> mc
    <mockcache.Client {'a': ('1234', None)}>
    >>> mc.add("a", "1111")
    0
    >>> mc.get("a")
    '1234'
    >>> mc
    <mockcache.Client {'a': ('1234', None)}>
    >>> mc.replace("a", "2222")
    1
    >>> mc.get("a")
    '2222'
    >>> mc
    <mockcache.Client {'a': ('2222', None)}>
    >>> mc.append("a", "3")
    1
    >>> mc.get("a")
    '22223'
    >>> mc
    <mockcache.Client {'a': ('22223', None)}>
    >>> mc.prepend("a", "1")
    1
    >>> mc.get("a")
    '122223'
    >>> mc
    <mockcache.Client {'a': ('122223', None)}>
    >>> mc.incr("a")
    122224
    >>> mc.get("a")
    122224
    >>> mc
    <mockcache.Client {'a': (122224, None)}>
    >>> mc.incr("a", 10)
    122234
    >>> mc.get("a")
    122234
    >>> mc
    <mockcache.Client {'a': (122234, None)}>
    >>> mc.decr("a")
    122233
    >>> mc.get("a")
    122233
    >>> mc
    <mockcache.Client {'a': (122233, None)}>
    >>> mc.decr("a", 5)
    122228
    >>> mc.get("a")
    122228
    >>> mc
    <mockcache.Client {'a': (122228, None)}>
    >>> mc.replace("b", "value")
    0
    >>> mc.get("b")
    >>> mc.get("b") is None
    True
    >>> mc
    <mockcache.Client {'a': (122228, None)}>
    >>> mc.add("b", "value", 5)
    1
    >>> mc.get("b")
    'value'
    >>> mc  # doctest: +ELLIPSIS
    <mockcache.Client {'a': (122228, None), 'b': ('value', ...)}>
    >>> import time
    >>> time.sleep(6)
    >>> mc.get("b")
    >>> mc.get("b") is None
    True
    >>> mc
    <mockcache.Client {'a': (122228, None)}>
    >>> mc.set("c", "value")
    1
    >>> mc.get_multi(["a", "b", "c"])
    {'a': 122228, 'c': 'value'}

"""

import datetime


__author__ = "Hong MinHee <http://dahlia.kr/>"
__maintainer__ = __author__
__email__ = "dahlia@lunant.net"
__copyright__ = "Copyright (c) 2010 Lunant <http://lunant.net/>"
__license__ = "MIT License"
__version__ = "1.0"


class Client(object):
    """Dictionary-based mock memcached client. Almost like other Python
    memcached client libraries' interface.

    """

    def __init__(self, *args, **kwargs):
        """Does nothing. It takes no or any arguments, but they are just for
        compatibility so ignored.

        """
        self.dictionary = {}

    def set_servers(self, servers):
        """Does nothing, like `__init__`. Just for compatibility."""
        pass

    def disconnect_all(self):
        """Does nothing, like `__init__`. Just for compatibility."""
        pass

    def delete(self, key, time=0):
        """Deletes the `key` from the dictionary."""
        if key in dictionary:
            if int(time) < 1:
                del self.dictionary[key]
                return 1
            self.set(key, self.dictionary[key], time)
        return 0

    def incr(self, key, delta=1):
        """Increments an integer by the `key`."""
        try:
            value, exp = self.dictionary[key]
        except KeyError:
            return
        else:
            value = int(value) + delta
            self.dictionary[key] = value, exp
            return value

    def decr(self, key, delta=1):
        """Decrements an integer by the `key`."""
        return self.incr(key, -delta)

    def append(self, key, val):
        """Append the `val` to the end of the existing `key`'s value.
        It works only when there is the key already.

        """
        try:
            self.dictionary[key] = str(self.dictionary[key][0]) + val, \
                                   self.dictionary[key][1]
        except KeyError:
            return 0
        else:
            return 1

    def prepend(self, key, val):
        """Prepends the `val` to the beginning of the existing `key`'s value.
        It works only when there is the key already.

        """
        try:
            self.dictionary[key] = val + str(self.dictionary[key][0]), \
                                   self.dictionary[key][1]
        except KeyError:
            return 0
        else:
            return 1

    def add(self, key, val, time=0):
        """Adds a new `key` with the `val`. Almost like `set` method,
        but it stores the value only when the `key` doesn't exist already.

        """
        if key in self.dictionary:
            return 0
        return self.set(key, val, time)

    def replace(self, key, val, time=0):
        """Replaces the existing `key` with `val`. Almost like `set` method,
        but it store the value only when the `key` already exists.

        """
        if key not in self.dictionary:
            return 0
        return self.set(key, val, time)

    def set(self, key, val, time=0):
        """Sets the `key` with `val`."""
        if not time:
            time = None
        elif time < 60 * 60 * 24 * 30:
            time = datetime.datetime.now() + datetime.timedelta(0, time)
        else:
            time = datetime.datetime.fromtimestamp(time)
        self.dictionary[key] = val, time
        return 1

    def get(self, key):
        """Retrieves a value of the `key` from the internal dictionary."""
        try:
            val, exptime = self.dictionary[key]
        except KeyError:
            return
        else:
            if exptime and exptime < datetime.datetime.now():
                del self.dictionary[key]
                return
            return val

    def get_multi(self, keys):
        """Retrieves values of the `keys` at once from the internal
        dictionary.

        """
        dictionary = self.dictionary
        pairs = ((key, dictionary[key]) for key in keys if key in dictionary)
        now = datetime.datetime.now
        return dict((key, value) for key, (value, exp) in pairs
                                 if not exp or exp > now())

    def __repr__(self):
        modname = "" if __name__ == "__main__" else __name__ + "."
        return "<%sClient %r>" % (modname, self.dictionary)

