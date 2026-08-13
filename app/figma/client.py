"""
Figma API Client
Fetches file data, frames, and node trees from Figma using the REST API.
"""

import os
import re
import httpx
from typing import Any

FIGMA_BASE_URL = "https://api.figma.com/v1"


def get_token() -> str:
    token = os.getenv("FIGMA_TOKEN", "")
    if not token:
        raise EnvironmentError("FIGMA_TOKEN is not set in environment.")
    return token


def parse_figma_url(url: str) -> tuple[str, str | None]:
    """
    Extract file_key and optional node_id from a Figma URL.
    Supports:
      https://www.figma.com/file/<key>/...
      https://www.figma.com/design/<key>/...
    """
    pattern = r"figma\.com/(?:file|design)/([A-Za-z0-9_-]+)"
    match = re.search(pattern, url)
    if not match:
        raise ValueError(f"Could not extract file key from URL: {url}")
    file_key = match.group(1)

    node_match = re.search(r"node-id=([^&]+)", url)
    node_id = node_match.group(1).replace("%3A", ":") if node_match else None

    return file_key, node_id


def fetch_file(file_key: str) -> dict[str, Any]:
    """Fetch full Figma file JSON."""
    headers = {"X-Figma-Token": get_token()}
    url = f"{FIGMA_BASE_URL}/files/{file_key}"
    response = httpx.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_node(file_key: str, node_id: str) -> dict[str, Any]:
    """Fetch a specific node from a Figma file."""
    headers = {"X-Figma-Token": get_token()}
    url = f"{FIGMA_BASE_URL}/files/{file_key}/nodes?ids={node_id}"
    response = httpx.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_image_urls(file_key: str, node_ids: list[str]) -> dict[str, str]:
    """
    Fetch rendered PNG image URLs for given node IDs.
    Returns a dict of {node_id: image_url}.
    """
    headers = {"X-Figma-Token": get_token()}
    ids_param = ",".join(node_ids)
    url = f"{FIGMA_BASE_URL}/images/{file_key}?ids={ids_param}&format=png&scale=1"
    response = httpx.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data.get("images", {})
