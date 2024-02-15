import csv
from collections import defaultdict
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

import pandas as pd

from os import listdir
from pathlib import Path


def ctree():
    """One of the python gems. Making possible to have dynamic tree structure."""
    return defaultdict(ctree)


def build_leaf(name, leaf):
    """Recursive function to build desired custom tree structure"""
    res = {"name": name}

    # add children node if the leaf actually has any children
    if len(leaf.keys()) > 0:
        res["children"] = [build_leaf(k, v) for k, v in leaf.items()]

    return res


def create_result_csv(topic):
    path = f"..\\Data\\Result\\{topic}\\{topic}.csv"
    print(listdir("..\\Data\\Result"))
    df_temp = pd.read_csv(path)
    df_temp.to_csv(f".\\{topic}.csv", index=False)


def parse_data_to_output(topic):
    """The main thread composed from two parts.
    First it's parsing the csv file and builds a tree hierarchy from it.
    Second it's recursively iterating over the tree and building custom
    json-like structure (via dict).
    And the last part is just print the result
    """
    path = f".\\Data\\Result\\{topic}\\{topic}.csv"
    tree = ctree()
    # NOTE: you need to have test.csv file as neighbor to this file
    with open(path, encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for rid, row in enumerate(reader):

            # skipping first header row. remove this logic if your csv is
            # headerless
            if rid == 0:
                continue

            # usage of python magic to construct dynamic tree structure and
            # basically grouping csv values under their parents

            leaf = tree[row[1]]
            for cid in range(1, len(row)):
                leaf = leaf[row[cid - 1]]

    # building a custom tree structure
    res = []

    for name, leaf in tree.items():
        res.append(build_leaf(name, leaf))

    # printing results into the terminal

    import json

    root1 = {"name": "Twitter tweets"}
    root1["children"] = res
    with open(".\\GraphicalRepresentation\\Health.json", "w") as outfile:
        outfile.write(json.dumps(root1, indent=4))


