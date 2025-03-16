from typing import Any

import networkx as nx
import numpy as np

from app.constants import SEED_VALUE


def get_linear_threshold_top_influential_nodes(
    graph: nx.Graph,
    n_top: int,
    num_simulations: int = 100,
) -> list[Any]:
    """Find `n_top` influential nodes using the Linear Threshold algorithm.

    Utilizes the Greedy algorithm. The edges weights and the thresholds are generated
    randomly.
    """

    np.random.seed(SEED_VALUE)

    weights_mapping = _generate_edge_weights(graph)

    selected_seeds: list[Any] = []
    candidates: set[Any] = set(graph.nodes())

    for _ in range(n_top):
        best_candidate = None
        best_spread = -1.0

        for candidate in candidates - set(selected_seeds):
            current_seed_set = set(selected_seeds) | {candidate}
            spread = _estimate_spread(
                graph,
                weights_mapping,
                num_simulations,
                current_seed_set,
            )

            if spread > best_spread:
                best_spread = spread
                best_candidate = candidate

        if best_candidate is None:
            break
        selected_seeds.append(best_candidate)

    return selected_seeds


def _generate_edge_weights(graph: nx.Graph) -> dict[Any, dict[Any, float]]:
    max_weights_sum = 0.9
    weights_mapping: dict[Any, dict[Any, float]] = {}

    for node in graph.nodes():
        neighbors = list(graph.neighbors(node))

        if not neighbors:
            weights_mapping[node] = {}
            continue

        raw_weights = np.random.rand(len(neighbors))
        total = raw_weights.sum()
        weights = (raw_weights / total) * max_weights_sum

        weights_mapping[node] = dict(zip(neighbors, weights, strict=True))

    return weights_mapping


def _estimate_spread(
    graph: nx.Graph,
    weights_mapping: dict[Any, dict[Any, float]],
    n_simulations: int,
    seed_set: set[Any],
) -> float:
    total_spread = 0
    for _ in range(n_simulations):
        total_spread += _run_lt_simulation(graph, weights_mapping, seed_set)
    return total_spread / n_simulations


def _run_lt_simulation(
    graph: nx.Graph,
    weights_mapping: dict[Any, dict[Any, float]],
    seed_set: set[Any],
) -> int:
    """Run one Linear Threshold simulation.

    Each node gets a threshold sampled in [0,1].

    Parameters:
        seed_set (Set[Any]): The set of initially active nodes.
    """
    thresholds: dict[Any, float] = {v: np.random.rand() for v in graph.nodes()}

    activated: set[Any] = set(seed_set)
    newly_activated: set[Any] = set(seed_set)

    while newly_activated:
        next_activated: set[Any] = set()
        for node in graph.nodes():
            if node in activated:
                continue

            influence_sum = 0
            for neighbor in graph.neighbors(node):
                if neighbor in activated:
                    influence_sum += weights_mapping[node][neighbor]

            if influence_sum >= thresholds[node]:
                next_activated.add(node)

        newly_activated = next_activated - activated
        activated.update(newly_activated)

    return len(activated)
