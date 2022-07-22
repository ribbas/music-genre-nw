from collections.abc import Iterator

import networkx


class NetworkGraph:
    def __init__(
        self,
        wrangled_data: list[
            dict[str, str | list[str] | dict[str, dict[str, int] | list[str]]]
        ],
    ) -> None:

        self.wrangled_data: list[
            dict[str, str | list[str] | dict[str, dict[str, int] | list[str]]]
        ] = wrangled_data
        self.graph: networkx.DiGraph = networkx.DiGraph()
        self.edges: list[tuple[str, str]] = []
        self.pos: dict[str, list[int]] = {}

    def get_nodes(self) -> list[tuple[str, dict[str, str]]]:

        return list(self.graph.nodes(data=True))

    def get_edges(self) -> list[tuple[str, str]]:

        return self.graph.edges()

    def get_adjacency(self) -> Iterator:

        return self.graph.adjacency()

    def set_nodes(self) -> None:

        data: dict[str, str | list[str] | dict[str, dict[str, int] | list[str]]]
        for value in self.wrangled_data:
            data = dict(name=value["genre"])
            if "other names" in value:
                data["aliases"] = value["other names"]
            self.graph.add_node(value["genre"], **data)

    def set_edges(self) -> None:

        for value in self.wrangled_data:
            if "subgenres" in value:
                for genre in value["subgenres"]:
                    self.edges.append((value["genre"], genre))
            if "derivative forms" in value:
                for genre in value["derivative forms"]:
                    self.edges.append((value["genre"], genre))
            if "fusion genres" in value:
                for genre in value["fusion genres"]:
                    self.edges.append((value["genre"], genre))
            if "stylistic origins" in value:
                for genre in value["stylistic origins"]:
                    self.edges.append((genre, value["genre"]))

    def initialize_graph(self) -> None:

        self.set_nodes()
        self.set_edges()
        self.graph.add_edges_from(self.edges)
        self.graph.remove_edges_from(networkx.selfloop_edges(self.graph))

    def generate_positions(self) -> dict[str, list[int]]:

        self.pos = networkx.drawing.nx_agraph.graphviz_layout(self.graph, prog="dot")
        return self.pos
