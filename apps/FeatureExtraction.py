import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import preprocessing
import plotly.express as px
import dash_table
import datavizFunctions as fx
import matplotlib.pyplot as plt
import pandas as pd
from app import app

df = preprocessing.df

# -------------------------------------------------------------------------------------
layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                html.Label("Please Choose a Company"),
                width={"size": 6}
            )
        ]),
    dbc.Row(
        [
            dbc.Col(
                dcc.Dropdown(
                    id='company_dropdown',
                    options=[{'label': i, 'value': c} for c, i in enumerate(df["Company Name"].unique())],
                    value=[''],
                    multi=False,
                    clearable=False,
                    style={"color": '#222222'}),
                width=6
            )
        ]),
    dbc.Row(
        [
            dbc.Col(
                dash_table.DataTable(
                    id="dash_table",
                    data=[]

                )
            )
        ]),

])


@app.callback(
    Output(component_id="dash_table", component_property="data"),
    [Input(component_id="company_dropdown", component_property="value")]
)
def update_table(cp_dropdown):
    dff = df[df["Company Name"][cp_dropdown].isin(cp_dropdown)]
    f_list = fx.create_TopNFeatures(dff['Company Name'], 20)
    dff2 = pd.DataFrame({'Featurename': f_list})

    return dff2
