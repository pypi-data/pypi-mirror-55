import cgi
import io
import json
from urllib.parse import urlsplit
from urllib.parse import parse_qsl
from http.cookies import SimpleCookie
from urllib.parse import urlsplit
from urllib.parse import parse_qsl

from hippu.errors import InvalidContentType
from hippu.http import Status
from hippu.http import Header


class Request:
    def __init__(self, exchange):
        self._exchange = exchange
        # Request body
        self._data = None
        # Expose exchange attributes trough Request object.
        self.client_address = exchange.client_address
        self.method = exchange.command
        self.headers = exchange.headers
        self.rfile = self._exchange.rfile
        self.path = self.create_path(self._exchange.path)

    def __len__(self):
        return self.content_length

    @classmethod
    def create_path(cls, path):
        return Path(path)

    @property
    def query(self):
        """ Query string part of the path. """
        return self.path.query

    @property
    def content(self):
        """ Returns content as bytes. """
        if not self._data:
            self._data = self._exchange.rfile.read(self.content_length)
        return self._data

    @property
    def text(self):
        """ Returns request data as utf-8 decoded string. """
        return self.content.decode('utf-8')

    @property
    def json(self):
        """ Convert request data (json) into Python data type. """
        if self.is_content_type(Header.APPLICATION_JSON):
            return json.loads(self.text)
        raise InvalidContentType()

    @property
    def form(self):
        with io.BytesIO(self.content) as data:
            form = cgi.FieldStorage(
                    fp = data,
                    headers = self.headers,
                    environ = { 'REQUEST_METHOD': self.method,
                                'CONTENT_TYPE': self.content_type,
                               })
        return form

    @property
    def content_type(self):
        """ Returns request content type. """
        return self.get_header(Header.CONTENT_TYPE)

    @property
    def content_length(self):
        """ Returns content length. """
        return int(self.get_header(Header.CONTENT_LENGTH, 0))

    @property
    def cookie(self):
        if not hasattr(self, '_cookie'):
            self._cookie = SimpleCookie()

            cookie_str = self.get_header(Header.COOKIE)

            if cookie_str:
                self._cookie.load(cookie_str)

        return self._cookie

    def get_header(self, key, default=None):
        """ Returns header value. """
        return self.headers.get(str(key), default)

    def is_content_type(self, value):
        """ Returns true if content type matches. """
        return str(self.content_type).lower() == str(value).lower()

    def __str__(self):
        return "HTTP {} {}".format(self.method, self.path)


class Path:
    def __init__(self, path):
        if not path.startswith('/'):
            path = '/' + path

        self._path = path
        self._components = urlsplit(path)
        self._base = ''

    @property
    def absolute(self):
        return self._components.path

    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, path):
        if not path.startswith('/'):
            path = '/' + path

        if path.endswith('/'):
            path = path[:-1]

        self._base = path

    @property
    def relative(self):
        return self.absolute.replace(self._base, '', 1)

    @property
    def query(self):
        return dict(parse_qsl(self._components.query))

    def startswith(self, s):
        return str(self).startswith(s)

    def __str__(self):
        return self._path
