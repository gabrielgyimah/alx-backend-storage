#!/usr/bin/env python3
"""Insert School Module"""


def insert_school(mongo_collection, **kwargs) -> str:
    """
    Inserts a new document in a collection based on kwargs
    mongo_collection will be the pymongo collection object
    Returns the new _id 
    """

    result = mongo_collection.insert_one(kwargs)
    return (result.inserted_id)