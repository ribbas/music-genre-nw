#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from math import log10
from time import time

import networkx as nx

from config import DATA_PATH
from util import dump_json, read_json


def make_edge_trace():

    edge_trace = {
        "x": [],
        "y": [],
        "line": {
            "width": 0.5,
            "color": "#888",
        },
        "hoverinfo": "none",
        "mode": "lines",
        "type": "scatter",
    }

    for edge in data["edges"]:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace["x"] += [x0, x1, None]
        edge_trace["y"] += [y0, y1, None]

    return edge_trace


def make_node_trace():

    node_trace = {
        "x": [],
        "y": [],
        "connections": [],
        "text": [],
        "mode": "markers",
        "hoverinfo": "text",
        "marker": {
            "showscale": True,
            "colorscale": "YIOrRd",
            "reversescale": True,
            "color": [],
            "size": 15,
            "colorbar": {
                "thickness": 12,
                "title": "Subgenres",
                "titleside": "right",
                "xanchor": "left",
                "tickvals": [0.0, 1.0],
                "ticktext": ["Unparsed", "0"],
                "ticks": "outside"
            },
            "line": {
                "width": 2
            }
        }
    }

    for node in data["nodes"]:
        x, y = pos[node]
        node_trace["x"].append(x)
        node_trace["y"].append(y)

    keys = data["subgenres"].keys()
    for node in graph.adjacency():
        num_children = 0
        node_info = node[0].title()
        if node[0] in keys:
            num_children = data["subgenres"][node[0]]["num_children"]
            node_trace["connections"].append(
                data["subgenres"][node[0]]["origins"] +
                data["subgenres"][node[0]]["children"]
            )
            node_trace["marker"]["color"].append(
                log10(num_children + 1) * 10 + 10)
            node_info += "<br>" + str(num_children) + " subgenres"
        else:
            node_trace["connections"].append([])
            node_trace["marker"]["color"].append(0)
        node_trace["text"].append(node_info)

    return node_trace


if __name__ == "__main__":

    data = read_json(DATA_PATH + "/data.json")

    graph = nx.DiGraph()
    graph.add_nodes_from(data["nodes"])
    graph.add_edges_from(data["edges"])

    print("Generating coordinates for network graph dot layout...")
    start = time()
    pos = nx.drawing.nx_agraph.graphviz_layout(graph, prog="dot")
    print("Layout took {:.2f}s to generate".format(time() - start))

    layout = {
        "title": "<br>Music Genre Network Graph",
        "titlefont": {
            "size": 16
        },
        "showlegend": False,
        "hovermode": "closest",
        "margin": {
            "b": 20,
            "l": 5,
            "r": 5,
            "t": 40
        },
        "xaxis": {
            "showgrid": False,
            "zeroline": False,
            "showticklabels": False
        },
        "yaxis": {
            "showgrid": False,
            "zeroline": False,
            "showticklabels": False
        },
        "annotations": [{
            "text": "<a href='https://github.com/sabbirahm3d/music-genre-nw'>What is this?</a> | <a href='https://github.com/sabbirahm3d/music-genre-nw'>Repository</a>",
            "showarrow": False,
            "xref": "paper",
            "yref": "paper",
            "x": 0.005,
            "y": -0.002
        }],
    }

    dump_json(
        DATA_PATH + "plot_data.json",
        {"layout": layout,
         "data": [make_edge_trace(), make_node_trace()]}
    )
