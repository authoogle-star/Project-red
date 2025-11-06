#!/usr/bin/env python3
"""
Test script for Datashader integration
Demonstrates the DataVisualization module's Datashader capabilities
"""

import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.data_visualization import DataVisualization

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    """Test Datashader visualization methods."""

    print("\n" + "=" * 60)
    print("  Datashader Integration Test")
    print("  Project Red-Sword Security Monitoring")
    print("=" * 60 + "\n")

    # Initialize visualization module
    logging.info("Initializing DataVisualization module...")
    viz = DataVisualization()

    # Test 1: Generate sample threat data
    logging.info("Test 1: Generating sample threat data...")
    try:
        threat_data = viz.generate_sample_threat_data(n_points=100000)
        logging.info(f"✅ Generated {len(threat_data):,} threat data points")
        logging.info(f"   Columns: {list(threat_data.columns)}")
        logging.info(f"   Threat types: {threat_data['threat_type'].unique().tolist()}")
    except Exception as e:
        logging.error(f"❌ Failed to generate threat data: {e}")
        return False

    # Test 2: Generate sample network traffic
    logging.info("\nTest 2: Generating sample network traffic data...")
    try:
        network_data = viz.generate_sample_network_traffic(n_points=100000)
        logging.info(f"✅ Generated {len(network_data):,} network traffic points")
        logging.info(f"   Columns: {list(network_data.columns)}")
        logging.info(f"   Protocols: {network_data['protocol'].unique().tolist()}")
    except Exception as e:
        logging.error(f"❌ Failed to generate network data: {e}")
        return False

    # Test 3: Create threat scatter visualization
    logging.info("\nTest 3: Creating Datashader threat scatter plot...")
    try:
        img = viz.datashader_threat_scatter(
            threat_data,
            x_col='timestamp',
            y_col='severity',
            category_col='threat_type',
            width=800,
            height=600
        )
        logging.info("✅ Successfully created threat scatter visualization")
        logging.info(f"   Image type: {type(img)}")
    except Exception as e:
        logging.error(f"❌ Failed to create threat scatter: {e}")
        return False

    # Test 4: Create network traffic visualization
    logging.info("\nTest 4: Creating Datashader network traffic plot...")
    try:
        img = viz.datashader_network_traffic(
            network_data,
            x_col='timestamp',
            y_col='bytes',
            width=800,
            height=600
        )
        logging.info("✅ Successfully created network traffic visualization")
    except Exception as e:
        logging.error(f"❌ Failed to create network traffic plot: {e}")
        return False

    # Test 5: Create heatmap
    logging.info("\nTest 5: Creating Datashader IP heatmap...")
    try:
        img = viz.datashader_heatmap(
            threat_data,
            x_col='source_ip',
            y_col='target_ip',
            width=600,
            height=600
        )
        logging.info("✅ Successfully created IP heatmap")
    except Exception as e:
        logging.error(f"❌ Failed to create heatmap: {e}")
        return False

    # Test 6: Create line plot
    logging.info("\nTest 6: Creating Datashader time series plot...")
    try:
        # Prepare time series data
        time_series = network_data[['timestamp', 'bytes']].copy()
        time_series = time_series.sort_values('timestamp')

        img = viz.datashader_line_plot(
            time_series,
            x_col='timestamp',
            y_col='bytes',
            width=800,
            height=400
        )
        logging.info("✅ Successfully created time series visualization")
    except Exception as e:
        logging.error(f"❌ Failed to create line plot: {e}")
        return False

    # Summary
    print("\n" + "=" * 60)
    print("  Test Results Summary")
    print("=" * 60)
    print("✅ All Datashader tests passed successfully!")
    print("\nCapabilities verified:")
    print("  • Generate sample security data")
    print("  • Create categorical scatter plots")
    print("  • Visualize network traffic patterns")
    print("  • Generate IP traffic heatmaps")
    print("  • Display time series data")
    print("\nNext steps:")
    print("  1. Run the dashboard: ./run_datashader_dashboard.sh")
    print("  2. Or use Panel: panel serve app.py --show")
    print("  3. Visit: http://localhost:5006/Datashader_Security_Monitoring")
    print("=" * 60 + "\n")

    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        logging.error(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
