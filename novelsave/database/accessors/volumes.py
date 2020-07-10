from typing import List

from .keyvalue import KeyValueAccessor


class VolumesAccess(KeyValueAccessor):
    table_name = 'volume'

    def set_volume(self, volume_name: str, ids: List[int]):
        """
        sets volume ids

        :param volume_name: name of volume
        :param ids: ids to be set for volume
        :return: None
        """
        self.put(volume_name, ids)