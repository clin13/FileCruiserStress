class ClientBadRequestError(Exception):
    def __init__(self, value = '', code = 0, path = ''):
        self.value = value
        self.code = code
        self.path = path
    def __str__(self):
        return repr(self.value)
            
class ClientInternalServerError(Exception):
    def __init__(self, value = '', code = 0):
        self.value = value
        self.code = code
    def __str__(self):
        return repr(self.value)

class ClientUnauthorizedError(Exception):
    def __init__(self, value = 'Unauthorized', code = 0):
        self.value = value
        self.code = code
    def __str__(self):
        return repr(self.value)
