from src.app.exceptions.not_found_error import NotFoundError
from src.app.database.db_client import DBClient
from abc import abstractmethod, ABC


class BaseDAO(ABC):
    def __init__(self, db_client: DBClient, name_entity: str):
        self._client_db = db_client
        self._name_entity = name_entity

    def _get_all_entities(self) -> list[tuple]:
        query = f'SELECT * FROM {self._name_entity}'
        self._client_db.open_connection()
        entities = self._client_db.execute_dml(query)
        self._client_db.close_connection()

        return entities

    def _get_concrete_entity(self, value_find: str, field_find: str) -> tuple:
        query = f"SELECT * FROM {self._name_entity} WHERE {field_find} LIKE '{value_find}'"

        self._client_db.open_connection()
        try:
            entity = self._client_db.execute_dml(query)[0]
        except IndexError:
            raise NotFoundError('Данные не найдены', 404)
        self._client_db.close_connection()

        return entity

    @abstractmethod
    def add(self, *args, **kwargs):
        pass
