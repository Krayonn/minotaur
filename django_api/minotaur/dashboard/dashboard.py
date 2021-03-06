import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash
import base64
import plotly.graph_objects as go

def b64_image(image_filename):
    # converts the data of the image file to base64 to be displayed on the web page
    with open(image_filename, 'rb') as f:
        image = f.read()
    return f"data:{image_filename};base64," + base64.b64encode(image).decode('utf-8')

def getDataTable(df, point_compound_id):
    df_comp = df[df['compound_id'] == point_compound_id]
    # Gets a list of dictionaries in form {'key': header value, 'value': body value}
    return [{'key':k, 'value':v} for k,v in df_comp[['compound_id', 'molecular_weight', 'a_log_p', 'molecular_formula', 'num_rings']].to_dict('rows')[0].items()]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('compounds_dashboard', external_stylesheets=external_stylesheets)

df = pd.read_csv('compounds.csv')
# To reolve floating points issues when displaying data
# In model they decimal field but this does not tranlate into dataframes
df['molecular_weight'] = df['molecular_weight'].apply(lambda x: round(x,5))
df['a_log_p'] = df['a_log_p'].apply(lambda x: round(x,3))

available_indicators = ['compound_id','molecular_weight', 'a_log_p', 'num_rings']
colour_indicators = ['num_rings', 'target']
assay_indicators = ['Kd', 'IC50']
assay_columns = ['result_id', 'target', 'result', 'operator', 'value', 'unit']

# data to populate compund table initially
dummy_data = df[df['compound_id'] == 1117973][assay_columns].to_dict('rows')

fig = go.FigureWidget()

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                placeholder="Select x-axis",
                value='molecular_weight'
            ),
            dcc.Loading(
                id="loading-1",
                type="default",
                children=html.Div(id="loading-output-1")
            ),
        ], style={'width': '30%', 'float': 'left', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                placeholder="Select y-axis",
                value='a_log_p'
            ),
        ],style={'width': '30%', 'margin-left': '5%', 'display': 'inline-block'})
    ]),

    html.Div([
        dcc.Graph(id='compounds-graph', style={'height': '600px'})
    ], style={'width': '59%', 'display': 'inline-block'}),

    html.Div([
        html.H3('Compound details'),
        html.Div([
            dash_table.DataTable(
                id='molecule-details',
                columns=[{"name": i, "id": i} for i in ['key', 'value']],
                style_cell={'textAlign': 'left',
                            'padding': '5px',
                            'minWidth': '50%',
                            'width': '50%',
                            'maxWidth': '50%'},
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'
                },
                data=getDataTable(df, 1117973))
        ], style={'table-layout': 'fixed'}),
        html.Div([
            html.Img(
                id='molecule-image',
                src=b64_image('dashboard/static/dashboard/images/1117973.png')
                )
        ], style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto', 'margin-top': 'auto', 'width':'40%', 'height': '40%'})
    ], style={'margin': 'auto', 'width': '39%', 'display': 'inline-block'}),
    html.Div([
        html.H3('Assay results for selected compound'),
        dash_table.DataTable(
            id='assay-results',
            columns=[{"name": i, "id": i} for i in assay_columns],
            style_cell={'textAlign': 'left', 'padding': '5px'},
            style_as_list_view=True,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold'
            },
            data=dummy_data)
    ], style={'margin-left': '10%', 'margin-right': '10%'}),
])

@app.callback(
    [Output('compounds-graph', 'figure'),
    Output('molecule-image', 'src'),
    Output('molecule-details', 'data')],
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('compounds-graph', 'hoverData')
     # Input('compounds-graph', 'clickData')
     ])
def update_graph(xaxis_column_name, yaxis_column_name, point_data
                 ):

    # cast to str otherwise it is a shallow copy
    xaxis_column_label = str(xaxis_column_name)
    yaxis_column_label = str(yaxis_column_name)

    # Update image of molecule
    if (point_data):
        point_ind = point_data['points'][0]['pointIndex']
        point_compound_id = df['compound_id'][point_ind]
        image_file = df[df['compound_id'] == point_compound_id]['image'].unique()[0]
        src=b64_image('dashboard/static/dashboard/'+image_file)
        # Update details of molecule
        data = getDataTable(df, point_compound_id)
    else:
        src=b64_image('dashboard/static/dashboard/images/27648.png')
        data = getDataTable(df, 1117973)

    # If compound id given filter df based of that
    df_fin = df

    # Update graph based on column choices
    fig = px.scatter(df_fin,xaxis_column_name, yaxis_column_name, color='num_rings', template='ggplot2')

    # ui revsion helps keep the state of fig (zooming, panning etc) the same unless one of the given components are changed when fig is updated
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest', uirevision=f'{xaxis_column_name}{yaxis_column_name}')

    # This returns componund id when point is hovered over
    fig.update_traces(customdata=df['compound_id'])
    fig.update_xaxes(title=xaxis_column_label)
    fig.update_yaxes(title=yaxis_column_label)

    return fig, src, data

@app.callback(
    Output('assay-results', 'data'),
    [Input('compounds-graph', 'hoverData')]
     # Input('compounds-graph', 'clickData')
     )
def update_table(point_data):
    point_compound_id = point_data['points'][0]['customdata']

    df_a = df[df['compound_id'] == point_compound_id]
    tdata = df_a[assay_columns].to_dict('rows')

    return tdata
