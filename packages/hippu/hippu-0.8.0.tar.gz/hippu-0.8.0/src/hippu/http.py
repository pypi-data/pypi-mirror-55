""" HTTP related constants. """
from enum import Enum
from enum import IntEnum


class Header(Enum):
    """ HTTP header related constants. """

    AGE = 'Age'
    CACHE_CONTROL = 'Cache-Control'
    CONNECTION = 'connection'
    CONTENT_ENCODING = 'Content-Encoding'
    CONTENT_TYPE = 'Content-Type'
    CONTENT_LENGTH = 'Content-Length'
    KEEP_ALIVE = 'Keep-Alive'
    LOCATION = 'Location'
    PRAGMA = 'Pragma'
    SET_COOKIE = 'Set-Cookie'
    TRANSFER_ENCODING = 'Transfer-Encoding'
    COOKIE = 'Cookie'
    ACCESS_CONTROL_ALLOW_ORIGIN = 'Access-Control-Allow-Origin'

    # HTTP header values

    APPLICATION_JSON = 'application/json'
    BOUNDARY = 'boundary'
    CHUNKED = 'chunked'
    GZIP = 'gzip'
    IMAGE_GIF = 'image/gif'
    IMAGE_PNG = 'image/png'
    IMAGE_JPEG = 'image/jpeg'
    IMAGE_BMP = 'image/bmp'
    IMAGE_ICO = 'image/ico'
    MULTIPART_X_MIXED_REPLACE = 'multipart/x-mixed-replace'
    NO_CACHE = 'no-cache'
    PRIVATE = 'private'
    TEXT_HTML = 'text/html'
    TEXT_PLAIN = 'text/plain'

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return str(self.value).lower() == str(other).lower()

    # If a class that overrides __eq__() needs to retain the implementation of
    # __hash__() from a parent class, the interpreter must be told this
    # explicitly by setting __hash__ = <ParentClass>.__hash__. Otherwise the
    # inheritance of __hash__() will be blocked, just as if __hash__ had been
    # explicitly set to None.
    #
    # http://docs.python.org/3.1/reference/datamodel.html#object.__hash__
    __hash__ = Enum.__hash__


class Status(IntEnum):
    """ HTTP response status codes.

    See e.g., https://developer.mozilla.org/en-US/docs/Web/HTTP/Status.
    """

    # 1xx INFORMATIONAL

    CONTINUE = 100
    SWITCHING_PROTOCOLS = 101
    PROCESSING = 102

    # 2×× SUCCESS

    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NON_AUTHORITATIVE_INFORMATION = 203
    NO_CONTENT = 204
    RESET_CONTENT = 205
    PARTIAL_CONTENT = 206
    MULTI_STATUS = 207
    ALREADY_REPORTED = 208
    IM_USED = 226

    # 3×× REDIRECTION

    MULTIPLE_CHOICES = 300
    MOVED_PERMANENTLY = 301
    FOUND = 302
    SEE_OTHER = 303
    NOT_MODIFIED = 304
    USE_PROXY = 305
    TEMPORARY_REDIRECT = 307
    PERMANENT_REDIRECT = 308

    # 4×× CLIENT_ERROR

    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    PAYMENT_REQUIRED = 402
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    PROXY_AUTHENTICATION_REQUIRED = 407
    REQUEST_TIMEOUT = 408
    CONFLICT = 409
    GONE = 410
    LENGTH_REQUIRED = 411
    PRECONDITION_FAILED = 412
    PAYLOAD_TOO_LARGE = 413
    REQUEST_URI_TOO_LONG = 414
    UNSUPPORTED_MEDIA_TYPE = 415
    REQUESTED_RANGE_NOT_SATISFIABLE = 416
    EXPECTATION_FAILED = 417
    IM_A_TEAPOT = 418
    MISDIRECTED_REQUEST = 421
    UNPROCESSABLE_ENTITY = 422
    LOCKED = 423
    FAILED_DEPENDENCY = 424
    UPGRADE_REQUIRED = 426
    PRECONDITION_REQUIRED = 428
    TOO_MANY_REQUESTS = 429
    REQUEST_HEADER_FIELDS_TOO_LARGE = 431
    CONNECTION_CLOSED_WITHOUT_RESPONSE = 444
    UNAVAILABLE_FOR_LEGAL_REASONS = 451
    CLIENT_CLOSED_REQUEST = 499

    # 5×× SERVER_ERROR

    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504
    HTTP_VERSION_NOT_SUPPORTED = 505
    VARIANT_ALSO_NEGOTIATES = 506
    INSUFFICIENT_STORAGE = 507
    LOOP_DETECTED = 508
    NOT_EXTENDED = 510
    NETWORK_AUTHENTICATION_REQUIRED = 511
    NETWORK_CONNECT_TIMEOUT_ERROR = 599
