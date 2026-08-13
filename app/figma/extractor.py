"""
Figma Node Extractor
Walks the Figma document tree and extracts meaningful component nodes
(frames, groups, components) along with their bounding boxes.
"""

from typing import Any


# Node types we treat as potential dashboard components
COMPONENT_TYPES = {"FRAME", "COMPONENT", "INSTANCE", "GROUP", "RECTANGLE", "TEXT", "VECTOR"}

# Minimum size (px) to consider a node a real component (filters tiny decorators)
MIN_WIDTH = 50
MIN_HEIGHT = 30


def extract_frames(figma_data: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Returns a flat list of top-level frames from the Figma document.
    Each frame represents one dashboard/page.
    """
    document = figma_data.get("document", {})
    frames = []
    for page in document.get("children", []):
        for child in page.get("children", []):
            if child.get("type") == "FRAME":
                frames.append(child)
    return frames


def extract_components(node: dict[str, Any], parent_bounds: dict | None = None) -> list[dict[str, Any]]:
    """
    Recursively walks a node tree and extracts leaf/meaningful components.
    Returns a list of component dicts with id, name, type, bounds, and raw node.
    """
    components = []
    node_type = node.get("type", "")
    bounds = node.get("absoluteBoundingBox") or node.get("absoluteRenderBounds")

    if bounds and node_type in COMPONENT_TYPES:
        w = bounds.get("width", 0)
        h = bounds.get("height", 0)
        if w >= MIN_WIDTH and h >= MIN_HEIGHT:
            components.append({
                "id": node.get("id"),
                "name": node.get("name", "unnamed"),
                "type": node_type,
                "bounds": {
                    "x": bounds.get("x", 0),
                    "y": bounds.get("y", 0),
                    "width": w,
                    "height": h,
                },
                "raw": node,
            })

    for child in node.get("children", []):
        components.extend(extract_components(child, bounds))

    return components


def get_canvas_size(frame: dict[str, Any]) -> tuple[float, float]:
    """Returns (width, height) of a frame."""
    bounds = frame.get("absoluteBoundingBox") or {}
    return bounds.get("width", 1440), bounds.get("height", 900)


def deduplicate_components(components: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Remove nested duplicates — if a parent and child have same bounds, keep parent.
    """
    seen_bounds = set()
    deduped = []
    for comp in components:
        b = comp["bounds"]
        key = (round(b["x"]), round(b["y"]), round(b["width"]), round(b["height"]))
        if key not in seen_bounds:
            seen_bounds.add(key)
            deduped.append(comp)
    return deduped
