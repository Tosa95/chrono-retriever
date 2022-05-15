import os

from ariadne import make_executable_schema, gql
from ariadne.asgi import GraphQL

from chrono.backend.mutations import mutation
from chrono.backend.queries import query
from chrono.backend.types.timestamp import timestamp
import chrono.backend.queries.windows_states_resolver
import chrono.backend.queries.activity_stats_resolver
import chrono.backend.mutations.windows_state_resolver

with open(os.path.join(os.path.dirname(__file__), "schema.graphql"), "rt") as schema_file:
    type_defs = gql(schema_file.read())

schema = make_executable_schema(type_defs, [mutation, query, timestamp])

app = GraphQL(schema, debug=True)
