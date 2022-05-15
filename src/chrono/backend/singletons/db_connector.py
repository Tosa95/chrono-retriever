from typing import Optional

from chrono.backend.db_connectors.db_connector import DbConnector
from chrono.backend.db_connectors.mongo_db_connector import MongoDbConnector
from chrono.backend.singletons.mongo import get_mongo_client

DB_CONNECTOR: Optional[DbConnector] = None


def get_db_connector() -> DbConnector:
    global DB_CONNECTOR

    if DB_CONNECTOR is None:
        DB_CONNECTOR = MongoDbConnector(get_mongo_client())

    return DB_CONNECTOR
