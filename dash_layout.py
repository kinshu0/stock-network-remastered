import dash_core_components as dcc
import dash_html_components as html
from dash_dangerously_set_inner_html import DangerouslySetInnerHTML
import numpy as np

from core_notebook import main
from datetime import date

from dash_table import DataTable

begin, end = '2007-01-01', '2008-12-31'

plot, G = main(begin, end)

da_table = ''

left_menu = html.Div([
        html.Div([
            html.H4('Time Range To Visualize', className = 'mb-4'),
            dcc.DatePickerRange(
                id='datepicker-range',
                min_date_allowed = date(1995, 1, 1),
                max_date_allowed = date(2024, 12, 31),
                initial_visible_month = date(2008, 1, 1),
                start_date = date(2008, 1, 1),
                end_date = date(2009, 12, 31),
            ),
        ], className = 'row p-3 mb-5'),
        html.Div([
            html.H4('Edge Definition Correlation Threshold', className = 'mb-4'),
            dcc.Slider(
                id='threshold',
                min = 0.4,
                max = 0.99,
                step = 0.01,
                value = 0.75,
                marks = {
                    x: f'{x}' for x in np.linspace(0.4, 0.99, 6)
                }
            )
        ], className = 'row p-3 mb-5'),
        html.Div([
            html.H4('Node Distance', className = 'mb-4'),
            dcc.Slider(
                id='node-distance',
                min = 0.01,
                max = 0.99,
                step = 0.01,
                value = 0.6,
                marks = {
                    0.1: '0.1',
                    0.2: '0.2',
                    0.3: '0.3',
                    0.4: '0.4',
                    0.5: '0.5',
                    0.6: '0.6',
                    0.7: '0.7',
                    0.8: '0.8',
                    0.9: '0.9',
                }
            )
        ], className = 'row p-3 mb-5'),
        html.Div([
            html.H4('Fruchterman-Reingold Simulation Iterations', className = 'mb-4'),
            dcc.Slider(
                id='iterations',
                min = 20,
                max = 300,
                step = 10,
                value = 100,
                marks = {
                    x: f'{x}' for x in range(20, 340, 40)
                }
            )
        ], className = 'row p-3 mb-5'),
        html.Div([
            html.Div([
                html.H4('Graph Metrics to Show', className = 'mb-4'),
                DangerouslySetInnerHTML('<b>Color:</b>'),
                dcc.RadioItems(
                    id='color_option',
                    options = [
                        {'label': 'none', 'value': 'nc'},
                        {'label': 'Sector', 'value': 'sector'},
                        {'label': 'Degree Centrality', 'value': 'dc'},
                        {'label': 'Closeness Centrality', 'value': 'cc'},
                        {'label': 'Betweenness Centrality', 'value': 'bc'},
                        {'label': 'Gain/Loss %', 'value': 'gl'},
                    ],
                    value = 'sector',
                    labelStyle={'display': 'block'},
                    className = 'mt-2',
                )
            ], className = 'row mb-2'),
            html.Div([
                DangerouslySetInnerHTML('<b>Size:</b>'),
                dcc.RadioItems(
                    id='size_option',
                    options = [
                        {'label': 'none', 'value': 'ns'},
                        {'label': 'Degree Centrality', 'value': 'dc'},
                        {'label': 'Closeness Centrality', 'value': 'cc'},
                        {'label': 'Betweenness Centrality', 'value': 'bc'},
                        {'label': 'Gain/Loss %', 'value': 'gl'},
                    ],
                    value = 'ns',
                    labelStyle={'display': 'block'},
                    className = 'mt-2',
                )
            ], className = 'row mb-2')
        ], className = 'row p-3')
    ],
    className="col-2 p-3 d-flex flex-column"
)

middle_graph = html.Div(
    [dcc.Graph(id="my-graph", figure=plot)],
    className="col-8",
)

right_menu = html.Div([
        # html.Div([
        #     html.Pre(id = 'hoverDataBox')
        # ], className = 'row p-3'),
        html.Div([
            # DataTable(id = 'clickDataBox')
            # html.Pre(id = 'clickDataBox')
            html.H5('Click on node to get its connections, edges are defined by pearson correlation coefficients; if tab says "updating...", wait for data to load (this example shows tickers taken from sandp500 index)', className='mt-3 mb-5'),
            html.H5('Rolling Mean Window Size', className='mb-3'),
            dcc.Slider(
                id='window-size',
                min = 1,
                max = 100,
                step = 1,
                value = 30,
                marks = {
                    1: '1',
                    30: '30',
                    50: '50',
                    60: '60',
                    75: '75',
                    90: '90',
                    100: '100',
                }
            ),
            html.Div([
                # DangerouslySetInnerHTML(da_table),
            ], id = 'clickDataBox')
        ], className = 'row p-3')
    ],
    className="col-2 p-3 d-flex flex-column"
)

# styles: for right side hover/click component
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

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




#########################################right side two output component
# html.Div(
#     className="two columns",
#     children=[
#         html.Div(
#             className='twelve columns',
#             children=[
#                 dcc.Markdown(d("""
#                 **Hover Data**
#                 Mouse over values in the graph.
#                 """)),
#                 html.Pre(id='hover-data', style=styles['pre'])
#             ],
#             style={'height': '400px'}),
#         html.Div(
#             className='twelve columns',
#             children=[
#                 dcc.Markdown(d("""
#                 **Click Data**
#                 Click on points in the graph.
#                 """)),
#                 html.Pre(id='click-data', style=styles['pre'])
#             ],
#             style={'height': '400px'})
#     ]
# )