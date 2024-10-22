from astrapy import DataAPIClient

# Initialize the client
client = DataAPIClient("AstraCS:ojBxOgCakUupJJQYaJQXZCiL:1ba8dc5559eed758f3c940bc045607bd3cb2834e24c11eee058b7d895629890a")
db = client.get_database_by_api_endpoint(
  "https://d307a082-ac11-47ec-a549-4a54d7ce3c41-us-east1.apps.astra.datastax.com"
)

print(f"Connected to Astra DB: {db.list_collection_names()}")

print("teste")