from airtable import Airtable
from configuration import base_id, table_dictionary, airtable_token

airtable = Airtable(base_id, table_dictionary, airtable_token)

# Fetch all records from Airtable
airtable_records = airtable.get_all()
# Provided Airtable records
# airtable_records = [
#     {'id': 'recXuY35LTgrIGeTF', 'createdTime': '2024-02-16T19:59:49.000Z', 'fields': {'UID': 1, 'create_date': '2024-02-16T19:59:49.000Z', 'keyword': 'hola', 'update_date': '2024-02-28T01:52:06.000Z'}},
#     {'id': 'recaWgENm9yEjxloh', 'createdTime': '2024-02-16T19:59:49.000Z', 'fields': {'UID': 3, 'create_date': '2024-02-16T19:59:49.000Z'}},  # This record doesn't have a keyword field
#     {'id': 'recj0WGlSJceOfHRC', 'createdTime': '2024-02-16T19:59:49.000Z', 'fields': {'UID': 2, 'create_date': '2024-02-16T19:59:49.000Z'}}
# ]

# Extract keywords from Airtable records
airtable_keywords = [record['fields'].get('keyword') for record in airtable_records if 'keyword' in record['fields']]

# Your JSON data
json_data = [
    {"keyword": "hello"},
    {"keyword": "hola"},
    {"keyword": "hellon"},
]

# Remove items from json_data that have a keyword matching any keyword in airtable_keywords
filtered_json_data = [item for item in json_data if item['keyword'] not in airtable_keywords]

print(filtered_json_data)
