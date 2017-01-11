#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import tqdm
import time
import json
import foursquare

with open("foursquare.secret.json", "r") as f:
    creds = json.load(f)
client = foursquare.Foursquare(version="20160110", **creds)

with open("data/match.yelp.json", "r") as f:
    yelp = json.load(f)

listings = []
for y in tqdm.tqdm(yelp):
    base_name = y["name"]
    try:
        results = client.venues.search(params=dict(
            near=y["address"],
            query=base_name,
            limit=1,
            categoryId="4d4b7105d754a06374d81259",
        ))
    except (foursquare.FailedGeocode, foursquare.ParamError):
        results = client.venues.search(params=dict(
            near="New York, NY",
            query=base_name,
            limit=1,
            categoryId="4d4b7105d754a06374d81259",
        ))

    if not len(results["venues"]):
        print("no results for '{0}'".format(base_name))
        continue
    listing = results["venues"][0]
    detail = client.venues(listing["id"])["venue"]

    data = dict(
        id=detail["id"],
        yelp_id=y["id"],
        base_name=y["base_name"],
        yelp_name=base_name,
        name=detail["name"],
        price=detail.get("price", {}).get("tier", None),
        rating=detail.get("rating", None),
        review_count=detail.get("ratingSignals", None),
        address=", ".join(listing["location"].get("formattedAddress", [])),
        categories=[c["name"] for c in detail["categories"]],
        stats=detail["stats"],
    )
    listings.append(data)

with open("data/match.foursquare.json", "w") as f:
    json.dump(listings, f, sort_keys=True, indent=4, separators=(',', ': '))
