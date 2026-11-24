from helper import read_csv
from helper import normalize_address
import csv

def match_orders():
    orders = {}
    trackings = {}
    matched_orders = []
    mkm_orders = read_csv("cm_orders.csv")
    dp_trackings = read_csv("trackings.csv")
    for order in mkm_orders:
        if order["shippingMethod_isInsured"] == "true" and order["trackingNumber"] == "":
            orders[order["idOrder"]] = normalize_address(order["shippingAddress_name"] + " " + order["shippingAddress_street"] + " " + order["shippingAddress_zip"] + " " + order["shippingAddress_city"])
    for tracking in dp_trackings:
        trackings[normalize_address(tracking["Name"])] = tracking["Tracking"]
    for order in orders:
        tracking = trackings.get(orders[order], "Unmatched")
        matched_orders.append([order, tracking, orders[order]])
    with open("matched_orders.csv", "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(["order_id", "tracking", "address"])
            writer.writerows(matched_orders)
    return

if __name__ == "__main__":
     match_orders()