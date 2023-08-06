"""
Copyright 2019 Zakru

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files
(the "Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import json
import urllib.request
import urllib.parse


def request(url, *args, **kwargs):
    """Requests a single JSON resource from the Wynncraft API.

    :param url: The URL of the resource to fetch
    :type url: :class:`str`
    :param args: Positional arguments to pass to the URL
    :param kwargs: Keyword arguments (:class:`str`) to pass to the URL

    :returns: The returned JSON object as a :class:`dict`
    :rtype: :class:`dict`
    """
    parsedArgs = (urllib.parse.quote(a) for a in args)

    parsedKwargs = {}
    for k,v in kwargs.items():
        parsedKwargs[k] = urllib.parse.quote(v)

    response = urllib.request.urlopen(url.format(*parsedArgs, **parsedKwargs))
    data = json.load(response)
    response.close()
    return data

def requestLegacy(url, *args, **kwargs):
    """Requests a single JSON resource from the Wynncraft API in the
    legacy format.

    :param url: The URL of the resource to fetch
    :type url: :class:`str`
    :param args: Positional arguments to pass to the URL
    :param kwargs: Keyword arguments (:class:`str`) to pass to the URL

    :returns: The returned JSON object as a :class:`dict`
    :rtype: :class:`dict`
    """
    data = request(url, *args, **kwargs)
    del data['request']
    return data


def requestList(url, *args, **kwargs):
    """Requests a list of objects from the Wynncraft API in the most
    commonly used format.

    :param url: The URL of the resource to fetch
    :type url: :class:`str`
    :param args: Positional arguments to pass to the URL
    :param kwargs: Keyword arguments to pass to the URL

    :returns: The returned ``data`` as a :class:`dict`
    :rtype: :class:`dict`
    """
    return request(url, *args, **kwargs)['data']


def requestObject(url, *args, **kwargs):
    """Requests a single object from the Wynncraft API in the most
    commonly used format.

    :param url: The URL of the resource to fetch
    :type url: :class:`str`
    :param args: Positional arguments to pass to the URL
    :param kwargs: Keyword arguments to pass to the URL

    :returns: The first element of the returned ``data`` as a
       :class:`dict`
    :rtype: :class:`dict`
    """
    return requestList(url, *args, **kwargs)[0]


class ObjectFromDict:
    """Recursively wraps a :class:`dict` in a Python object.

    Example use::

       >>> o = ObjectFromDict({'foo': 'bar'})
       >>> o.foo
       'bar'

    :param data: The parsed JSON data from the Wynncraft API
    :type data: :class:`dict`
    """

    def __init__(self, data):
        for k,v in data.items():
            self.__dict__[k] = self._handleItem(v)

    def _handleItem(self, item):
            if isinstance(item, dict):
                return ObjectFromDict(item)
            elif isinstance(item, list):
                return [self._handleItem(v) for v in item]
            else:
                return item

    def __repr__(self):
        return dict.__repr__(self.__dict__)
