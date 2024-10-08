from src.app.exceptions.constraint_violation_error import ConstraintViolationException
from src.app.exceptions.invalid_field_error import InvalidFieldError
from src.app.exceptions.db_error.database_error import DataBaseError
from src.app.exceptions.validation_error import ValidationError
from src.app.exceptions.no_content_error import NoContentError
from src.app.exceptions.not_found_error import NotFoundError
from src.app.services.currency_service import CurrencyService
from src.app.dto.currency_dto import CurrencyDTO
from src.app.router import Router


class CurrencyController:
    def __init__(self):
        self.__service = CurrencyService()
        self.register_routes()

    def register_routes(self):
        @Router().route(r'^/currencies$', method='GET')
        def get_all_currencies() -> dict:
            try:
                currencies = self.__service.get_all_currencies()
            except (NoContentError, DataBaseError) as err:
                return err.to_dict()

            return {"code": 200, "body": [currency.to_dict() for currency in currencies]}

        @Router().route(r'^/currency/(?P<currency_code>[a-zA-Z]{3})$', method='GET')
        def get_concrete_currencies(currency_code: str) -> dict:
            try:
                currency = self.__service.get_concrete_currency(currency_code)
            except (NotFoundError, DataBaseError) as err:
                return err.to_dict()

            return {"code": 200, "body": currency.to_dict()}

        @Router().route(r'^/currencies$', method='POST')
        def add_currency(request: dict) -> dict:
            try:
                request_dto = CurrencyDTO(name=request['name'],
                                          code=request['code'],
                                          sign=request['sign'])
                added_currency = self.__service.add_currency(request_dto)
            except KeyError:
                return InvalidFieldError('A required form field is missing').to_dict()
            except (ConstraintViolationException, ValidationError, DataBaseError, NotFoundError) as err:
                return err.to_dict()

            return {"code": 201, "body": added_currency.to_dict()}
