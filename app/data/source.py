import csv
from pathlib import Path

import networkx as nx

from app.data.constants import lastfm_asia_nodes_csv_file_path


def import_lastfm_asia_graph() -> nx.Graph:
    graph = nx.Graph()
    return import_graph_from_csv(graph, lastfm_asia_nodes_csv_file_path)


def import_graph_from_csv(graph: nx.Graph, file_path: Path) -> nx.Graph:
    """Import an undirected graph from a CSV file.

    The expected CSV file format:
        node_1,node_2
        0,747
        1,4257
        ...
    """
    expected_row_length = 2

    with file_path.open("r", newline="") as f:
        reader = csv.reader(f)
        next(reader, None)

        for row in reader:
            if len(row) < expected_row_length:
                continue

            node1, node2 = int(row[0]), int(row[1])
            graph.add_edge(node1, node2)

    return graph
