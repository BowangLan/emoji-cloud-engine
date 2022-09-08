import os
from dataclasses import dataclass, field
from PIL import Image

from .config import data_dir


@dataclass
class EmojiItem:

    unicode: str
    weight: float
    vendor: str
    _im: Image.Image = field(default=None, init=False)

    def exists(self) -> bool:
        """Check if the current emoji item instance exists
        """
        return os.path.exists(self.fullpath)

    @property
    def fullpath(self) -> str:
        return os.path.join(data_dir, self.vendor, "%s.png" % self.unicode) 

    @property
    def image(self):
        if not self._im:
            self._im = Image.open(self.fullpath).convert("RGBA")
        return self._im



class EmojiManager:


    @staticmethod
    def check_exists(unicode: str, vendor: str) -> bool:
        """Check if an emoji with a given unicode and vendor exists

        Args:
            unicode (str): unicode of the emoji
            vendor (str): vendor of the emoji
        """
        path = os.path.join(data_dir, vendor, "%s.png" % unicode)
        return os.path.exists(path)


    @staticmethod
    def create_list_from_single_vendor(items: dict[str, float], vendor: str) -> list[EmojiItem]:
        """Create a list of EmojiItem objects with the same vendor from a dictionary of unicodes and weights.

        Args:
            items (dict[str, float]): a dictionary of emoji unicode and their corresponding weight
            vendor (str): a shared vendor

        Returns:
            a list of existing EmojiItems
        """
        e_list = [
            EmojiItem(unicode=u, weight=items[u], vendor=vendor) 
            for u in items.keys()
        ]
        return EmojiManager.filter_exist(e_list)


    @staticmethod
    def create_list_from_multiple_vendor(items: list) -> list[EmojiItem]:
        """Create a list of EmojiItem objects from a list of dictionaries. 
        These dictionaries must have the following keys:
         - 'unicode' (str) - unicode of the emoji
         - 'vendor' (str) - vendor of the emoji
         - 'weight' (float) - weight of the emoji

        Args:
            items (list): a list of dictionaries described above

        Returns:
            list[EmojiItem]
        """
        e_list = [
            EmojiItem(unicode=e['unicode'], weight=e['weight'], vendor=e['vendor'])
            for e in items
        ]
        return EmojiManager.filter_exist(e_list)


    @staticmethod
    def filter_exist(items: list[EmojiItem]) -> list[EmojiItem]:
        """Filter a list of EmojiItem objects by removing the non-existing ones.

        Args:
            items (list[EmojiItem]): _description_

        Returns:
            list[EmojiItem]: _description_
        """
        return list(filter(lambda e: e.exists(), items))