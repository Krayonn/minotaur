import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash
import base64
import plotly.graph_objects as go

def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return f"data:{image_filename};base64," + base64.b64encode(image).decode('utf-8')

def click_fn(trace, points, state):
    print("CLICK")
    ind = points.point_inds[0]
    image_file = df['image'][ind]

global image_file
image_file = 'images/1117973.png'
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('compounds_dashboard', external_stylesheets=external_stylesheets)

df = pd.read_csv('compounds.csv')
# df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

available_indicators = ['compound_id','molecular_weight', 'a_log_p', 'num_rings']
colour_indicators = ['num_rings', 'target']

fig = go.FigureWidget()

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                placeholder="Select x-axis"
            ),
            dcc.Loading(
                id="loading-1",
                type="default",
                children=html.Div(id="loading-output-1")
            ),
        ],
        style={'width': '30%', 'float': 'left', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                placeholder="Select y-axis"
            ),
        ],style={'width': '30%', 'margin-left': '5%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='colour-column',
                options=[{'label': i, 'value': i} for i in colour_indicators],
                placeholder="Select size"
            ),
        ],style={'width': '30%', 'float': 'right', 'display': 'inline-block'})
    ]),
    dcc.Graph(style={'height': '600px'}, id='indicator-graphic'),
    html.Img(id='molecule-image', src=b64_image('dashboard/static/dashboard/'+image_file)),
    # html.Img(src=b64_image('dashboard/static/dashboard/+'images_file)),
])

@app.callback(
    [Output('indicator-graphic', 'figure'),
    Output('molecule-image', 'src')],
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('colour-column', 'value'),
     Input('indicator-graphic', 'clickData')])
def update_graph(xaxis_column_name, yaxis_column_name, colour_column_name, click_data
                 ):
    print("HERE")
    print(click_data)
    if (click_data):
        point_ind = click_data['points'][0]['pointIndex']
        print('Point ind: ',point_ind)
        image_file = df['image'][point_ind]
        print('Image file: ',image_file)
        src=b64_image('dashboard/static/dashboard/'+image_file)
    else:
        src=b64_image('dashboard/static/dashboard/images/27648.png')
    fig = px.scatter(df,xaxis_column_name, yaxis_column_name, color=colour_column_name, template='ggplot2')
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    fig.update_xaxes(title=xaxis_column_name)

    fig.update_yaxes(title=yaxis_column_name)

    return fig, src
