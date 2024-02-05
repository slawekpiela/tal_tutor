import requests
import base64

from requests.auth import HTTPBasicAuth
from configuration import api_sa_key, api_sa_secret

# this is for SMSsouthafrica.coc.za
url = "https://rest.mymobileapi.com/v1/Balance"


# Replace these with your actual client_id and secret_id
client_id = api_sa_key
secret_id = api_sa_secret


credentials = f"{client_id}:{secret_id}".encode('utf-8')

encoded_credentials = base64.b64encode(credentials).decode('utf-8')

headers = {
    "Authorization": f"Basic {encoded_credentials}",
    "accept": "application/json"
}



response = requests.get(url, headers=headers)

print(response.text)

# apiKey = api_sa_key
# apiSecret = api_sa_secret
#
# basic = HTTPBasicAuth(apiKey, apiSecret)
#
# sendRequest = {
#     "messages": [{"content": "Hello SMS World from Python", "destination": "0648032037"}]
# }
#
# try:
#     sendResponse = requests.post("https://rest.mymobileapi.com/bulkmessages",
#                                  auth=basic,
#                                  json=sendRequest)
#
#     if sendResponse.status_code == 200:
#         print("Success:")
#         print(sendResponse.json())
#     else:
#         print("Failure:")
#         print(sendResponse.json())
# except Exception as e:
#     print(e)