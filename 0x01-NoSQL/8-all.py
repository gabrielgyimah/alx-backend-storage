#!/usr/bin/env python3
"""List All module"""
import pymongo


def list_all(mongo_collection) -> list:
    """
    Llists all documents in a collection
    Return an empty list if no document in the collection
    mongo_collection will be the pymongo collection object
    """
    cursor = mongo_collection.find()
    docs = [doc for doc in cursor]
    return docs