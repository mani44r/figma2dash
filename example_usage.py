"""
Example Usage Script
Demonstrates how to use the Figma to Dashboard pipeline programmatically.
"""

from dotenv import load_dotenv
from app.pipeline import ProcessingPipeline
import json

# Load environment variables
load_dotenv()

def example_basic_usage():
    """Basic usage example."""
    print("=" * 60)
    print("EXAMPLE 1: Basic Usage")
    print("=" * 60)
    
    # Replace with your actual Figma URL
    figma_url = "https://www.figma.com/file/YOUR_FILE_KEY"
    
    try:
        # Create pipeline
        pipeline = ProcessingPipeline(figma_url)
        
        # Run conversion
        config = pipeline.run()
        
        # Print summary
        summary = pipeline.get_summary()
        print("\n📊 SUMMARY:")
        print(f"  Total Components: {summary['total_components']}")
        print(f"  Canvas Size: {summary['canvas_size']['width']}x{summary['canvas_size']['height']}")
        print(f"\n  Component Breakdown:")
        for comp_type, count in summary['component_types'].items():
            print(f"    - {comp_type}: {count}")
        
        # Save to files
        with open("output_config.json", "w") as f:
            f.write(pipeline.get_json())
        print("\n✅ Saved JSON config to: output_config.json")
        
        with open("output_config.yaml", "w") as f:
            f.write(pipeline.get_yaml())
        print("✅ Saved YAML config to: output_config.yaml")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def example_detailed_output():
    """Example showing detailed component information."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Detailed Component Output")
    print("=" * 60)
    
    figma_url = "https://www.figma.com/file/YOUR_FILE_KEY"
    
    try:
        pipeline = ProcessingPipeline(figma_url)
        config = pipeline.run()
        
        print("\n📋 COMPONENTS DETECTED:\n")
        for i, component in enumerate(config.components, 1):
            print(f"{i}. {component.name}")
            print(f"   Type: {component.component_type}")
            print(f"   Grid Position: Row {component.grid_position.row}, "
                  f"Columns {component.grid_position.col_start}-{component.grid_position.col_end}")
            print(f"   Size: {component.bounds.width:.0f}x{component.bounds.height:.0f}px")
            print()
        
    except Exception as e:
        print(f"❌ Error: {e}")


def example_filter_by_type():
    """Example showing how to filter components by type."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Filter Components by Type")
    print("=" * 60)
    
    figma_url = "https://www.figma.com/file/YOUR_FILE_KEY"
    
    try:
        pipeline = ProcessingPipeline(figma_url)
        config = pipeline.run()
        
        # Filter charts
        charts = [c for c in config.components if c.component_type == "chart"]
        print(f"\n📊 CHARTS ({len(charts)}):")
        for chart in charts:
            print(f"  - {chart.name}")
        
        # Filter tables
        tables = [c for c in config.components if c.component_type == "table"]
        print(f"\n📋 TABLES ({len(tables)}):")
        for table in tables:
            print(f"  - {table.name}")
        
        # Filter KPI cards
        kpis = [c for c in config.components if c.component_type == "kpi_card"]
        print(f"\n💳 KPI CARDS ({len(kpis)}):")
        for kpi in kpis:
            print(f"  - {kpi.name}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("\n🚀 Figma to Dashboard - Example Usage\n")
    print("⚠️  Before running:")
    print("  1. Set FIGMA_TOKEN in .env")
    print("  2. Set OPENAI_API_KEY in .env")
    print("  3. Replace YOUR_FILE_KEY with your actual Figma file URL")
    print()
    
    # Uncomment the example you want to run:
    
    # example_basic_usage()
    # example_detailed_output()
    # example_filter_by_type()
    
    print("\n💡 Uncomment an example function to run it!")
