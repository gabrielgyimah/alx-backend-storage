#!/usr/bin/env python3
"""Nginx Log Module"""


from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['logs']
collection = db['nginx']

total_logs = collection.count_documents({})
print(f"first line: {total_logs} logs where {total_logs} is the number of documents in this collection")

http_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
print("second line: Methods:")
for method in http_methods:
    count = collection.count_documents({"method": method})
    print(f"\t{count} {method} requests")

status_count = collection.count_documents({"method": "GET", "path": "/status"})
print(f"one line: {status_count} documents with method=GET and path=/status")

client.close()