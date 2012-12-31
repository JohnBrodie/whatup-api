

class APIError(Exception):

    def __init__(self, errors):
        self.errors = errors
