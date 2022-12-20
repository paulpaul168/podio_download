import os
import pypodio2
from pypodio2 import api
import json, requests

# Replace this with the path to the JSON file containing the credentials
credentials_file = 'credentials.json'

# Replace this with the path to the text file containing the field values to search for
field_values_file = 'values.txt'

# Read the app ID and field ID from the configuration file
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
    app_id = config['app_id']
    field_id = config['field_id']
except FileNotFoundError:
    print("Error: The file 'config.json' was not found.")
    exit(1)
except KeyError as e:
    print(f"Error: The configuration file is missing the '{e}' key.")
    exit(1)

# Read the field values from the text file
with open(field_values_file, 'r') as f:
    field_values = f.read().splitlines()

# Load the credentials from the JSON file
with open(credentials_file, 'r') as f:
    credentials = json.load(f)
    client_id = credentials['client_id']
    client_secret = credentials['client_secrets']
    username = credentials['username']
    password = credentials['password']

# Authenticate with Podio
client = api.OAuthClient(
            credentials["client_id"],
            credentials["client_secrets"],
            credentials["username"],
            credentials["password"],
        )

# Set the request parameters
data = {
    'grant_type': 'password',
    'username': username,
    'password': password,
    'client_id': client_id,
    'client_secret': client_secret
}

# Make the request to the Podio OAuth2 endpoint
response = requests.post(
    'https://podio.com/oauth/token',
    data=data
)

# Extract the access token from the response
access_token = response.json()['access_token']

# Print the access token
print(access_token)

# Set the authorization header for the request
headers = {
    'Authorization': f"OAuth2 {access_token}"
}

# Set the base URL for the Podio API
api_url = 'https://api.podio.com'

count = client.Application.get_items(f"{app_id}/count")["count"]
results = []
for i in range(0, int(count / 30) + 1):
    result = client.Item.filter(
        app_id, attributes={"limit": 30, "offset": i * 30}
    )
    if "items" in result: 
        results += result["items"]

items = []
for item in results:
    if item["title"] in field_values:
        print("Apppend: " + item["title"])
        items.append(item)

for item in items:
        try:
            field_response = requests.get( f"{api_url}/item/{item['item_id']}", headers=headers)
            field_data = field_response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error: An error occurred while getting field data for item {item['item_id']}: {e}")
            continue

        if field_data['files'] == []:
            print(f"No attachmend found for item {item['item_id']} url: https://podio.com/spaceteamat/buchhaltung-2022/apps/bestellungen/items/{item['title'][1:]}")
            continue
        # Get the attachment data from the field
        try:
            attachment_data = field_data['files'][0]
        except KeyError:
            print(f"Error: No attachment found for item {item['item_id']}.")
            continue
        # Download the attachment
        attachment_url = attachment_data['link']
        try:
            attachment_response = requests.get(attachment_url, headers=headers)
        except requests.exceptions.RequestException as e:
            print(f"Error: An error occurred while downloading the attachment for item {item['item_id']}: {e}")
            continue

        # Save the attachment to a file
        try:
            with open(os.path.join("output",attachment_data['name']), 'wb') as f:
                f.write(attachment_response.content)
        except OSError as e:
            print(f"Error: An error occurred while saving the attachment for item {item['item_id']}: {e}")
            continue

        print(f"Successfully downloaded attachment for item {item['item_id']}.")
