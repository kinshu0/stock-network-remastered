import dash_core_components as dcc
import dash_html_components as html
from dash_dangerously_set_inner_html import DangerouslySetInnerHTML

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
                end_date = date(2009, 12, 31),
            ),
        ], className = 'row p-3'),
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
    className="col-2 p-3 d-flex flex-column justify-content-around"
)

middle_graph = html.Div(
    [dcc.Graph(id="my-graph", figure=plot)],
    className="col-8",
)

right_menu = html.Div([
        html.Div([
            html.Pre(id = 'hoverDataBox')
        ], className = 'row p-3'),
        html.Div([
            # DataTable(id = 'clickDataBox')
            # html.Pre(id = 'clickDataBox')
            html.Div([
                # DangerouslySetInnerHTML(da_table),
            ], id = 'clickDataBox')
        ], className = 'row p-3')
    ],
    className="col-2 p-3 d-flex flex-column justify-content-around"
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
            )
        ],
        className = 'navbar navbar-expand-lg navbar-light bg-light',
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