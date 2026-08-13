"""
Dashboard Config Generator
Generates JSON/YAML dashboard configuration from classified and mapped components.
"""

import json
import yaml
from typing import Any
from app.models import DashboardConfig, DashboardComponent, ComponentBounds, GridPosition


def generate_config(components: list[dict[str, Any]], canvas_width: float, canvas_height: float) -> DashboardConfig:
    """
    Generate a structured dashboard configuration from processed components.
    """
    dashboard_components = []
    
    for comp in components:
        component = DashboardComponent(
            id=comp["id"],
            name=comp["name"],
            type=comp["type"],
            component_type=comp.get("component_type", "unknown"),
            bounds=ComponentBounds(**comp["bounds"]),
            grid_position=GridPosition(**comp["grid_position"]),
            image_url=comp.get("image_url")
        )
        dashboard_components.append(component)
    
    config = DashboardConfig(
        canvas_width=canvas_width,
        canvas_height=canvas_height,
        components=dashboard_components
    )
    
    return config


def to_json(config: DashboardConfig, pretty: bool = True) -> str:
    """Convert config to JSON string."""
    data = config.model_dump(exclude_none=True)
    if pretty:
        return json.dumps(data, indent=2)
    return json.dumps(data)


def to_yaml(config: DashboardConfig) -> str:
    """Convert config to YAML string."""
    data = config.model_dump(exclude_none=True)
    return yaml.dump(data, sort_keys=False, default_flow_style=False)


def to_dict(config: DashboardConfig) -> dict[str, Any]:
    """Convert config to dictionary."""
    return config.model_dump(exclude_none=True)
