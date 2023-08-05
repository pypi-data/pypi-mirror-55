from contextlib import contextmanager
from enum import IntEnum
import io
import json
import logging
from http.cookies import SimpleCookie

try:
    from PIL import Image
except ImportError:
    pil_support = False
else:
    pil_support = True

from hippu.http import Status
from hippu.http import Header


log = logging.getLogger(__name__)


class Response:
    def __init__(self, exchange):
        self._exchange = exchange
        # Note: Requests lib uses matching 'status_code' attribute.
        self.status_code = Status.OK
        # Content type is determined and set by the server unless
        # explicitly set.
        self.content_type = None
        self._data = None
        self.headers = {}
        self.headers_sent = False
        self._keep_alive = None
        self.encoding = 'UTF-8'

    def __len__(self):
        if self._data:
            return len(self._data)
        return 0

    @classmethod
    def create(self, exchange):
        return Response(exchange)

    @property
    def content(self):
        return self._data

    @content.setter
    def content(self, data):
        # Content type is determined and set by the server if not set explicitely.
        self._data = data

    @property
    def text(self):
        return self.content.decode('utf-8')

    @property
    def server(self):
        """ Returns the HTTP server instance. """
        return self._exchange.server

    def set_header(self, key, value):
        #
        # Converting headers to all lower case to simplify following
        # operations.
        #
        # HTTP header names are case-insensitive, according to RFC 2616:
        #   Each header field consists of a name followed by a colon (":")
        #   and the field value. Field names are case-insensitive.
        #
        #   [https://www.w3.org/Protocols/rfc2616/rfc2616-sec4.html#sec4.2]
        #
        self.headers[str(key).lower()] = value

    def get_header(self, key, default=None):
        return self.headers.get(str(key).lower(), default)

    def send_status(self, code):
        """ Send response status code. """
        self._exchange.send_response(code)

    def send_header(self, key, value):
        """ Send single HTTP header. """
        self._exchange.send_header(str(key), value)
        self.headers_sent = True

    def send_headers(self, headers):
        """ Send response headers. """
        self._exchange.send_headers(headers)
        self.headers_sent = True

    def keep_alive(self, timeout=10, max_count=100):
        self._keep_alive = (timeout, max_count)

    def write(self, data):
        """ Write data. """
        self._exchange.wfile.write(data)

    @property
    def cookie(self):
        if not hasattr(self, '_cookie'):
            self._cookie = SimpleCookie()
        return self._cookie

    def finalize(self):
        """ Converts data into bytes and resolves content-type and
        encoding.

        Server will call finalize() method just before send. Filters
        will be applied before this.
        """
        data = self._data
        content_type = self.content_type

        # Use content-type and encoding set.
        if isinstance(data, bytes):
            pass

        # Strings are encoded by using response encoding type.
        elif isinstance(data, str):
            self.content = data.encode(self.encoding)
            self.content_type = Header.TEXT_HTML

        # Strings are encoded by using response encoding type.
        elif isinstance(data, (int, float)):
            self.content = str(data).encode(self.encoding)
            self.content_type = Header.TEXT_HTML

        # Dicts, lists and tuples will be converted to bytes by using
        # standard json library.
        elif isinstance(data, (dict, list, tuple)):
            data = json.dumps(data, default=to_json)
            self.content = data.encode(self.encoding)
            self.content_type = Header.APPLICATION_JSON

        # PIL images are returned in png format.
        elif pil_support and isinstance(data, Image.Image):
            if not content_type:
                img_frmt = 'png'
                content_type = Header.IMAGE_PNG
            elif content_type == Header.IMAGE_BMP:
                img_frmt = 'bmp'
            elif content_type == Header.IMAGE_GIF:
                img_frmt = 'gif'
            elif content_type == Header.IMAGE_JPEG:
                img_frmt = 'jpeg'
            elif content_type == Header.IMAGE_PNG:
                img_frmt = 'png'
            elif content_type == Header.IMAGE_ICO:
                img_frmt = 'ico'
            else:
                log.warning("Content-type '{}' does not match the content (PIL Image).")
                img_frmt = 'png'
                content_type = Header.IMAGE_PNG

            with io.BytesIO() as f:
                data.save(f, format=img_frmt)
                self.content = f.getvalue()

            self.content_type = Header.IMAGE_PNG

        # Content type is set as text/html but the content is not string.
        elif content_type == Header.TEXT_HTML and not isinstance(data, str):
            self.content = str(self.content).encode(self.encoding)

        elif hasattr(data, '__iter__'):
            data = json.dumps(dict(data), default=to_json)
            self.content = data.encode(self.encoding)
            self.content_type = Header.APPLICATION_JSON


def to_json(o):
    """
    Example:
        def to_dict(self):
            return dict(name=self.name, id=self.id)

        def __iter__(self):
            return iter([('name', self.name), ('id', self.id)])
    """
    if hasattr(o, 'to_dict'):
        return o.to_dict()
    return dict(o)
