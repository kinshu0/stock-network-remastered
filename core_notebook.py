#!/usr/bin/env python
# coding: utf-8

# In[18]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

import pathlib

import networkx as nx
import plotly.express as px

# import plotly.graph_objects as go


# In[19]:


'''
Returns single dataframe and list of tickers
'''
def load_ts_data(data_folder):
    files = os.listdir(data_folder)
    stonks = []
    for i, x in enumerate(files):
        ticker = x[0:-4]
        try:
            df = pd.read_csv(data_folder / x, parse_dates=['timestamp'], usecols=['timestamp', 'close'], index_col='timestamp')
        except:
            print(f'{x} {i+1}/{len(files)} skipped, error...')
            continue
        df.columns = [ticker]
        stonks.append(df)
        print(f'{x} {i+1}/{len(files)} done...')
    return pd.concat(stonks, axis=1)


# In[20]:


def detrend(all_stocks):
    A = all_stocks.sort_index(ascending=False)
    B = A.shift(-1)
    pct_change = (A - B)/B
    return pct_change


# In[21]:


def rolling_window_preprocess(all_stocks, window_size = 30):
    rolling_all_stocks = all_stocks.sort_index(ascending=False).rolling(window_size).mean()
    return rolling_all_stocks


# In[22]:


def get_edges(pct_change, threshold = 0.8):
    correlation_matrix = pct_change.corr()
    chopped = np.tril(correlation_matrix, -1)
    
    r, c = np.where(abs(chopped) >= threshold)
        
    label_r = correlation_matrix.index[r]
    label_c = correlation_matrix.columns[c]
    
    pairs = pd.concat([ pd.Series(np.array(label_r)), pd.Series(np.array(label_c))], axis=1)
    return pairs


# In[23]:


def get_node_metrics(G, node_distance=0.6, simulation_iterations=100):
    pos = nx.spring_layout(G, node_distance, iterations=simulation_iterations)    
    degree = dict(G.degree)
    degree_centrality = nx.algorithms.centrality.degree_centrality(G)
    closeness_centrality = nx.algorithms.centrality.closeness_centrality(G)
    betweenness_centrality = nx.algorithms.centrality.betweenness_centrality(G)
    
    pos_df = pd.DataFrame.from_dict(pos, orient='index', columns=['x', 'y'])
    degree_df = pd.DataFrame.from_dict(degree, orient='index', columns=['degree'])
    degree_centrality_df = pd.DataFrame.from_dict(degree_centrality, orient='index', columns=['degree_centrality'])
    closeness_centrality_df = pd.DataFrame.from_dict(closeness_centrality, orient='index', columns=['closeness_centrality'])
    betweenness_centrality_df = pd.DataFrame.from_dict(betweenness_centrality, orient='index', columns=['betweenness_centrality'])
    
    node_properties_df = pd.concat([pos_df, degree_df, degree_centrality_df, closeness_centrality_df, betweenness_centrality_df], axis=1)
    return node_properties_df


# In[24]:


def edge_trace_convert(pairs, node_properties_df):
    a = pairs[0]
    b = pairs[1]
    x0s = node_properties_df['x'][a]
    y0s = node_properties_df['y'][a]
    x1s = node_properties_df['x'][b]
    y1s = node_properties_df['y'][b]
    
    edge_x = np.full(len(x0s) * 3, None)
    edge_x[::3] = x0s
    edge_x[::3] = x0s
    edge_x[1::3] = x1s
    
    edge_y = np.full(len(x0s) * 3, None)
    edge_y[::3] = y0s
    edge_y[1::3] = y1s
    
    return edge_x, edge_y


# In[25]:


def load_preprocess(data_folder):
    data = pathlib.Path(data_folder)
    all_stocks = load_ts_data(data)
    detrended = detrend(all_stocks)
    
    return detrended


# In[26]:


def create_graph(data, start, stop, tickers_to_show, rolling_window_size, threshold, additional_ticker_properties,
                node_distance = 0.6, simulation_iterations = 100):
    data.sort_index(inplace=True)
    rolled = rolling_window_preprocess(data[start:stop][tickers_to_show], rolling_window_size)
    connections = get_edges(rolled, threshold)
    
    G = nx.Graph()
    G.add_nodes_from(tickers_to_show)
    G.add_edges_from(zip(connections[0], connections[1]))
    
    node_properties_df = get_node_metrics(G, node_distance, simulation_iterations)
    gain_loss_df = (data + 1.00).prod()
    gain_loss_df.name = 'gain_loss'
    updated_node_properties = pd.concat([node_properties_df, additional_ticker_properties, gain_loss_df], axis=1, join='inner')
    
    '''add additional node properties through concat node_properties_df or index lookup append'''
    edge_x, edge_y = edge_trace_convert(connections, updated_node_properties)
    
    return updated_node_properties, edge_x, edge_y, G


# In[30]:


def plot_graph(node_properties, edge_x, edge_y, layout, graph_attrs):
    '''Add properties like size color etc to layout'''    
    lolz = px.scatter(
        node_properties, x='x', y='y', text=node_properties.index,
        template =  { 'layout':layout },
        hover_name = 'Company Name', hover_data = ['betweenness_centrality'],
#         size = size,
#         color = 'color'
        **graph_attrs
    )
    lolz.add_scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='rgba(120, 120, 120, 0.3)'),
        mode='lines'
    )
    return lolz
#     fig = go.Figure()

#     a = go.Scatter(
#         x=node_properties['x'], y=node_properties['y'], text=node_properties.index,
#         template =  { 'layout':layout },
#         hover_name = node_properties['Company Name'], hover_data = node_properties['betweenness_centrality'],
# #         size = size,
# #         color = 'color'
#         **graph_attrs
#     )
#     b = go.Scatter(
#         x=edge_x, y=edge_y,
#         line=dict(width=0.5, color='#888'),
#         mode='lines'
#     )
#     fig.update_layout(layout)
#     fig.add_trace(b)
#     fig.add_trace(a)
#     return fig


# In[28]:


data_folder = 'ticker_data'
data = load_preprocess(data_folder)

all_tickers = list(data.columns)

all_da_arguments = dict(
    start = '2020-01-01', stop = '2020-11-23',
    tickers_to_show = ['A', 'MMM', 'GOOG', 'AAPL'],
    rolling_window_size = 30,
    threshold = 0.75,
    additional_ticker_properties = pd.read_csv('symbols.csv', index_col='Ticker'),
)



def main(start = '2020-01-01', stop = '2020-11-23', tickers_to_show = all_tickers,
        rolling_window_size = 30, threshold = 0.75,
        additional_ticker_properties = pd.read_csv('symbols.csv', index_col='Ticker'),
        mark_color = 'sector', mark_size = 'ns', node_distance = 0.6, simulation_iterations = 100):
    
    layout = dict(
        height = 700,
        margin=dict(b=0,l=0,r=0,t=0),
        showlegend=True,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        hovermode = 'closest',
    )


    node_properties, edge_x, edge_y, G = create_graph(data, start, stop, tickers_to_show,
                                                   rolling_window_size, threshold, additional_ticker_properties,
                                                   node_distance, simulation_iterations)

    # if mark_color == '#fffb91':
    #     plot = plot_graph(node_properties, edge_x, edge_y, layout,
    #                      graph_attrs = dict(color = None, marker = dict(color=mark_color), size = node_properties[mark_size] + 8))
    # else:
    #     plot = plot_graph(node_properties, edge_x, edge_y, layout,
    #                      graph_attrs = dict(color = None, marker = dict(color='#fffb91'), size = node_properties[mark_size] + 8))
    #                     #  graph_attrs = dict(color = node_properties[mark_color], size = node_properties[mark_size] + 8))
    
    
    value_attr_key = {
        'nc': np.full(node_properties.shape[0], '#fffb91'),
        'ns': np.full(node_properties.shape[0], 15.0),
        'sector': node_properties['Sector'],
        'dc': node_properties['degree_centrality'],
        'cc': node_properties['closeness_centrality'],
        'bc': node_properties['betweenness_centrality'],
        'gl': node_properties['gain_loss']
    }


    plot = plot_graph(node_properties, edge_x, edge_y, layout,
                     graph_attrs = dict(color = value_attr_key[mark_color], size = value_attr_key[mark_size] ))


    return plot, G
