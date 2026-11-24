from requests_oauthlib import OAuth1
import csv
import unicodedata
import re
from env import APP_SECRET, APP_TOKEN, ACCESS_SECRET, ACCESS_TOKEN, BASE_URL

def xml_to_dict(element):

    result = {}

    for child in element:

        # If the element has children, recursively process them
        if len(child):
            value = xml_to_dict(child)

        # Otherwise, retrieve its text
        else:
            value = child.text.strip() if child.text else None

        # Handle repeated XML elements
        if child.tag in result:
            if not isinstance(result[child.tag], list):
                result[child.tag] = [result[child.tag]]

            result[child.tag].append(value)

        else:
            result[child.tag] = value

    return result

def read_csv(filename):
    with open(filename, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        return list(reader)

def get_auth(url):
    return OAuth1(
        client_key=APP_TOKEN,
        client_secret=APP_SECRET,
        resource_owner_key=ACCESS_TOKEN,
        resource_owner_secret=ACCESS_SECRET,
        signature_method="HMAC-SHA1",
        realm=url
    )

def flatten_dict(data, parent_key="", separator="_"):
    items = {}

    for key, value in data.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key

        if isinstance(value, dict):
            items.update(flatten_dict(value, new_key, separator))

        else:
            items[new_key] = value

    return items

def normalize_address(address):
    address = address.lower()

    # Normalize German characters and other Unicode characters
    address = unicodedata.normalize("NFKD", address)
    address = "".join(
        char for char in address
        if not unicodedata.combining(char)
    )

    # Remove punctuation
    address = re.sub(r"[^\w\s]", " ", address)

    # Remove unnecessary whitespace
    address = " ".join(address.split())

    return address