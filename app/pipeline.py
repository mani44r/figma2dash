"""
Main Processing Pipeline
Orchestrates the entire flow: Figma → Extract → Classify → Map → Generate Config
"""

from typing import Any
from app.figma.client import parse_figma_url, fetch_file, fetch_image_urls
from app.figma.extractor import extract_frames, extract_components, get_canvas_size, deduplicate_components
from app.classifier.vision_classifier import classify_batch
from app.layout.grid_mapper import map_to_grid
from app.generator.config_generator import generate_config, to_json, to_yaml
from app.models import DashboardConfig


class ProcessingPipeline:
    """End-to-end pipeline for Figma to Dashboard conversion."""
    
    def __init__(self, figma_url: str):
        self.figma_url = figma_url
        self.file_key = None
        self.node_id = None
        self.figma_data = None
        self.components = []
        self.canvas_width = 1440
        self.canvas_height = 900
        self.config: DashboardConfig | None = None
    
    def run(self) -> DashboardConfig:
        """Execute the full pipeline."""
        print("🚀 Starting Figma to Dashboard Pipeline...")
        
        # Step 1: Parse URL
        print("\n📎 Step 1: Parsing Figma URL...")
        self.file_key, self.node_id = parse_figma_url(self.figma_url)
        print(f"   File Key: {self.file_key}")
        if self.node_id:
            print(f"   Node ID: {self.node_id}")
        
        # Step 2: Fetch Figma data
        print("\n📥 Step 2: Fetching Figma file data...")
        self.figma_data = fetch_file(self.file_key)
        print(f"   Document: {self.figma_data.get('name', 'Unknown')}")
        
        # Step 3: Extract components
        print("\n🔍 Step 3: Extracting components from design...")
        frames = extract_frames(self.figma_data)
        if not frames:
            raise ValueError("No frames found in Figma file.")
        
        # Use first frame as main dashboard
        main_frame = frames[0]
        print(f"   Using frame: {main_frame.get('name', 'Unnamed')}")
        
        self.canvas_width, self.canvas_height = get_canvas_size(main_frame)
        print(f"   Canvas size: {self.canvas_width}x{self.canvas_height}px")
        
        raw_components = extract_components(main_frame)
        self.components = deduplicate_components(raw_components)
        print(f"   Found {len(self.components)} components")
        
        # Step 4: Fetch component images
        print("\n🖼️  Step 4: Fetching component images...")
        node_ids = [comp["id"] for comp in self.components]
        image_urls = fetch_image_urls(self.file_key, node_ids)
        
        for comp in self.components:
            comp["image_url"] = image_urls.get(comp["id"], "")
        
        valid_images = sum(1 for c in self.components if c.get("image_url"))
        print(f"   Retrieved {valid_images}/{len(self.components)} images")
        
        # Step 5: Classify components using AI
        print("\n🤖 Step 5: Classifying components with AI...")
        self.components = classify_batch(self.components)
        
        # Show classification summary
        type_counts = {}
        for comp in self.components:
            comp_type = comp.get("component_type", "unknown")
            type_counts[comp_type] = type_counts.get(comp_type, 0) + 1
        
        for comp_type, count in type_counts.items():
            print(f"   - {comp_type}: {count}")
        
        # Step 6: Map to grid layout
        print("\n📐 Step 6: Mapping to 12-column grid...")
        self.components = map_to_grid(self.components, self.canvas_width, self.canvas_height)
        print(f"   Mapped {len(self.components)} components to grid")
        
        # Step 7: Generate config
        print("\n⚙️  Step 7: Generating dashboard configuration...")
        self.config = generate_config(self.components, self.canvas_width, self.canvas_height)
        print(f"   Config created with {len(self.config.components)} components")
        
        print("\n✅ Pipeline completed successfully!\n")
        return self.config
    
    def get_json(self, pretty: bool = True) -> str:
        """Get config as JSON."""
        if not self.config:
            raise RuntimeError("Pipeline not executed. Call run() first.")
        return to_json(self.config, pretty)
    
    def get_yaml(self) -> str:
        """Get config as YAML."""
        if not self.config:
            raise RuntimeError("Pipeline not executed. Call run() first.")
        return to_yaml(self.config)
    
    def get_summary(self) -> dict[str, Any]:
        """Get a summary of the processing results."""
        if not self.config:
            raise RuntimeError("Pipeline not executed. Call run() first.")
        
        type_counts = {}
        for comp in self.config.components:
            type_counts[comp.component_type] = type_counts.get(comp.component_type, 0) + 1
        
        return {
            "figma_url": self.figma_url,
            "file_key": self.file_key,
            "canvas_size": {
                "width": self.canvas_width,
                "height": self.canvas_height
            },
            "total_components": len(self.config.components),
            "component_types": type_counts
        }
