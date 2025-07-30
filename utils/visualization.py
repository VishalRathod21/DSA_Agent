import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def plot_time_complexity(complexity_data):
    """Visualize time complexity comparison"""
    fig, ax = plt.subplots()
    algorithms = list(complexity_data.keys())
    times = list(complexity_data.values())
    
    bars = ax.bar(algorithms, times, color=['#4e54c8', '#8f94fb', '#6a11cb'])
    ax.set_ylabel('Time Complexity (Big O)')
    ax.set_title('Algorithm Time Complexity Comparison')
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., 1.02*height,
                f'{height}', ha='center', va='bottom')
    
    return fig

def visualize_graph(edges):
    """Visualize a graph from a list of edges"""
    G = nx.Graph()
    G.add_edges_from(edges)
    
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='#4e54c8', 
            node_size=700, font_size=10, font_weight='bold', 
            edge_color='gray', width=1.5)
    
    return plt.gcf()

def plot_sorting_visualization(data, algorithm_name):
    """Create a bar chart visualization of sorting algorithm"""
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(range(len(data)), data, color='#4e54c8')
    
    # Customize the plot
    ax.set_title(f'{algorithm_name} - Sorting Visualization')
    ax.set_xlabel('Index')
    ax.set_ylabel('Value')
    
    # Add a color gradient based on value
    for i, bar in enumerate(bars):
        bar.set_facecolor(plt.cm.viridis(data[i]/max(data)))
    
    return fig
