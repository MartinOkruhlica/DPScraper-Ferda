import requests
from helper import get_auth, xml_to_dict, flatten_dict
import csv
import xml.etree.ElementTree as ET
from env import BASE_URL

def get_mkm_orders():
    all_orders = []
    start = 1
    page_size = 100

    while True:

        url = f"{BASE_URL}/orders/seller/sent/{start}"
        print(f"Calling {url}")
        response = requests.get(
            url,
            auth=get_auth(url),
            headers={"Accept": "application/json"},
            timeout=30,
            allow_redirects=False
        )

        if response.status_code == 204:
            break

        response.raise_for_status()

        root = ET.fromstring(response.text)
        page_orders = root.findall("order")
        page_orders = [
            xml_to_dict(order)
            for order in root.findall(".//order")
]

        all_orders.extend(page_orders)

        print(f"Retrieved {len(all_orders)} orders so far")

        if len(page_orders) < page_size:
            break

        start += page_size
    orders = [flatten_dict(order) for order in all_orders]
    fieldnames = list(dict.fromkeys(
    key
    for order in orders
    for key in order.keys()
))
    with open("cm_orders.csv", "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(orders)
    return

if __name__ == "__main__":
    get_mkm_orders()
