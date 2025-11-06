import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import datashader as ds
import datashader.transfer_functions as tf
from datashader.colors import Greys9, viridis, inferno
import colorcet as cc

class DataVisualization:
    def __init__(self):
        sns.set(style="whitegrid")

    def plot_device_information(self, device_data):
        df = pd.DataFrame(device_data)
        plt.figure(figsize=(10, 6))
        sns.barplot(x="device_type", y="count", data=df)
        plt.title("Device Information")
        plt.xlabel("Device Type")
        plt.ylabel("Count")
        plt.show()

    def plot_network_traffic(self, traffic_data):
        df = pd.DataFrame(traffic_data)
        plt.figure(figsize=(10, 6))
        sns.lineplot(x="timestamp", y="traffic", hue="protocol", data=df)
        plt.title("Network Traffic")
        plt.xlabel("Timestamp")
        plt.ylabel("Traffic")
        plt.show()

    def plot_system_logs(self, log_data):
        df = pd.DataFrame(log_data)
        plt.figure(figsize=(10, 6))
        sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
        plt.title("System Logs Correlation")
        plt.show()

    def plot_threat_detection(self, threat_data):
        df = pd.DataFrame(threat_data)
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x="timestamp", y="severity", hue="threat_type", data=df)
        plt.title("Threat Detection")
        plt.xlabel("Timestamp")
        plt.ylabel("Severity")
        plt.show()

    def plot_defcon_level(self, defcon_data):
        df = pd.DataFrame(defcon_data)
        plt.figure(figsize=(10, 6))
        sns.lineplot(x="timestamp", y="defcon_level", data=df)
        plt.title("Defcon Level Status")
        plt.xlabel("Timestamp")
        plt.ylabel("Defcon Level")
        plt.show()

    # Datashader visualization methods for large-scale data

    def datashader_network_traffic(self, traffic_df, x_col='timestamp', y_col='bytes', width=800, height=600):
        """
        Create a Datashader visualization of network traffic patterns.
        Ideal for millions of data points.

        Args:
            traffic_df: DataFrame with network traffic data
            x_col: Column name for x-axis (e.g., timestamp)
            y_col: Column name for y-axis (e.g., bytes transferred)
            width: Canvas width in pixels
            height: Canvas height in pixels

        Returns:
            Datashader image object
        """
        canvas = ds.Canvas(plot_width=width, plot_height=height)
        agg = canvas.points(traffic_df, x_col, y_col)
        img = tf.shade(agg, cmap=cc.fire)
        return tf.set_background(img, "black")

    def datashader_threat_scatter(self, threat_df, x_col='timestamp', y_col='severity',
                                   category_col='threat_type', width=800, height=600):
        """
        Create a Datashader scatter plot of threat detections with categorical coloring.

        Args:
            threat_df: DataFrame with threat data
            x_col: Column name for x-axis
            y_col: Column name for y-axis
            category_col: Column name for categorical data (threat types)
            width: Canvas width in pixels
            height: Canvas height in pixels

        Returns:
            Datashader image object
        """
        canvas = ds.Canvas(plot_width=width, plot_height=height)
        agg = canvas.points(threat_df, x_col, y_col, ds.count_cat(category_col))
        img = tf.shade(agg, color_key=cc.palette['glasbey_category10'])
        return tf.set_background(img, "black")

    def datashader_heatmap(self, data_df, x_col, y_col, agg_col=None, width=800, height=600):
        """
        Create a Datashader heatmap for large-scale 2D data.

        Args:
            data_df: DataFrame with data to visualize
            x_col: Column name for x-axis
            y_col: Column name for y-axis
            agg_col: Optional column to aggregate (default: count)
            width: Canvas width in pixels
            height: Canvas height in pixels

        Returns:
            Datashader image object
        """
        canvas = ds.Canvas(plot_width=width, plot_height=height)

        if agg_col:
            agg = canvas.points(data_df, x_col, y_col, ds.mean(agg_col))
        else:
            agg = canvas.points(data_df, x_col, y_col)

        img = tf.shade(agg, cmap=cc.coolwarm)
        return img

    def datashader_line_plot(self, time_series_df, x_col='timestamp', y_col='value',
                             width=800, height=600):
        """
        Create a Datashader line plot for large time series data.

        Args:
            time_series_df: DataFrame with time series data
            x_col: Column name for x-axis (timestamp)
            y_col: Column name for y-axis (values)
            width: Canvas width in pixels
            height: Canvas height in pixels

        Returns:
            Datashader image object
        """
        canvas = ds.Canvas(plot_width=width, plot_height=height)
        agg = canvas.line(time_series_df, x_col, y_col)
        img = tf.shade(agg, cmap=viridis)
        return tf.set_background(img, "black")

    def datashader_network_graph(self, connections_df, source_col='source_ip',
                                  target_col='target_ip', width=800, height=600):
        """
        Create a Datashader visualization of network connections.
        Useful for visualizing IP traffic patterns.

        Args:
            connections_df: DataFrame with source and target columns
            source_col: Column name for source nodes
            target_col: Column name for target nodes
            width: Canvas width in pixels
            height: Canvas height in pixels

        Returns:
            Datashader image object
        """
        # Aggregate connection counts
        canvas = ds.Canvas(plot_width=width, plot_height=height)

        # For network visualization, we need x,y coordinates
        # This is a simplified version - you'd typically use network layout algorithms
        agg = canvas.points(connections_df, source_col, target_col)
        img = tf.shade(agg, cmap=cc.fire)
        return tf.set_background(img, "black")

    def generate_sample_threat_data(self, n_points=1000000):
        """
        Generate sample threat detection data for demonstration.

        Args:
            n_points: Number of data points to generate

        Returns:
            DataFrame with sample threat data
        """
        np.random.seed(42)

        threat_types = ['Malware', 'Phishing', 'DDoS', 'SQL Injection', 'XSS',
                        'Brute Force', 'Zero Day', 'Ransomware']

        data = {
            'timestamp': np.random.randint(0, 86400, n_points),  # 24 hours in seconds
            'severity': np.random.beta(2, 5, n_points),  # Skewed towards lower severity
            'threat_type': np.random.choice(threat_types, n_points),
            'source_ip': np.random.randint(0, 255, n_points),
            'target_ip': np.random.randint(0, 255, n_points),
            'bytes_transferred': np.random.lognormal(10, 2, n_points)
        }

        return pd.DataFrame(data)

    def generate_sample_network_traffic(self, n_points=1000000):
        """
        Generate sample network traffic data for demonstration.

        Args:
            n_points: Number of data points to generate

        Returns:
            DataFrame with sample network traffic data
        """
        np.random.seed(42)

        protocols = ['TCP', 'UDP', 'ICMP', 'HTTP', 'HTTPS', 'SSH', 'FTP', 'DNS']

        data = {
            'timestamp': np.linspace(0, 86400, n_points),  # 24 hours
            'bytes': np.random.lognormal(8, 2, n_points),
            'protocol': np.random.choice(protocols, n_points),
            'packets': np.random.poisson(10, n_points),
            'source_port': np.random.randint(1024, 65535, n_points),
            'dest_port': np.random.randint(1, 65535, n_points)
        }

        return pd.DataFrame(data)
