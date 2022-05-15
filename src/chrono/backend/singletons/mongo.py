import os
import pprint

from pymongo import MongoClient

MONGO_CLIENT = None


def get_mongo_client():
    global MONGO_CLIENT

    if MONGO_CLIENT is None:
        host = os.environ["MONGO_HOST"]
        port = os.environ["MONGO_PORT"]
        username = os.environ["MONGO_USERNAME"]
        password = os.environ["MONGO_PASSWORD"]

        pprint.pp(os.environ)

        full_url = f"mongodb://{username}:{password}@{host}:{port}"
        MONGO_CLIENT = MongoClient(full_url)

    return MONGO_CLIENT
