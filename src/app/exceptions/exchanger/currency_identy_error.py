from src.app.exceptions.user_error import UserError


class CurrencyIdentityError(UserError):
    def __init__(self, message: str):
        super().__init__(message, 400)
