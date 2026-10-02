# use this to open the browser, then log into DeutschePost
# "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\playwright-debug"

from playwright.sync_api import sync_playwright
import time
import csv


with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")

    context = browser.contexts[0]
    page = context.pages[0]
    html = page.content()
    order_ids = []
    orders_url = page.url
    page.wait_for_selector("li.order")
    orders = page.locator("li.order")
    count = orders.count()

    for i in range(count):
        order = orders.nth(i)
        bestelldatum = order.locator(
        "div.order-card:has-text('Bestelldatum') dd.oh-value").first.inner_text()
        order_id = order.locator(".orderNumber .oh-value").inner_text()
        checked_ids = set()
        with open("checked_orders.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                checked_ids.add(row["order_id"])
            if order_id in checked_ids:
                continue
            else:
                with open("checked_orders.csv", "a", newline="", encoding="utf-8") as file2:
                    writer = csv.writer(file2)
                    writer.writerow([order_id])
                order.locator(".order-card").click()
                page.wait_for_load_state("domcontentloaded")

        tracking_link = page.locator("a:has-text('Trackinginformationen')")
        if  tracking_link.count() > 0:
            tracking_href =  tracking_link.get_attribute("href")
            base = "https://shop.deutschepost.de"
            tracking_url = base + tracking_href
            page.goto(tracking_url)
            page.wait_for_load_state("domcontentloaded")
            rows = page.locator("tr.table__tr:has(td)")
            count = rows.count()
            results = []
            for i2 in range(count):
                row = rows.nth(i2)
                empfaenger = row.locator('td[data-title="Empfänger"]').inner_text().split()
                customer = " ".join(empfaenger)
                href = row.locator('td[data-title="Sendungsnummer"] a').get_attribute("href")[-20:]
                results.append({
                    "empfaenger": customer,
                    "sendungsnummer_href": href
                })
            with open("trackings.csv", "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                for item in results:
                    writer.writerow([item["empfaenger"], item["sendungsnummer_href"], bestelldatum])
            time.sleep(2)
            print("Going back from tracking page...")
            page.go_back(wait_until="commit")
            print("Back to order page:", page.url)
            print("Going back from order page...")
            page.go_back(wait_until="commit")
            print("Back to order list:", page.url)
            page.wait_for_selector("li.order")
        else:
            print("Going back from order page...")
            page.go_back(wait_until="commit")
            print("Back to order list:", page.url)
            page.wait_for_selector("li.order")

