import json 
import time
import requests
import random
import pprint

from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin




UA_STRINGS = [
    "Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36\
        (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G996U Build/QP1A.190711.020; wv) AppleWebKit/537.36\
        (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15\
        (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1"
]

HEADERS = {
    'User-Agent': random.choice(UA_STRINGS),
    'Accept-Language': 'en-US, en;q=0.5'
}

def get_categories(url):
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')

    items = soup.select("div a.BoxLink-sc-1f5ptnf-0")
    categories = [{"title": item.select_one("h4 div.Text__TextBase-sc-1cait9d-0-div").text, "url": urljoin(url, item.get("href"))} for item in items]
    return categories


def get_homes(url):
    result = []
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')

    items = soup.select("li.Grid__CellBox-sc-144isrp-0")
    for item in items:
        try:
            script = json.loads(item.select_one("script").text)
            result.append({
                "address": {
                    "streetAddress": script["address"]["streetAddress"],
                    "addressLocality": script["address"]["addressLocality"],
                    "addressRegion": script["address"]["addressRegion"],
                    "postalCode": script["address"]["postalCode"],
                },
                "geo": {
                    "latitude": script["geo"]["latitude"],
                    "longitude": script["geo"]["longitude"]
                },
                "url": urljoin(url, item.select_one("div a.Anchor__StyledAnchor-sc-5lya7g-1").get("href")),
            })
        except:
            pass
    return result


def get_details():
    url = "https://www.trulia.com/p/ca/riverside/8576-brotchie-ln-riverside-ca-92509--2608197341"
    
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')

    script = soup.select_one("#__next  div.BodyContainer-sc-1v15goo-0 script[data-testid=hdp-seo-product-schema]").text
    script = json.loads(script)
    details = {
        "name": script["name"], 
        "description": script["description"],
        "image": script["image"],
        "price": script["offers"]["price"],
        "availability": script["offers"]["availability"],
        "priceCurrency": script["offers"]["priceCurrency"],
        "brand": script["brand"]["name"],
        "review": script["review"],
        "additionalProperty": [{"name": data["name"], "value": data["value"]} for data in script["additionalProperty"]]
    }
    return details


def main():
    url = "https://www.trulia.com/"
    categories = get_categories(url)



print(get_homes("https://www.trulia.com/CA/Jurupa_Valley/"))