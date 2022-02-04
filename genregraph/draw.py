#!/usr/bin/env python
# -*- coding: utf-8 -*-

import plotly.graph_objects as go


class GraphPlotter:
    def __init__(self, pos: dict, nodes: list, edges: list, adjacency: list) -> None:

        self.pos: dict = pos
        self.nodes: list = nodes
        self.edges: list = edges
        self.adjacency: list = adjacency

    def draw(self):

        edge_x = []
        edge_y = []
        for edge in self.edges:
            x0, y0 = self.pos[edge[0]]
            x1, y1 = self.pos[edge[1]]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=0.5, color="#888"),
            hoverinfo="none",
            mode="lines",
        )

        node_x = []
        node_y = []
        for node in self.nodes:
            x, y = self.pos[node]
            node_x.append(x)
            node_y.append(y)

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers",
            hoverinfo="text",
            marker=dict(
                showscale=True,
                # colorscale options
                #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale="YlGnBu",
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title="Node Connections",
                    xanchor="left",
                    titleside="right",
                ),
                line_width=2,
            ),
        )

        node_adjacencies = []
        node_text = []
        for node, adjacencies in enumerate(self.adjacency):
            node_adjacencies.append(len(adjacencies[1]))
            node_text.append(
                f"""{self.nodes[adjacencies[0]].get('name',adjacencies[0])}
                <br># of connections: {len(adjacencies[1])}"""
            )

        node_trace.marker.color = node_adjacencies
        node_trace.text = node_text

        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title="<br>Network graph made with Python",
                titlefont_size=16,
                showlegend=False,
                hovermode="closest",
                margin=dict(b=20, l=5, r=5, t=40),
                annotations=[
                    dict(
                        text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                        showarrow=False,
                        xref="paper",
                        yref="paper",
                        x=0.005,
                        y=-0.002,
                    )
                ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            ),
        )
        fig.show()
