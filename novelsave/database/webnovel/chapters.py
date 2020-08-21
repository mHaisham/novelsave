from typing import List

from tinydb import where
from webnovel.models import Chapter

from ..accessors import IAccessor


class ChaptersAccess(IAccessor):
    _table_name = 'chapters'

    fields = ['no', 'id', 'title', 'paragraphs']

    def insert(self, obj):
        """
        put object without checking if it already exists

        :param obj: object to be added
        :return: None
        """
        self.table.insert(self._to_dict(obj))

    def put(self, chapter: Chapter):
        """
        put chapter with unique identifier chapter.id into database

        :param chapter: object to be added
        :return: None
        """
        self.table.upsert(self._to_dict(chapter), where('id') == chapter.id)

    def put_all(self, chapters):
        """
        put chapter with unique identifier chapter.id into database

        :param chapters: object to be added
        :return: None
        """
        for chapter in chapters:
            self.put(chapter)

    def all(self) -> List[Chapter]:
        """
        :return: all chapters
        """
        return [self._from_dict(o) for o in self.table.all()]

    def get(self, id) -> Chapter:
        """
        :param id: id of chapter
        :return: chapter with corresponding id
        :raises ValueError: if more than one value corresponds to key
        """
        docs = self.table.search(where('id') == id)
        if len(docs) == 1:
            return self._from_dict(docs[0])
        else:
            raise ValueError(f'More than one value with id: {id}')

    def _to_dict(self, chapter) -> dict:
        return {field: getattr(chapter, field) for field in ChaptersAccess.fields}

    def _from_dict(self, obj) -> Chapter:
        return Chapter(**{key: value for key, value in obj.items() if key in ChaptersAccess.fields})