"""Functions to create reference model graphs."""

import networkx as nx

from app.constants import SEED_VALUE


def create_er_graph(nodes: int, edges: int) -> nx.Graph:
    p: float = (2 * edges) / (nodes * (nodes - 1)) if nodes > 1 else 0
    return nx.erdos_renyi_graph(nodes, p, seed=SEED_VALUE)


def create_ba_graph(nodes: int, edges: int) -> nx.Graph:
    _edges: int = max(1, round(edges / nodes))
    if nodes <= _edges:
        raise ValueError("Can not create BA graph")
    return nx.barabasi_albert_graph(nodes, _edges, seed=SEED_VALUE)


def create_ws_graph(nodes: int, edges: int) -> nx.Graph:
    neighbours: int = round(2 * edges / nodes)
    if neighbours % 2 != 0:
        neighbours += 1

    neighbours = max(2, neighbours)
    if neighbours >= nodes:
        neighbours = nodes - 1 if (nodes - 1) % 2 == 0 else nodes - 2

    if nodes <= neighbours:
        raise ValueError("Can not create WS graph")
    return nx.watts_strogatz_graph(nodes, neighbours, 0.1, seed=SEED_VALUE)
