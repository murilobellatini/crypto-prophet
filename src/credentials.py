"""
Credential files are loaded and stored in variables here.
"""
import os
import json
from src.paths import LOCAL_CREDENTIALS_PATH

# load facebook api data
TWITTER_BEARER_TOKEN = os.environ.get('TWITTER_BEARER_TOKEN')

# Loads GCloud Credentials
GOOGLE_CLOUD_CREDENTIALS_PATH = LOCAL_CREDENTIALS_PATH / \
    'gcloud.json'

with open(GOOGLE_CLOUD_CREDENTIALS_PATH, mode='r') as json_file:
    gcloud_credentials_dict = json.load(json_file)