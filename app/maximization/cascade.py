from typing import Any

import networkx as nx
import numpy as np

from app.constants import SEED_VALUE


def get_independent_cascade_top_influential_nodes(
    graph: nx.Graph,
    n_top: int,
    candidates: set[Any],
    num_simulations: int = 100,
    p: float = 0.1,
) -> list[Any]:
    """Find `n_top` influential nodes among `candidates` using Independent Cascade.

    Utilizes the Greedy algorithm. The probabilities are fixed to `p`.
    """
    np.random.seed(SEED_VALUE)

    probabilities_mapping = _generate_edge_probabilities(graph, p)

    selected_seeds: list[Any] = []

    for _ in range(n_top):
        best_candidate = None
        best_spread = -1.0

        for candidate in candidates - set(selected_seeds):
            current_seed_set = set(selected_seeds) | {candidate}
            spread = _estimate_spread(
                graph,
                probabilities_mapping,
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


def _generate_edge_probabilities(
    graph: nx.Graph,
    p: float = 0.1,
) -> dict[Any, dict[Any, float]]:
    """Generate fixed edge probabilities mapping."""
    probabilities_mapping: dict[Any, dict[Any, float]] = {}

    for node in graph.nodes():
        neighbors = list(graph.neighbors(node))
        probabilities_mapping[node] = dict.fromkeys(neighbors, p)

    return probabilities_mapping


def _estimate_spread(
    graph: nx.Graph,
    probabilities_mapping: dict[Any, dict[Any, float]],
    n_simulations: int,
    seed_set: set[Any],
) -> float:
    total_spread = 0
    for _ in range(n_simulations):
        total_spread += _run_ic_simulation(graph, probabilities_mapping, seed_set)
    return total_spread / n_simulations


def _run_ic_simulation(
    graph: nx.Graph,
    probabilities_mapping: dict[Any, dict[Any, float]],
    seed_set: set[Any],
) -> int:
    """Run one simulation of the Independent Cascade model."""
    activated: set[Any] = set(seed_set)
    new_active: set[Any] = set(seed_set)

    while new_active:
        next_active: set[Any] = set()

        for node in new_active:
            for neighbor in graph.neighbors(node):
                if (
                    neighbor not in activated
                    and np.random.rand() < probabilities_mapping[node][neighbor]
                ):
                    next_active.add(neighbor)

        new_active = next_active - activated
        activated.update(new_active)

    return len(activated)
