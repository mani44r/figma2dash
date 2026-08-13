"""
Vision-based Component Classifier
Uses Google Gemini Vision API to classify components from screenshots.
"""

import os
import base64
import httpx
import google.generativeai as genai
from typing import Literal
from PIL import Image
import io

ComponentType = Literal["chart", "table", "kpi_card", "filter", "text", "image", "button", "unknown"]


def get_gemini_client():
    """Initialize Gemini with API key from environment."""
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY is not set in environment.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')


def download_image_as_pil(image_url: str) -> Image.Image:
    """Download image from URL and return PIL Image."""
    response = httpx.get(image_url, timeout=30)
    response.raise_for_status()
    return Image.open(io.BytesIO(response.content))


def classify_component(image_url: str, component_name: str = "") -> ComponentType:
    """
    Classifies a component image using Gemini Vision.
    Returns one of: chart, table, kpi_card, filter, text, image, button, unknown.
    """
    model = get_gemini_client()
    
    # Download image
    try:
        image_pil = download_image_as_pil(image_url)
    except Exception as e:
        print(f"Error downloading image: {e}")
        return "unknown"

    # Construct prompt
    prompt = f"""You are an AI that classifies dashboard components.

Look at this component image and classify it into ONE of these categories:
- chart (bar chart, line chart, pie chart, area chart, scatter plot, etc.)
- table (data table, grid, list with rows/columns)
- kpi_card (single metric card, stat card, number display with label)
- filter (dropdown, date picker, search box, filter control)
- text (heading, label, paragraph, title)
- image (logo, icon, decorative image)
- button (clickable button, action button)
- unknown (if none of the above fit)

Component name: "{component_name}"

Respond with ONLY the category name, nothing else."""

    try:
        response = model.generate_content([prompt, image_pil])
        
        classification = response.text.strip().lower()
        
        # Validate response
        valid_types: list[ComponentType] = [
            "chart", "table", "kpi_card", "filter", "text", "image", "button", "unknown"
        ]
        
        if classification in valid_types:
            return classification  # type: ignore
        
        # Fuzzy matching for common variations
        if "chart" in classification or "graph" in classification:
            return "chart"
        elif "table" in classification or "grid" in classification:
            return "table"
        elif "kpi" in classification or "card" in classification or "metric" in classification:
            return "kpi_card"
        elif "filter" in classification or "dropdown" in classification or "picker" in classification:
            return "filter"
        elif "text" in classification or "heading" in classification or "label" in classification:
            return "text"
        elif "image" in classification or "icon" in classification or "logo" in classification:
            return "image"
        elif "button" in classification:
            return "button"
        else:
            return "unknown"
            
    except Exception as e:
        print(f"Error classifying component: {e}")
        return "unknown"


def classify_batch(components: list[dict]) -> list[dict]:
    """
    Classifies multiple components.
    Adds 'component_type' field to each component dict.
    """
    for comp in components:
        image_url = comp.get("image_url", "")
        name = comp.get("name", "")
        
        if not image_url:
            comp["component_type"] = "unknown"
            continue
            
        comp["component_type"] = classify_component(image_url, name)
    
    return components
