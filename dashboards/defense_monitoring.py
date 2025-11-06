#!/usr/bin/env python3
"""
Defense Monitoring Dashboard with Datashader
"""
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import panel as pn
import numpy as np
import pandas as pd
import datashader as ds
import datashader.transfer_functions as tf
import colorcet as cc

pn.extension(design="bootstrap", sizing_mode="stretch_width")

def create_datashader_dashboard():
    """Create comprehensive Datashader-powered security monitoring dashboard."""

    # Generate sample data
    n_points = 1000000
    np.random.seed(42)

    threat_types = ['Malware', 'Phishing', 'DDoS', 'SQL Injection', 'XSS',
                    'Brute Force', 'Zero Day', 'Ransomware']

    threat_data = pd.DataFrame({
        'timestamp': np.random.randint(0, 86400, n_points),
        'severity': np.random.beta(2, 5, n_points),
        'threat_type': pd.Categorical(np.random.choice(threat_types, n_points)),
        'source_ip': np.random.randint(0, 255, n_points),
        'target_ip': np.random.randint(0, 255, n_points),
        'bytes_transferred': np.random.lognormal(10, 2, n_points)
    })

    network_data = pd.DataFrame({
        'timestamp': np.linspace(0, 86400, n_points),
        'bytes': np.random.lognormal(8, 2, n_points),
        'protocol': np.random.choice(['TCP', 'UDP', 'ICMP', 'HTTP', 'HTTPS'], n_points),
        'packets': np.random.poisson(10, n_points),
    })

    # Visualization 1: Threat Detection Scatter Plot
    def create_threat_scatter():
        canvas = ds.Canvas(plot_width=800, plot_height=400)
        agg = canvas.points(threat_data, 'timestamp', 'severity', ds.count_cat('threat_type'))
        img = tf.shade(agg, color_key=cc.palette['glasbey_category10'])
        img = tf.set_background(img, "black")
        from PIL import Image
        return pn.pane.PNG(img, width=800, height=400)

    # Visualization 2: Network Traffic Over Time
    def create_network_traffic():
        canvas = ds.Canvas(plot_width=800, plot_height=400)
        agg = canvas.points(network_data, 'timestamp', 'bytes')
        img = tf.shade(agg, cmap=cc.fire)
        img = tf.set_background(img, "black")
        from PIL import Image
        return pn.pane.PNG(img, width=800, height=400)

    # Visualization 3: IP Traffic Heatmap
    def create_ip_heatmap():
        canvas = ds.Canvas(plot_width=600, plot_height=600)
        agg = canvas.points(threat_data, 'source_ip', 'target_ip')
        img = tf.shade(agg, cmap=cc.fire)
        from PIL import Image
        return pn.pane.PNG(img, width=600, height=600)

    # Data statistics
    total_threats = len(threat_data)
    high_severity = len(threat_data[threat_data['severity'] > 0.7])
    unique_threat_types = threat_data['threat_type'].nunique()

    stats_card = pn.Column(
        "### Security Monitoring Statistics",
        f"**Total Threats Detected:** {total_threats:,}",
        f"**High Severity Threats:** {high_severity:,}",
        f"**Unique Threat Types:** {unique_threat_types}",
        f"**Data Points Visualized:** {n_points:,}",
        "---",
        "**Powered by Datashader** - Efficiently visualizing millions of data points",
        styles={'background': '#2b2b2b', 'padding': '20px', 'border-radius': '10px'}
    )

    # Create the dashboard layout
    datashader_dashboard = pn.Column(
        pn.pane.Markdown("# 🛡️ Datashader Security Monitoring Dashboard"),
        pn.pane.Markdown("""
        This dashboard demonstrates **Datashader's** ability to visualize massive security datasets.
        Each visualization below represents **1 million data points** rendered in real-time using
        Datashader's powerful rasterization pipeline.

        ## Key Features:
        - **Projection**: Data is projected into visualization bins
        - **Aggregation**: Large datasets are compressed into aggregate arrays
        - **Transformation**: Aggregates are processed into images
        """),

        pn.Row(stats_card, width=800),

        "---",

        pn.pane.Markdown("## 1. Threat Detection Timeline (1M points)"),
        pn.pane.Markdown("*Categorical scatter plot showing threat types over 24 hours by severity*"),
        create_threat_scatter(),

        "---",

        pn.pane.Markdown("## 2. Network Traffic Density (1M points)"),
        pn.pane.Markdown("*Heatmap showing network traffic volume over time*"),
        create_network_traffic(),

        "---",

        pn.pane.Markdown("## 3. IP Traffic Matrix"),
        pn.pane.Markdown("*Source vs Target IP visualization showing connection patterns*"),
        create_ip_heatmap(),

        "---",

        pn.pane.Markdown("""
### 📊 Integration with Security Modules

This Datashader integration works with your modules:
- **RealTimeMonitoring**: Visualize live threat streams
- **ThreatIntelligence**: Display threat feeds at scale
- **PredictiveAnalytics**: Show predictions across large datasets
- **NetworkExploitation**: Map network attack surfaces

[← Back to Home](./home) | [Attack Control →](./attack_control)
        """),
    )

    return datashader_dashboard

# Create and serve defense monitoring dashboard
dashboard = create_datashader_dashboard()

pn.template.BootstrapTemplate(
    title="Defense Monitoring",
    main=dashboard,
    main_max_width="95%",
    header_background="#8B0000",
).servable()
