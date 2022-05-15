from copy import deepcopy
from datetime import datetime
from pprint import pprint
from typing import Iterable, Optional

import pymongo
from bson import ObjectId
from pymongo import MongoClient

from chrono.backend.db_connectors.db_connector import DbConnector
from chrono.model.activity_regex_filter import ActivityRegexFilter
from chrono.model.windows_state import WindowsState


class MongoDbConnector(DbConnector):

    def __init__(self, mongo_client: MongoClient, db_name: str = "chrono",
                 windows_states_collection_name: str = "windows_states"):
        self._mongo_client = mongo_client
        self._db_name = db_name
        self._windows_states_collection_name = windows_states_collection_name
        self._collection = self._mongo_client[self._db_name][self._windows_states_collection_name]

    @staticmethod
    def id_to_str(item: dict) -> dict:
        item = deepcopy(item)
        item["id"] = str(item["_id"])
        del item["_id"]
        return item

    def upsert_windows_state(self, windows_state: WindowsState) -> WindowsState:

        if windows_state.id is None:
            insert_id = self._collection.insert_one(windows_state.dict()).inserted_id
            res = self._collection.find_one({"_id": insert_id})
        else:
            self._collection.update_one({"_id": ObjectId(windows_state.id)},
                                              {"$set": windows_state.dict(exclude={"id"})})
            res = self._collection.find_one({"_id": ObjectId(windows_state.id)})
        res = self.id_to_str(res)
        return WindowsState(**res)

    def get_timestamp_filter(self, from_timestamp: datetime, to_timestamp: datetime):
        return {
            "timestamp": {
                "$gte": from_timestamp,
                "$lt": to_timestamp
            },
        }

    def apply_filter(self, filter: dict) -> Iterable[WindowsState]:
        items = self._collection.find(filter).sort("timestamp", pymongo.ASCENDING)

        items = (self.id_to_str(i) for i in items)

        items = (WindowsState(**i) for i in items)

        return items

    def get_windows_states(self, from_timestamp: datetime, to_timestamp: datetime, hostname: Optional[str] = None,
                           username: Optional[str] = None) -> Iterable[WindowsState]:

        filter = self.get_timestamp_filter(from_timestamp, to_timestamp)

        if hostname is not None:
            filter["hostname"] = hostname

        if username is not None:
            filter["username"] = username

        return self.apply_filter(filter)

    def add_re_filter(self, filter: dict, field_name: str, re_filter: Optional[str]):
        if re_filter is not None:
            filter[field_name] = {"$regex": re_filter}

    def get_windows_states_w_activity_filter(self, from_timestamp: datetime, to_timestamp: datetime,
                                             activity_filter: ActivityRegexFilter) -> Iterable[WindowsState]:

        filter = self.get_timestamp_filter(from_timestamp, to_timestamp)
        self.add_re_filter(filter, "active_window.hostname", activity_filter.hostname_re)
        self.add_re_filter(filter, "active_window.username", activity_filter.username_re)
        self.add_re_filter(filter, "active_window.name", activity_filter.name_re)
        self.add_re_filter(filter, "active_window.process_name", activity_filter.process_name_re)
        self.add_re_filter(filter, "active_window.url", activity_filter.url_re)
        self.add_re_filter(filter, "active_window.project", activity_filter.project_re)
        self.add_re_filter(filter, "active_window.branch", activity_filter.branch_re)
        self.add_re_filter(filter, "active_window.file", activity_filter.file_re)

        pprint(filter)

        return self.apply_filter(filter)
