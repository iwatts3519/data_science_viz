import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from app import app
import preprocessing

df = preprocessing.df

X = range(0, 401, 10)

# -------------------------------------------------------------------------------------
layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                html.Label("Please choose a sector from the drop down"),
                width={"size": 6, "offset": 1},

            )
        ]),
    dbc.Row(
        [

            dbc.Col(
                dcc.Dropdown(
                    id="Sec_Dropdown",
                    options=[{'label': i, 'value': i} for i in df['Sector'].unique()],
                    value=['Consumer Services'],
                    multi=True,
                    clearable=False

                ), width=6

            )
        ]),
    dbc.Row(
        [
            dbc.Col(
                dcc.Graph(id='Figure_1'),
                width=6
            )
        ]),

])


# -------------------------------------------------------------------------------------
@app.callback(
    Output(component_id="Figure_1", component_property="figure"),
    [Input(component_id="Sec_Dropdown", component_property="value")]
)
def update_graph(sec_dropdown):
    dff1 = df[df['Sector'].isin(sec_dropdown)]

    figa = px.box(dff1,
                  x="Sector",
                  y="Years in Business",
                  title="Years in Business by Sector")

    return figa
