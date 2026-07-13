class AppError(ValueError):
    """Base application exception that carries an HTTP status code."""
    status_code = 400

    def __init__(self, message: str):
        super().__init__(message)


class BadRequest(AppError):
    status_code = 400


class NotFound(AppError):
    status_code = 404


class Forbidden(AppError):
    status_code = 403


class Conflict(AppError):
    status_code = 409
