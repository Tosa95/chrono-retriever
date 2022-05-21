import json
import logging
import pprint
import os
import time
from datetime import datetime
from typing import Optional

from click._compat import open_stream

from chrono.model.windows_state import WindowsState
from chrono.retrievers.window_specializer import ALL_SPECIALIZERS
from chrono.retrievers.windows_state_retriever import WindowsStateRetriever

from python_graphql_client import GraphqlClient

# Instantiate the client with an endpoint.


# Create the query string and variables required for the request.
from chrono.utils.to_jsonable_dict import to_jsonable_dict

query = """
    mutation windowsState($state: WindowsStateInput) {
        windows_state(state:$state) {
            id
        }
    }
"""

SEND_EVERY = 30.0
ENDPOINT = "http://tosahomemilan.ddns.net:8000"
# ENDPOINT = "http://localhost:8000"

CACHE_FILE_LOCATION = os.path.join(os.path.dirname(__file__), "cache.json")
TO_BE_SENT = []

retriever = WindowsStateRetriever(ALL_SPECIALIZERS)
last_sent: Optional[datetime] = None
prev_active = None


def retrieve_windows_state():
    global last_sent
    global prev_active

    state = retriever.retrieve_windows_state()

    if state.active_window != prev_active or last_sent is None or (
            datetime.now() - last_sent).total_seconds() > SEND_EVERY:
        last_sent = datetime.now()

        TO_BE_SENT.append(state)

        prev_active = state.active_window

        print("RETRIEVED")
        pprint.pprint(state)
        print()


if __name__ == "__main__":
    client = GraphqlClient(endpoint=ENDPOINT, timeout=(0.5, 30))

    if os.path.exists(CACHE_FILE_LOCATION):
        try:
            with open(CACHE_FILE_LOCATION, "rt") as f:
                TO_BE_SENT = [WindowsState(**d) for d in json.load(f)]
        except:
            logging.info("Unable to load json file")

    while True:
        retrieve_windows_state()
        try:

            while len(TO_BE_SENT) > 0:
                retrieve_windows_state()
                print(len(TO_BE_SENT))
                state = TO_BE_SENT[0]

                data = state.dict(exclude_none=True)
                data = to_jsonable_dict(data)

                variables = {"state": data}
                # pprint.pprint(data)

                res = client.execute(query=query, variables=variables)
                print("SENT")
                print(res)
                if "active_window" in data:
                    pprint.pprint(data["active_window"])
                print()

                del TO_BE_SENT[0]

            if os.path.exists(CACHE_FILE_LOCATION):
                os.remove(CACHE_FILE_LOCATION)

        except Exception as e:
            print(e)
            with open(CACHE_FILE_LOCATION, "wt") as f:
                json.dump([to_jsonable_dict(state.dict(exclude_none=True)) for state in TO_BE_SENT], f)

        time.sleep(0.5)
