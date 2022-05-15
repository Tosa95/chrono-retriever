import pprint
import time

from chrono.retrievers.window_specializer import ALL_SPECIALIZERS
from chrono.retrievers.windows_state_retriever import WindowsStateRetriever

from python_graphql_client import GraphqlClient

# Instantiate the client with an endpoint.


# Create the query string and variables required for the request.
query = """
    mutation windowsState($state: WindowsStateInput) {
        windows_state(state:$state) {
            id
        }
    }
"""

if __name__ == "__main__":
    client = GraphqlClient(endpoint="http://192.168.1.78:8000")
    retriever = WindowsStateRetriever(ALL_SPECIALIZERS)

    prev_active = None

    while True:
        state = retriever.retrieve_windows_state()

        if state.active_window != prev_active:
            data = state.dict(exclude_unset=True)
            variables = {"state": data}
            # pprint.pprint(data)

            res = client.execute(query=query, variables=variables)
            print(res)
            pprint.pprint(state.active_window)

        prev_active = state.active_window
        time.sleep(0.5)
