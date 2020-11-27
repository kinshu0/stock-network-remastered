#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import networkx as nx
import plotly.graph_objs as go

import pandas as pd
# from colour import Color
from datetime import date
import json

from core_notebook import main, load_preprocess

from dash_dangerously_set_inner_html import DangerouslySetInnerHTML

# from dash_layout import layout, begin, end, G, plot, da_table
# from dash_layout import layout, begin, end, da_table
from dash_layout import left_menu, right_menu


import pickle

data_folder = 'ticker_data'
# data = load_preprocess(data_folder)

data = pickle.load(open('data', 'rb'))

all_tickers = list(data.columns)



# import the css template, and pass the css template into dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css', ]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Stock Network"


begin, end = '2007-01-01', '2008-12-31'
plot, G = main(begin, end, tickers_to_show=all_tickers ,data=data)

middle_graph = html.Div(
    [dcc.Graph(id="my-graph", figure=plot)],
    className="col-8",
)

layout = html.Div([
    ########################################################################################### Navigation Bar
    html.Nav(
        [
            html.A(
                'Stock Network Graph', className = 'h1 m-2 text-dark', href = '#', id = 'navicon', style = {'text-decoration': 'none'}
            ),
            html.A(
                'Created by Kinshu Gupta', className = 'align-self-end', href = 'mailto:kinshugupta2002@gmail.com'
            )
        ],
        className = 'navbar d-flex navbar-expand-lg navbar-light bg-light',
    ),
    
    #############################################################################################define the row
    html.Div([
        html.Div(
            [
                left_menu,
                middle_graph,
                right_menu,
            ],
            className = 'row'
        ),
    ], className="container-fluid d-flex justify-content-around",)

], className='', style = {})

app.layout = layout

server = app.server

###################################callback for left side components
@app.callback(
    dash.dependencies.Output('my-graph', 'figure'),
    [dash.dependencies.Input('datepicker-range', 'start_date'), dash.dependencies.Input('datepicker-range', 'end_date'),
    dash.dependencies.Input('color_option', 'value'), dash.dependencies.Input('size_option', 'value'), dash.dependencies.Input('threshold', 'value'),
    dash.dependencies.Input('node-distance', 'value'), dash.dependencies.Input('iterations', 'value'), dash.dependencies.Input('window-size', 'value')]
)
def update_output(start_date, end_date, color, size, threshold, noded, iterations, window):
    begin, end = start_date, end_date
    global plot
    global G
    plot, G = main(start=start_date, stop=end_date, mark_color = color, mark_size = size, threshold=threshold, node_distance=noded, simulation_iterations=iterations,
    rolling_window_size=window, tickers_to_show=all_tickers, data=data)
    return plot
    # to update the global variable of YEAR and ACCOUNT



################################callback for right side components
# @app.callback(
#     dash.dependencies.Output('hoverDataBox', 'children'),
#     [dash.dependencies.Input('my-graph', 'hoverData')])
# def display_hover_data(hoverData):
#     return json.dumps(hoverData, indent=2)


@app.callback(
    # dash.dependencies.Output('clickDataBox', 'data'),
    dash.dependencies.Output('clickDataBox', 'children'),
    [dash.dependencies.Input('my-graph', 'clickData')])
def display_click_data(clickData):
    if clickData:
        ticker = clickData['points'][0]['text']
        list_of_correlations = nx.function.neighbors(G, ticker)
        # optext = '\n'.join(list_of_correlations)
        optext = pd.DataFrame(list_of_correlations, columns = [f'Nodes Connected to {ticker}']).to_html(classes=['table-striped', 'table-hover'])
        
        return DangerouslySetInnerHTML(optext)
        # global da_table
        # da_table = optext
        # return optext



if __name__ == '__main__':
    app.run_server(debug=False)