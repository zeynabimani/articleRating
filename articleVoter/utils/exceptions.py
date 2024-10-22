import logging

from rest_framework import status

logger = logging.getLogger(__name__)


class Error(Exception):
    """
    Base class for microservice errors

    Typically a Http response is generated from this.
    """

    def __init__(self, type, message, http_status_code, extra_info=None):
        super(Error, self).__init__(message)
        self.type = type
        self.message = message
        self.http_status_code = http_status_code
        self.extra_info = extra_info


class BadRequestError(Error):
    """
    Is raised when an invalid request comes from client
    """

    def __init__(self, message, extra_info=None):
        super(BadRequestError, self).__init__(
            'bad_request', message, suggested_http_status=status.HTTP_400_BAD_REQUEST, extra_info=extra_info
        )
