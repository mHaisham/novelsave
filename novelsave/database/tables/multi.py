from typing import List

from tinydb import where

from ..accessors import IAccessor
from ...models import Chapter


class MultiClassTable(IAccessor):
    def __init__(self, db, table: str, cls, fields: List[str], identifier: str):
        super(MultiClassTable, self).__init__(db)
        self.table_name = table

        # error checks
        if identifier not in fields:
            raise ValueError("'identifier' must be a field")
        if not fields:
            raise ValueError("'fields' must not be empty")

        self.cls = cls
        self.fields = fields
        self.identifier = identifier

    def put(self, obj, check=True):
        """
        put object with unique identifier chapter.id into database

        :param obj: object to be added
        :param check: uses upsert if true
        :return: None
        """
        if check:
            self.table.upsert(self._to_dict(obj), where(self.identifier) == getattr(obj, self.identifier))
        else:
            self.table.insert(self._to_dict(obj))

    def put_all(self, objs: List):
        """
        put obj with unique identifier into database

        :param objs: object to be added
        :return: None
        """
        for obj in objs:
            self.put(obj)

    def all(self) -> List:
        """
        :return: all objects
        """
        return [self._from_dict(o) for o in self.table.all()]

    def get(self, id) -> Chapter:
        """
        :param id: unique identifier
        :return: chapter with corresponding id
        :raises ValueError: if more than one value corresponds to key
        """
        docs = self.table.search(where('id') == id)
        if len(docs) == 1:
            return self._from_dict(docs[0])
        else:
            raise ValueError(f'More than one value with id: {id}')

    def _to_dict(self, chapter) -> dict:
        return {field: getattr(chapter, field) for field in self.fields}

    def _from_dict(self, obj) -> Chapter:
        return self.cls(**{key: value for key, value in obj.items() if key in self.fields})
