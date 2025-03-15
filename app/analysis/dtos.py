"""Analysis data transfer objects."""

from app.dtos import CustomBaseModel


class DegreeStats(CustomBaseModel):
    mean: float
    variance: float
    skewness: float
    kurtosis: float


class ConnectedComponentsStats(CustomBaseModel):
    n_components: int
    component_sizes: tuple[int]
    largest_component_size: int
    average_size: float
    std_size: float
