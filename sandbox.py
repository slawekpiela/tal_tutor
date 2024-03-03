import json
import requests
from configuration import base_id, airtable_token, table_dictionary
import json
import requests
from configuration import base_id, airtable_token, table_dictionary
import streamlit as st
from airtable import Airtable
from configuration import airtable_token, base_id, table_dictionary
# Example JSON data

# # json_data = [
# #     {"fields": {"keyword": "John", "transcription":"ˈɜr.li"}},
# #     {"fields": {"keyword": "Alice", "transcription":"ˈɜr.li"}},
# #
# # ]
# #{"fields": " "}, {"fields": " "}, {"fields": "}"}, {"fields": "\n"}, {"fields": "]"}]}}
my_json={'records': [{'fields': {'keyword': 'Off', 'transcription': '/ɔf/', 'translation': '-', 'study_status': '---',
                         'user': 'slawek', 'no_of_tries': 0, 'group': ''}}, {
                 'fields': {'keyword': 'Early', 'transcription': '/ˈɜrli/', 'translation': '-', 'study_status': '---',
                            'user': 'slawek', 'no_of_tries': 0, 'group': ''}}, {
                 'fields': {'keyword': 'In', 'transcription': '/ɪn/', 'translation': '-', 'study_status': '---',
                            'user': 'slawek', 'no_of_tries': 0, 'group': ''}}, {
                 'fields': {'keyword': 'The', 'transcription': '/ðə/', 'translation': '-', 'study_status': '---',
                            'user': 'slawek', 'no_of_tries': 0, 'group': ''}}, {
                 'fields': {'keyword': 'Morning', 'transcription': '/ˈmɔrnɪŋ/', 'translation': '-',
                            'study_status': '---', 'user': 'slawek', 'no_of_tries': 0, 'group': ''}}, {
                 'fields': {'keyword': 'Towards', 'transcription': '/təˈwɔrdz/', 'translation': '-',
                            'study_status': '---', 'user': 'slawek', 'no_of_tries': 0, 'group': ''}}, {
                 'fields': {'keyword': 'Moon', 'transcription': '/mun/', 'translation': '-', 'study_status': '---',
                            'user': 'slawek', 'no_of_tries': 0, 'group': ''}}, {
                 'fields': {'keyword': 'He', 'transcription': '/hiː/', 'translation': '-', 'study_status': '---',
                            'user': 'slawek', 'no_of_tries': 0, 'group': ''}}, {
                 'fields': {'keyword': 'Knew', 'transcription': '/njuː/', 'translation': '-', 'study_status': '---',
                            'user': 'slawek', 'no_of_tries': 0, 'group': ''}}, {
                 'fields': {'keyword': 'That', 'transcription': '/ðæt/', 'translation': '-', 'study_status': '---',
                            'user': 'slawek', 'no_of_tries': 0, 'group': ''}}, {
                 'fields': {'keyword': 'Going', 'transcription': '/ˈɡoʊɪŋ/', 'translation': '-', 'study_status': '---',
                            'user': 'slawek', 'no_of_tries': 0, 'group': ''}}, {
                 'fields': {'keyword': 'There', 'transcription': '/ˈðɛr/', 'translation': '-', 'study_status': '---',
                            'user': 'slawek', 'no_of_tries': 0, 'group': ''}}, {
                 'fields': {'keyword': 'Will', 'transcription': '/wɪl/', 'translation': '-', 'study_status': '---',
                            'user': 'slawek', 'no_of_tries': 0, 'group': ''}}, {
                 'fields': {'keyword': 'Be', 'transcription': '/bi/', 'translation': '-', 'study_status': '---',
                            'user': 'slawek', 'no_of_tries': 0, 'group': ''}}, {
                 'fields': {'keyword': 'Exciting', 'transcription': '/ɪkˈsaɪtɪŋ/', 'translation': '-',
                            'study_status': '---', 'user': 'slawek', 'no_of_tries': 0, 'group': ''}}]}

# print(json_data)
# from airtable import Airtable
#
# # Assuming base_id, table_dictionary, and airtable_token are defined
# airtable = Airtable(base_id, table_dictionary, airtable_token)
#
# # Iterate through each record in the provided JSON data
# for record in json_data['records']:
#     # Extract the 'fields' dictionary, which contains the actual data to be inserted
#     fields = record['fields']
#
#     # Use the 'fields' dictionary directly when inserting into Airtable
#     response = airtable.insert(fields)
#
#     # Print the response to confirm the insertion
#     print(response)
#     print('-------------------------------')
airtable = Airtable(base_id, table_dictionary, airtable_token)

# Iterate through each record in the provided JSON data
for record in my_json['records']:
    # Extract the 'fields' dictionary, which contains the actual data to be inserted
    fields = record['fields']

    # Use the 'fields' dictionary directly when inserting into Airtable
    response = airtable.insert(fields)
    print(response)
