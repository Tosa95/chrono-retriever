import json
import pprint
import time
from datetime import datetime
from typing import Optional

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
# ENDPOINT = "http://tosahomemilan.ddns.net:8000"
ENDPOINT = "http://localhost:8000"

if __name__ == "__main__":
    client = GraphqlClient(endpoint=ENDPOINT)
    retriever = WindowsStateRetriever(ALL_SPECIALIZERS)

    prev_active = None
    last_sent: Optional[datetime] = None

    while True:
        state = retriever.retrieve_windows_state()

        if state.active_window != prev_active or last_sent is None or (
                datetime.now() - last_sent).total_seconds() > SEND_EVERY:
            data = state.dict(exclude_unset=True)
            data = to_jsonable_dict(data)
            variables = {"state": data}
            # pprint.pprint(data)

            res = client.execute(query=query, variables=variables)
            pprint.pprint(state.active_window)
            last_sent = datetime.now()

        prev_active = state.active_window
        time.sleep(0.5)
