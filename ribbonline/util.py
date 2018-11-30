import json


def has_emoji(string, emoji):
    return emoji in string


def load_credentials(filename='credentials.json'):
    with open(filename, 'rt') as f:
        credentials = json.load(fp=f)
    return credentials
