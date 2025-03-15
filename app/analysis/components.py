import networkx as nx
import numpy as np
import structlog

from app.analysis.dtos import ConnectedComponentsStats


def calculate_connected_components_analysis(graph: nx.Graph) -> None:
    logger: structlog.stdlib.BoundLogger = structlog.get_logger()

    analysis_to = connected_components_analysis(graph)
    logger.info("Connected components analysis", **analysis_to.model_dump())


def connected_components_analysis(graph: nx.Graph) -> ConnectedComponentsStats:
    """Analyze the connected components of an undirected graph."""

    components: list[set] = list(nx.connected_components(graph))
    n_components = len(components)

    sizes = np.array([len(component) for component in components])

    largest_component_size = int(sizes.max())

    average_size = float(np.mean(sizes))
    std_size = float(np.std(sizes))

    return ConnectedComponentsStats(
        n_components=n_components,
        component_sizes=tuple(sizes),
        largest_component_size=largest_component_size,
        average_size=average_size,
        std_size=std_size,
    )
