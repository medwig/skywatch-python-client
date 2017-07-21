class SkywatchException(Exception):
    '''Exception'''
    pass


class InvalidAPIKey(SkywatchException):
    '''Invalid API key'''
    pass

class InvalidRequestError(SkywatchException):
    '''Invalid query parameters passed'''
    pass

class SkywatchInternalError(SkywatchException):
    '''Internal error in the skywatch client'''
    pass

