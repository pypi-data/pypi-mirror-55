from requests.exceptions import RequestException


class HttpResponseError(RequestException):
    """ Base error for the application """
    @property
    def error(self):
        if self.response:
            return getattr(self.response, 'error')

    @property
    def request_id(self):
        if self.response:
            return getattr(self.response, 'requestId')

    @property
    def context(self):
        if self.response:
            return getattr(self.response, 'context')

    @property
    def name(self):
        if self.response:
            return getattr(self.response, 'name')

    @property
    def code(self):
        if self.response:
            return getattr(self.response, 'status_code')


class ApiKeyError(Exception):
    """ Merchant key was not valid """
