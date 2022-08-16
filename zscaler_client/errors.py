class CredentialError(Exception):
    pass

class RequestError(Exception):
    pass

class ActivationError(Exception):
    pass

class ActionNotSupported(Exception):
    pass

class MaxSizeExeededError(Exception):
    pass

class UrlLengthExceeded(Exception):
    pass

class MissingRequiredField(Exception):
    pass

class MissingRequiredParameter(Exception):
    pass