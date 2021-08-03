import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px

import networkx as nx
import pandas as pd
import numpy as np

import base64
import io

    
default_stylesheet = [
    {
        "selector": 'node',
        'style': {
            "opacity": 0.65,
        }
    },
    {
        "selector": 'edge',
        'style': {
            "curve-style": "bezier",
        }
    },
]
                
external_stylesheets = [dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                cyto.Cytoscape(
                    id='cytoscape',

                    style={'width': '100%', 'height': '900px'},
                    ),
                width = 8,
                ),
            dbc.Col(
                html.Div(children=[
                    dcc.Tabs(id='tabs', children=[
                        dcc.Tab(label='Control Panel', children=[
                            html.H4('Layout:'),
                            dcc.Dropdown(
                                id='layout-dropdown',
                                value='random',
                                clearable=False,
                                options=[
                                    {'label': name.capitalize(), 'value': name}
                                    for name in ['grid', 'random', 'circle', 'cose', 'concentric']
                                ]),
                            
                            html.H4('Node Properties:'),
                            
                            html.Label('Labels:'),
                            dcc.RadioItems(
                                id = "node-label",
                                options=[
                                    {'label': 'On', 'value': 'True'},
                                    {'label': 'Off', 'value': 'False'},
                                    ],
                                value='True'
                                ),
                            
                            html.Label('Color:'),
                            dcc.Input(
                                id = "node-color",
                                value='gray', 
                                type='text'
                                ),
                            
                            html.Label('Opacity:'),
                            dcc.Input(
                                id = "node-opacity",
                                value=0.65, 
                                type='number',
                                min = 0,
                                max = 1,
                                step = 0.01,
                                ),

                            
                            html.Label('Size:'),
                            dcc.Input(
                                id = "node-size",
                                value=25, 
                                type='number',
                                min = 0,
                                ),
                       
                            
                        
                            html.H4('Edge Properties:'),
                            
                            html.Label('Labels:'),
                            dcc.RadioItems(
                                id = "edge-label",
                                options=[
                                    {'label': 'On', 'value': 'True'},
                                    {'label': 'Off', 'value': 'False'},
                                    ],
                                value='True'
                                ),
                            
                            html.Label('Color:'),
                            dcc.Input(
                                id = "edge-color",
                                value='gray', 
                                type='text'
                                ),
                            
                            html.Label('Opacity:'),
                            dcc.Input(
                                id = "edge-opacity",
                                value=0.65, 
                                type='number',
                                min = 0,
                                max = 1,
                                step = 0.01,
                                ),

                            
                            html.Label('Size:'),
                            dcc.Input(
                                id = "edge-size",
                                value=3, 
                                type='number',
                                min = 0,
                                step = 0.2,
                                ),
                            
                            html.Label('Arrows:'),
                            dcc.RadioItems(
                                id = "arrows",
                                options=[
                                    {'label': 'On', 'value': 'True'},
                                    {'label': 'Off', 'value': 'False'},
                                    ],
                                value='False'
                                ),
                            html.Label('Arrow Size:'),
                            dcc.Input(
                                id = "arrow-size",
                                value=1, 
                                type='number',
                                min = 0,
                                step = 0.2,
                                ),
                            ]),
                        dcc.Tab(label='Upload Network', children=[
                            dcc.Upload(
                                id='upload-data',
                                children=html.Div([
                                    'Drag and Drop or ',
                                    html.A('Select Files')
                                    ]),
                                style={
                                    'width': '100%',
                                    'height': '60px',
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin': '10px'
                                    },
                                # Allow multiple files to be uploaded
                                multiple=False
                                ),
                            ]),
                        dcc.Tab(label='Generate Network', children=[
                            html.H4('Network Type:'),
                            dcc.Dropdown(
                                id='net-type-dropdown',
                                value='Random',
                                clearable=False,
                                options=[
                                    {'label': name.capitalize(), 'value': name}
                                    for name in ['Uploaded', 'Random', 'Small World', 'Scale Free']
                                ]),
                            html.H4('Number of Nodes:'),
                            dcc.Input(
                                id = "num-nodes",
                                value=25, 
                                type='number',
                                min = 0,
                                step = 1,
                                ),
                            html.Label('Random network/small world connection probability:'),
                            dcc.Input(
                                id = "prob",
                                value=0.15, 
                                type='number',
                                min = 0.0,
                                max = 1.0,
                                step = 0.01,
                                ),
                            html.Label('Small world starting connections:'),
                            dcc.Input(
                                id = "num-connections",
                                value=2, 
                                type='number',
                                min = 2,
                                step = 2,
                                ),
                            html.Label('Scale free connections:'),
                            dcc.Input(
                                id = "scale-connections",
                                value=2, 
                                type='number',
                                min = 1,
                                step = 1,
                                ),
                            ])
                        ])
                    ])
                )
            ]
        ),
    ],
    style={'width': '75%', 'margin': 'auto'},
)



@app.callback(Output('cytoscape', 'layout'),
              Input('layout-dropdown', 'value'))
def update_layout(layout):
    return {
        'name': layout,
        'animate': True
    }

@app.callback(Output('cytoscape', 'stylesheet'),
              Input('node-label', 'value'),
              Input('node-color', 'value'),
              Input('node-opacity', 'value'),
              Input('node-size', 'value'),
              Input('edge-label', 'value'),
              Input('edge-color', 'value'),
              Input('edge-opacity', 'value'),
              Input('edge-size', 'value'),
              Input('arrows', 'value'),
              Input('arrow-size', 'value')
              )
def update_stylesheet(node_label, 
                      node_color, 
                      node_opacity,
                      node_size,
                      edge_label, 
                      edge_color, 
                      edge_opacity,
                      edge_size,
                      arrows,
                      arrow_size):
    stylesheet = []
    stylesheet.extend(default_stylesheet)
    
    stylesheet.append(
        {
            "selector": 'node',
            'style': {
                'width': node_size,
                'height': node_size,
                'background-color': node_color,
                'opacity': node_opacity
                },
            }
        )
    stylesheet.append(
            {
                "selector": 'edge',
                'style': {
                    'width': edge_size,
                    'line-color': edge_color,
                    'opacity': edge_opacity,
                    }
                }
            )
    if arrows == 'True':
        stylesheet.append(
            {
                "selector": 'edge',
                'style': {
                    'target-arrow-shape': 'vee',
                    'arrow-scale': arrow_size,
                    }
                }
            )
        
    
    if node_label == 'True':
        stylesheet.append({
                'selector': 'node',
                'style': {
                    'content': 'data(label)'
                    }
                }
            )
    if edge_label == 'True':
        stylesheet.append({
                'selector': 'edge',
                'style': {
                    'content': 'data(weight)'
                    }
                }
            )
    return stylesheet

@app.callback(Output('cytoscape', 'elements'),
              Input('net-type-dropdown', 'value'),
              Input('prob', 'value'),
              Input('num-connections', 'value'),
              Input('scale-connections', 'value'),
              Input('num-nodes', 'value'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_output(net_type, p, k1, k2, n, contents, name):
    if net_type == "Uploaded" and contents is not None:
        content_type, content_string = contents.split(',')
    
        decoded = base64.b64decode(content_string)
        try:
                # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            
        except Exception as e:
            pass
        
        elements = []
        
        unique_ids = {}
        for i, x in enumerate(np.unique([df['source'], df['target']])):
            unique_ids[str(x)] = i        
            elements.append({"data": {"id": i, "label": str(x)}})
            
        
        weighted = ('weight' in df.columns)
        for index, row in df.iterrows():
            if not weighted:
                elements.append({
                    'data': {
                        'source': unique_ids[str(row['source'])],
                        'target': unique_ids[str(row['target'])]
                    }
                })
            else:
                elements.append({
                'data': {
                    'source': unique_ids[str(row['source'])],
                    'target': unique_ids[str(row['target'])],
                    'weight': str(row['weight'])
                }
            })

        return elements
    
    if net_type == "Random":
        G = nx.erdos_renyi_graph(n, p, directed=False)
    if net_type == "Small World":
        G = nx.watts_strogatz_graph(n, k1, p)
    if net_type == "Scale Free":
        G = nx.barabasi_albert_graph(n, k2)
        
    
        
    elements = []
        
    for x in G.nodes:
        elements.append({"data": {"id": x, "label": str(x)}})
        
    

    for e in G.edges:
        elements.append({
            'data': {
                'source': e[0],
                'target': e[1]
            }
        })
        
        
    return elements

    return []



                    

if __name__ == '__main__':
    app.run_server(debug=True)
