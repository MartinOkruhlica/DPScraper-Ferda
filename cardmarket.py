import requests
import time
from helper import read_csv, get_auth
from env import BASE_URL

def update_tracking(order_id, tracking_number):
    url = f"{BASE_URL}/order/{order_id}/tracking"
    xml_body = f"""<?xml version="1.0" encoding="UTF-8"?>
    <request>
        <trackingNumber>{tracking_number}</trackingNumber>
    </request>"""
    headers = {
        "Content-Type": "application/xml",
        "Accept": "*/*"
    }
    response = requests.put(
        url,
        auth=get_auth(url),
        headers=headers,
        data=xml_body.encode("utf-8"),
        timeout=30
    )
    response.raise_for_status()
    time.sleep(1)
    return response

def update_tracking_numbers_from_file():
    matched_orders = read_csv("matched_orders.csv")
    for order in matched_orders:
        if order["tracking"] == "Unmatched":
            continue
        else:
            tracking_number = order["tracking"]
        try:
            print(f"updating tracking for order {order["order_id"]}")
            r = update_tracking(order["order_id"], tracking_number)
            r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error")
            print(errh.args[0])


if __name__ == "__main__":
    update_tracking_numbers_from_file()