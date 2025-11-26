from typing import Dict
from C3_FastAPITour.model.tag import Tag

# simple in-memory database
_db : Dict[str, Tag] = {}

def create(tag : Tag) -> None:
    """
    Save a tag object in the in-memory DB.
    The key is the tag string itself.
    """
    _db[tag.tag] = tag


def get(tag_str : str) -> Tag:

    """
    Retrieve a Tag object by its tag string.
    Raises keyError if not found.
    """
    return _db[tag_str]