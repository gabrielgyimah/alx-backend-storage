#!/usr/bin/env python3
"""Schools By Topic Module"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of school having a specific topic
    mongo_collection will be the pymongo collection object
    topic (string) will be topic searched
    """

    return mongo_collection.find({'topics': {'$elemMatch': {'$eq': topic}}})