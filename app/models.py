"""
Pydantic Models for Data Validation
"""

from pydantic import BaseModel, HttpUrl
from typing import Literal


class FigmaRequest(BaseModel):
    figma_url: str


class ComponentBounds(BaseModel):
    x: float
    y: float
    width: float
    height: float


class GridPosition(BaseModel):
    row: int
    col_start: int
    col_span: int
    col_end: int


class DashboardComponent(BaseModel):
    id: str
    name: str
    type: str
    component_type: Literal["chart", "table", "kpi_card", "filter", "text", "image", "button", "unknown"]
    bounds: ComponentBounds
    grid_position: GridPosition
    image_url: str | None = None


class DashboardConfig(BaseModel):
    layout: str = "12-column-grid"
    canvas_width: float
    canvas_height: float
    components: list[DashboardComponent]
