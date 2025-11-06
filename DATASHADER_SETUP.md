# Datashader Integration Guide

## Overview

This project now includes **Datashader** integration for visualizing large-scale security monitoring data. Datashader is a powerful data rasterization pipeline that can efficiently visualize millions (or billions) of data points in real-time.

## What's Been Added

### 1. Dependencies (`requirements.txt`)
- `datashader` - Core rasterization engine
- `colorcet` - Perceptually uniform colormaps
- `holoviews` - High-level plotting library
- `bokeh` - Interactive visualization library
- `numpy` - Numerical computing
- `pandas` - Data manipulation

### 2. Enhanced DataVisualization Module

The `modules/data_visualization.py` module now includes:

#### New Datashader Methods:

- `datashader_network_traffic()` - Visualize network traffic patterns
- `datashader_threat_scatter()` - Categorical scatter plot for threat detection
- `datashader_heatmap()` - Generic heatmap for 2D data
- `datashader_line_plot()` - Time series visualization
- `datashader_network_graph()` - Network connection patterns
- `generate_sample_threat_data()` - Generate demo threat data
- `generate_sample_network_traffic()` - Generate demo network data

#### Example Usage:

```python
from modules.data_visualization import DataVisualization

viz = DataVisualization()

# Generate sample data
threat_df = viz.generate_sample_threat_data(n_points=1000000)
network_df = viz.generate_sample_network_traffic(n_points=1000000)

# Create visualizations
threat_img = viz.datashader_threat_scatter(threat_df)
traffic_img = viz.datashader_network_traffic(network_df)
heatmap_img = viz.datashader_heatmap(threat_df, 'source_ip', 'target_ip')
```

### 3. Datashader Dashboard in app.py

A complete security monitoring dashboard has been added to `app.py`:

- **1 Million Data Points** per visualization
- Real-time rendering using Datashader
- Three main visualizations:
  1. Threat Detection Timeline (categorical scatter)
  2. Network Traffic Density (heatmap)
  3. IP Traffic Matrix (connection patterns)

## Installation

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

or with conda (recommended for optimal performance):

```bash
conda install -c conda-forge datashader colorcet holoviews bokeh numpy pandas panel
```

### Step 2: Verify Installation

```python
import datashader
import colorcet
import panel
print("Datashader version:", datashader.__version__)
```

## Running the Application

### Option 1: Run with Panel Serve (Recommended)

```bash
panel serve app.py --show --port 5006
```

This will start two dashboards:
1. **Image Classification Demo** - Original demo (http://localhost:5006/Panel_Demo_-_Image_Classification)
2. **Datashader Security Monitoring** - New dashboard (http://localhost:5006/Datashader_Security_Monitoring)

### Option 2: Run Directly

```bash
python app.py
```

Then navigate to the Panel server URLs shown in the terminal.

## How Datashader Works

Datashader uses a 3-step pipeline:

### 1. **Projection**
Each data record is projected into bins of a plotting grid based on a specified glyph (points, lines, etc.)

```python
canvas = ds.Canvas(plot_width=800, plot_height=600)
```

### 2. **Aggregation**
Reductions are computed for each bin, compressing large datasets into aggregate arrays

```python
agg = canvas.points(dataframe, 'x_column', 'y_column')
```

### 3. **Transformation**
Aggregates are processed into images with colormaps and styling

```python
img = tf.shade(agg, cmap=colorcet.fire)
img = tf.set_background(img, "black")
```

## Integration with Your Security Modules

The Datashader visualization works seamlessly with your existing modules:

### RealTimeMonitoring
```python
from modules.real_time_monitoring import RealTimeMonitoring
from modules.data_visualization import DataVisualization

monitoring = RealTimeMonitoring(threat_intelligence_module)
viz = DataVisualization()

# Collect monitoring data
async for data in data_stream:
    # Convert to DataFrame
    df = pd.DataFrame(monitoring_data)

    # Visualize with Datashader
    img = viz.datashader_network_traffic(df, x_col='timestamp', y_col='bytes')
```

### ThreatIntelligence
```python
from modules.threat_intelligence import ThreatIntelligence

threat_intel = ThreatIntelligence()
threat_data = await threat_intel.get_threat_intelligence()

# Convert to DataFrame and visualize
df = pd.DataFrame(threat_data)
img = viz.datashader_threat_scatter(df)
```

### VulnerabilityScanner
```python
from modules.vulnerability_scanner import VulnerabilityScanner

scanner = VulnerabilityScanner()
scan_results = scanner.scan_network()

# Visualize scan results across IP ranges
df = pd.DataFrame(scan_results)
img = viz.datashader_heatmap(df, 'target_ip', 'vulnerability_count')
```

## Customization

### Changing Color Schemes

```python
import colorcet as cc

# Available colormaps
img = tf.shade(agg, cmap=cc.fire)      # Fire colors
img = tf.shade(agg, cmap=cc.coolwarm)  # Cool to warm
img = tf.shade(agg, cmap=cc.rainbow)   # Rainbow
img = tf.shade(agg, cmap=cc.bmy)       # Blue-magenta-yellow
```

### Adjusting Canvas Size

```python
# Larger canvas for more detail
canvas = ds.Canvas(plot_width=1920, plot_height=1080)

# Smaller canvas for faster rendering
canvas = ds.Canvas(plot_width=400, plot_height=300)
```

### Using Your Own Data

Replace the sample data generation with your actual security data:

```python
# Instead of:
threat_data = viz.generate_sample_threat_data(1000000)

# Use your data:
threat_data = pd.read_sql("SELECT * FROM threat_logs", engine)
# or
threat_data = pd.read_csv("threat_data.csv")
# or
threat_data = pd.DataFrame(your_monitoring_data)
```

## Performance Tips

1. **Data Types**: Ensure numeric columns are proper numeric types (not strings)
   ```python
   df['timestamp'] = pd.to_numeric(df['timestamp'])
   ```

2. **Memory Management**: Process data in chunks for very large datasets
   ```python
   chunks = pd.read_csv('large_file.csv', chunksize=100000)
   for chunk in chunks:
       img = viz.datashader_network_traffic(chunk)
   ```

3. **Canvas Resolution**: Match canvas size to display size
   ```python
   # For web display (typically 72-96 DPI)
   canvas = ds.Canvas(plot_width=800, plot_height=600)

   # For high-res displays
   canvas = ds.Canvas(plot_width=1600, plot_height=1200)
   ```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'datashader'"
**Solution**: Install datashader: `pip install datashader`

### Issue: Visualizations appear blank
**Solution**: Check that your data columns exist and contain valid numeric data
```python
print(df.dtypes)  # Check data types
print(df.describe())  # Check data ranges
```

### Issue: Performance is slow
**Solution**:
- Reduce canvas size
- Ensure data is properly indexed
- Use categorical aggregation for categorical data

## Resources

- [Datashader Documentation](https://datashader.org/)
- [Datashader Examples](https://examples.pyviz.org/datashader/)
- [Panel Documentation](https://panel.holoviz.org/)
- [HoloViz Tutorial](https://holoviz.org/tutorial/)
- [Colorcet Color Maps](https://colorcet.holoviz.org/)

## Next Steps

1. **Connect Real Data**: Replace sample data with actual security monitoring data
2. **Add Interactivity**: Use Panel widgets to filter and explore data
3. **Create Dashboards**: Combine multiple visualizations in custom layouts
4. **Real-time Updates**: Implement streaming data visualization
5. **Export Visualizations**: Save images for reports and documentation

## Example: Complete Integration

```python
import panel as pn
from modules.data_visualization import DataVisualization
from modules.real_time_monitoring import RealTimeMonitoring

# Initialize
pn.extension()
viz = DataVisualization()

# Generate or load data
threat_data = viz.generate_sample_threat_data(1000000)

# Create visualizations
threat_scatter = pn.pane.PNG(
    viz.datashader_threat_scatter(threat_data),
    width=800,
    height=400
)

# Create dashboard
dashboard = pn.Column(
    "# Security Monitoring Dashboard",
    threat_scatter,
)

# Serve
dashboard.servable()
```

Run with: `panel serve your_script.py --show`

---

**Generated with Datashader Integration**
Project: Red-Sword Security Monitoring Platform
