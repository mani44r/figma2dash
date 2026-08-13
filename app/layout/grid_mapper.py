"""
12-Column Grid Layout Mapper
Maps component bounding boxes to a 12-column grid system.
"""

from typing import Any

GRID_COLUMNS = 12


def map_to_grid(components: list[dict[str, Any]], canvas_width: float, canvas_height: float) -> list[dict[str, Any]]:
    """
    Maps components to a 12-column grid.
    Adds 'grid_position' field with row, col_start, col_span.
    """
    if canvas_width <= 0:
        canvas_width = 1440
    
    col_width = canvas_width / GRID_COLUMNS
    
    # Sort components by Y position (top to bottom), then X (left to right)
    sorted_comps = sorted(components, key=lambda c: (c["bounds"]["y"], c["bounds"]["x"]))
    
    # Assign rows based on Y clustering
    rows = assign_rows(sorted_comps, tolerance=20)
    
    for comp in sorted_comps:
        bounds = comp["bounds"]
        x = bounds["x"]
        width = bounds["width"]
        
        # Calculate column start and span
        col_start = max(1, min(GRID_COLUMNS, round((x / canvas_width) * GRID_COLUMNS) + 1))
        col_span = max(1, min(GRID_COLUMNS, round((width / canvas_width) * GRID_COLUMNS)))
        
        # Ensure col_start + col_span doesn't exceed grid
        if col_start + col_span - 1 > GRID_COLUMNS:
            col_span = GRID_COLUMNS - col_start + 1
        
        comp["grid_position"] = {
            "row": rows[comp["id"]],
            "col_start": col_start,
            "col_span": col_span,
            "col_end": col_start + col_span - 1
        }
    
    return sorted_comps


def assign_rows(components: list[dict[str, Any]], tolerance: float = 20) -> dict[str, int]:
    """
    Assigns row numbers to components based on Y position clustering.
    Components within 'tolerance' pixels vertically are considered same row.
    """
    rows = {}
    current_row = 1
    last_y = None
    
    for comp in components:
        y = comp["bounds"]["y"]
        
        if last_y is None or abs(y - last_y) > tolerance:
            if last_y is not None:
                current_row += 1
            last_y = y
        
        rows[comp["id"]] = current_row
    
    return rows


def calculate_row_heights(components: list[dict[str, Any]]) -> dict[int, float]:
    """
    Calculate the maximum height for each row.
    Returns {row_number: max_height_in_row}.
    """
    row_heights = {}
    
    for comp in components:
        row = comp.get("grid_position", {}).get("row")
        height = comp["bounds"]["height"]
        
        if row:
            row_heights[row] = max(row_heights.get(row, 0), height)
    
    return row_heights
