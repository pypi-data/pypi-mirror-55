import threading
from queue import Queue

from hippu.http import Status
from hippu.http import Header



# TO DO
#
#   Base stream is chunked.
#
#   do_chunk_begin
#   do_chunk
#   do_chunk_end
#
#  MJPEGStream is specialized from chunked stream.
#
#  IS buffer size needed? Can buffering moved outside of the stream? Like
#  StreamBuffer + Blocking Stream.
#
#  buffer = StreamBuffer(10)

#  with res.stream() as stream:
#      while stream:
#          stream.put(buffer.get())
#
# There could be

class StreamClosed(Exception):
    """ Raised if user tries to write into closed stream. """
    pass


class StreamFactory:
    """ Stream factory to create stream objects. """

    @classmethod
    def create(cls, response, buffer_size=0):
        if buffer_size == 0:
            return NonBlockingStream(response)

        if buffer_size == 1:
            return Stream(response)

        if buffer_size > 0:
            return BufferedStream(response)

        raise ValueError("Invalid buffer size: {}. Should be [0..n] where n is integer.".format(buffer_size))


class Stream:
    """ Base HTTP stream.

    Stream takes response object and content type as arguments.
    """

    def __init__(self, response, content_type='image/jpeg'): #, boundary='FRAME'):
        self._frame_count = 0
        self._response = response
        self._open = threading.Event()
        self.content_type = content_type

        # self._boundary = boundary
        # self._beging_of_frame = '--{}\r\n'.format(self._boundary).encode()

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
        """ Returns true if stream is open. """
        return self._open.is_set()

    @property
    def frame_count(self):
        return self._frame_count

    def open(self):
        """ Open data stream by sending headers. """
        # content_type = "multipart/x-mixed-replace; boundary={}".format(self._boundary)
        self._send_status(Status.OK)
        self._send_headers({ Header.AGE: 0,
                             Header.CACHE_CONTROL: 'no-cache, private',
                             Header.PRAGMA: 'no-cache',
                             Header.CONTENT_TYPE: "multipart/x-mixed-replace; boundary=FRAME" })

        # Stream is "opened" and it's possible put data in to it.
        self._open.set()

    def put(self, data):
        """ Put data to stream. """
        self._write_frame(data, self.content_type)

    def close(self):
        self._open.clear()

    def _write_frame(self, data, content_type):
        """ Write HTTP frame to response. """
        if not self._open.is_set():
            raise StreamClosed("Stream is not open for writing.")

        try:
            self._write(b'--FRAME\r\n')
            self._send_headers({ Header.CONTENT_TYPE: content_type,
                                 Header.CONTENT_LENGTH: len(data) })
            self._write(data)
            self._write(b'\r\n')
        except BrokenPipeError:
            # Client has closed the connection. It's not possible to write
            # data to stream.
            self.close()
        except OSError:
            # Any other OS based error.
            # See https://docs.python.org/3/library/exceptions.html#os-exceptions
            self.close()
        else:
            self._increase_frame_count()
            # Close stream also if server is closed.
            if self._response.server.is_stopped():
                self.close()

    def _send_status(self, status):
        self._response.send_status(status)

    def _send_headers(self, headers):
        self._response.send_headers(headers)

    def _write(self, data):
        self._response.write(data)

    def _increase_frame_count(self):
        self._frame_count += 1


class BufferedStream(Stream):
    """ Buffered stream. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._queue = Queue()
        self._stopped = threading.Event()

    def open(self):
        """ Opens stream and starts a worker thread. """
        super().open()
        threading.Thread(target=self._worker).start()

    def close(self):
        """ Closes stream and notifies worker thread. """
        super().close()
        self._stopped.set()

    def put(self, data, block=True, timeout=None):
        self._queue.put(data, block=block, timeout=timeout)

    def _worker(self):
        """ Writes data to stream. """
        while True:
            if self._stopped.is_set():
                break

            try:
                item = self._queue.get(timeout=1)
            except queue.Empty:
                continue

            try:
                self._write_frame(item, self.content_type)
            except:
                self._stopped.set()
            finally:
                self._queue.task_done()


class NonBlockingStream(Stream):
    """ Non blocking and non buffered stream.

    Calling put(data) does not block. Data is not buffered; only the latest data
    object is sent if data is set multiple times in between two subsequent frame
    write operations (producer is faster than consumer).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = None
        self._stopped = threading.Event()
        self._data_available = threading.Event()

    def open(self):
        """ Opens stream and starts a worker thread. """
        super().open()
        threading.Thread(target=self._worker).start()

    def put(self, data):
        """ Put data to stream. """
        if self._stopped.is_set():
            raise ConnectionError("Connection closed")

        self._data = data
        self._data_available.set()

    def close(self):
        """ Closes stream and notifies worker thread. """
        super().close()
        self._stopped.set()
        self._data_available.clear()

    def _worker(self):
        """ Writes data frames to response stream. """
        while True:
            if self._stopped.is_set():
                break

            if self._data_available.wait(timeout=0.25):
                data = self._data
                self._data_available.clear()

                try:
                    self._write_frame(data, self.content_type)
                except:
                    self._stopped.set()
