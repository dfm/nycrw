#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

from bs4 import BeautifulSoup

with open("data/raw.html", "r") as f:
    soup = BeautifulSoup(f, 'html.parser')

with open("data/names.txt", "w") as f:
    for card in soup.find_all("div", {"class": "card-body"}):
        for name, meals in zip(card.find_all("h3", {"class": "card-title"}),
                               card.find_all("small", {"class": "meals"})):
            f.write(name.text + "\t" + meals.text + "\n")
