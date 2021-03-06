class InvalidCredentialsError(Exception):
    """Will be raised if username or password is not valid."""


class AccessForbiddenError(Exception):
    """Will be raised if user has not enough permissions for action."""


class InvalidAccessToken(Exception):
    """Will be raised if access token is not valid."""


class UserNotFoundError(Exception):
    """Will be raised if user does not exist."""


class UserAlreadyExistsError(Exception):
    """Will be raised if user already exists."""
