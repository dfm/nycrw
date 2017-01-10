#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import tqdm
import time
import json
import random
import requests
from bs4 import BeautifulSoup
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

__all__ = []

with open("config_secret.json", "r") as f:
    creds = json.load(f)
auth = Oauth1Authenticator(**creds)
client = Client(auth)

with open("data/names.txt", "r") as f:
    names = f.read().splitlines()

listings = []
for base_name in tqdm.tqdm(names):
    results = client.search("New York, NY", term=base_name, limit=1)
    if not len(results.businesses):
        print("no results for '{0}'".format(base_name))
        continue
    listing = results.businesses[0]

    # Get the price
    price = None
    r = requests.get("https://www.yelp.com/biz/"+listing.id)
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.content, 'html.parser')
        elements = soup.find_all("span", {"class": "price-range"})
        if len(elements):
            price = elements[0].text
    else:
        print("return code: {0}".format(r.status_code))

    data = dict(
        id=listing.id,
        base_name=base_name,
        name=listing.name,
        price=price,
        rating=listing.rating,
        review_count=listing.review_count,
        address=", ".join(listing.location.display_address),
        categories=[c.name for c in listing.categories],
        neighborhoods=listing.location.neighborhoods,
    )
    listings.append(data)

    # Pause a bit - no need to overdo it!
    time.sleep(0.5 * random.random())

with open("data/match.json", "w") as f:
    json.dump(listings, f, sort_keys=True, indent=4, separators=(',', ': '))
