import io
import threading

try:
    from PIL import Image
except ImportError:
    _PIL_SUPPORT = False
else:
    _PIL_SUPPORT = True

try:
    import numpy
except ImportError:
    _NPY_SUPPORT = False
else:
    _NPY_SUPPORT = True

try:
    import cv2
except ImportError:
    _CV2_SUPPORT = False
else:
    _CV2_SUPPORT = True

from hippu.http import Status
from hippu.http import Header


class StreamClosed(Exception):
    """ Raised if user tries to write into closed stream. """
    pass


class Stream:
    """ Stream base.

    Stream takes response object and content type as arguments.
    """

    def __init__(self, response, content_type):
        self._response = response
        self._content_type = content_type
        self._open = threading.Event()

    def __enter__(self):
        """ Required by context manager to open the stream.

        Example usage where stream() returns a stream object:

            >>> with response.stream() as stream:
            >>>    pass
        """
        self.open()
        return self

    def __exit__(self, *args):
        """ Required by context manager to close the stream.

        Example usage where stream() returns a stream object:

            >>> with response.stream() as stream:
            >>>    pass
        """
        self.close()

    def __bool__(self):
        """ Returns true if stream is open to write. """
        return self.is_open()

    def is_open(self):
        """ Returns true if stream is open to write. """
        return self._open.is_set()

    def open(self):
        """ Open data stream. """
        self._open.set()

    def write(self, data):
        """ Write data to stream. """
        if not self._open.is_set():
            raise StreamClosed("Stream is not open for writing.")

        try:
            self.do_write(data)
        except BrokenPipeError:
            # Client has closed the connection. It's not possible to write
            # data to stream.
            self._open.clear()
        except OSError:
            # Any other OS based error.
            # See https://docs.python.org/3/library/exceptions.html#os-exceptions
            self._open.clear()
        else:
            # Close stream also if server is closed.
            if self._response.server.is_stopped():
                self.close()

    def close(self):
        """ Close stream. """
        self._open.clear()

    def do_write(self, data):
        """ Write one piece of data in to stream. """
        self._write(data)

    def _send_status(self, status):
        self._response.send_status(status)

    def _send_headers(self, headers):
        self._response.send_headers(headers)

    def _write(self, data):
        self._response.write(data)


class ChunkedStream(Stream):
    """ Chunked stream.

    See https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Transfer-Encoding
    """

    def open(self):
        """ Open chunked data stream. """
        self._send_status(Status.OK)
        self._send_headers({ Header.TRANSFER_ENCODING: Header.CHUNKED,
                             Header.CONTENT_TYPE: self._content_type })
        super().open()

    def do_write(self, data):
        """ Write 'chunk' of data to stream. """
        self._write(b'%x\r\n' % len(data))
        self._write(data)
        self._write(b'\r\n')

    def close(self):
        """ Close chunked data stream. """

        if self._open.is_set():
            try:
                self._write(b'0\r\n')
                self._write(b'\r\n')
            except BrokenPipeError:
                # Client might have or can close the connection.
                pass

        super().close()


class MJPEGStream(Stream):
    """ Motion JPEG (MJPEG) stream. """
    def __init__(self, response):
        super().__init__(response=response, content_type='image/jpeg')
        self.headers = { Header.AGE: 0,
                         Header.CACHE_CONTROL: 'no-cache, private',
                         Header.PRAGMA: 'no-cache',
                         Header.CONTENT_TYPE: "multipart/x-mixed-replace; boundary=FRAME" }

    def open(self):
        """ Open data stream by sending headers. """
        self._send_status(Status.OK)
        self._send_headers(self.headers)
        super().open()

    def do_write(self, data):
        """ Write image data to stream. """
        self._write(b'--FRAME\r\n')
        self._send_headers({ Header.CONTENT_TYPE: self._content_type,
                             Header.CONTENT_LENGTH: len(data) })
        self._write(data)
        self._write(b'\r\n')

    def put(self, image):
        """ Put image object into stream. """
        self.write(self.get_bytes_of(image))

    def get_bytes_of(self, image):
        """ Returns byte presentation of an image in JPEG format.

        Supports PIL and Numpy images.

        Raises TypeError if provided image object is not supported.

        This method can be replaced to add support for additional image types.
        For example:
            >>> stream.get_bytes_of = get_bytes_of_my_img_type
        """
        if _PIL_SUPPORT and isinstance(image, Image.Image):
            return get_pil_img_bytes(image)

        if _NPY_SUPPORT and isinstance(image, numpy.ndarray):
            return get_npy_img_bytes(image)

        raise TypeError("Not supported type: '{}'".format(image))


def get_pil_img_bytes(image):
    """ Returns bytes presentation of PIL image. """
    with io.BytesIO() as output:
        image.save(output, format="JPEG")
        return output.getvalue()


def get_npy_img_bytes(image):
    """ Returns bytes presentation of Numpy image.

    Raises an exception if no OpenCV support (not installed).
    """
    if not _CV2_SUPPORT:
        raise Exception("OpenCV is required to encode numpy arrays into JPG format.")

    return cv2.imencode(ext='.jpg', img=image)[1]
