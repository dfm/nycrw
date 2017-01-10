#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

from bs4 import BeautifulSoup

with open("data/raw.html", "r") as f:
    soup = BeautifulSoup(f, 'html.parser')

with open("data/names.txt", "w") as f:
    for el in soup.find_all("a", {"class": "card-link"}):
        f.write(el.text + "\n")
