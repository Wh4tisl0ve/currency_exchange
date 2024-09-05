from src.app.exceptions.db_error.database_error import DataBaseError


class ConstraintViolationException(Exception):
    def __init__(self, message: str, code: int):
        super().__init__(message)
        self.__code = code

    def to_dict(self) -> dict:
        return {"message": self.args[0],
                "code": self.__code}