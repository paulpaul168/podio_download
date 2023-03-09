# Program to download attachments from Podio items

This program uses the PyPodio2 library to connect to the Podio API and download attachments from Podio items that match a set of field values.
Requirements

* Python 3.6 or later
* PyPodio2 library
* A Podio account with API access
* A JSON file containing the Podio API credentials (client ID, client secret, username, and password)
* A text file containing the field values to search for
* A JSON file containing the app ID and field ID to search in

Usage

* Install the PyPodio2 library by running pip install pypodio2 in the terminal. (use venv!?)
* Create a Podio account and enable API access for your account.
* Create a new app in Podio or use an existing app.
* Find the app ID and field ID to search in. You can get these values by going to the app's settings page and looking at the URL. The app ID is the number after "/app/" and the field ID is the number after "/field/".
* Create a JSON file called config.json with the following contents:

```json

{
    "app_id": "APP_ID",
    "field_id": "FIELD_ID"
}
```

Replace APP_ID and FIELD_ID with the app ID and field ID from step 4.  
  
Create a JSON file called credentials.json with the following contents:

```json

{
    "client_id": "CLIENT_ID",
    "client_secrets": "CLIENT_SECRET",
    "username": "USERNAME",
    "password": "PASSWORD"
}
```
Replace CLIENT_ID, CLIENT_SECRET, USERNAME, and PASSWORD with your Podio API credentials.  
  
Create a text file called values.txt and add the field values to search for, one value per line.  
  
Run the program by executing the following command in the terminal:  
```
python download_attachments.py
```
The program will download all attachments from items in the specified app that match the field values in values.txt. The attachments will be saved in a new directory called output.
