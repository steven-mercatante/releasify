from .utils import ReleaseType


class ClientError(Exception):
    def __init__(self, message=None, resp=None):
        super(ClientError, self).__init__(message)
        self.resp = resp


class UnauthorizedError(ClientError):
    def __init__(self, resp):
        message = 'Unauthorized. Check your credentials.'
        super(UnauthorizedError, self).__init__(message, resp)


class NotFoundError(ClientError):
    def __init__(self, resp):
        message = 'Resource not found'
        super(NotFoundError, self).__init__(message, resp)


class NoCommitsError(ClientError):
    def __init__(self):
        message = 'No commits since last release'
        super(NoCommitsError, self).__init__(message)


class InvalidReleaseTypeError(ClientError):
    def __init__(self, release_type):
        release_types = ', '.join(member.value for _, member in ReleaseType.__members__.items())
        message = f'`{release_type}` is not a valid release type. Must be one of: {release_types}'
        super(InvalidReleaseTypeError, self).__init__(message)
