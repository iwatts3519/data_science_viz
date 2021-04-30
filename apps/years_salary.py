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
                html.Label("Please choose a range of number of years a company has been in business for"),
                width={"size": 6},

            )
        ]),
    dbc.Row(
        [
            dbc.Col(
                dcc.RangeSlider(
                    id="range_slider",
                    min=df['Years in Business'].min(),
                    max=df['Years in Business'].max(),
                    marks={i: f'{i}' for i in X},
                    value=[0, 10],
                    updatemode='drag'
                ), width=6

            ),
            dbc.Col(
                dcc.Dropdown(
                    id="Sector_Dropdown",
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
                dcc.Graph(id='Figure_4'),
                width=6
            ),
            dbc.Col(
                dcc.Graph(id='Figure_5'),
                width=6
            )
        ]),

])


# -------------------------------------------------------------------------------------
@app.callback(
    Output(component_id="Figure_4", component_property="figure"),
    [Input(component_id="range_slider", component_property="value")]
)
def update_graph(rng_slider):
    dff = df[(df["Years in Business"] >= rng_slider[0]) & (df["Years in Business"] <= rng_slider[1])]

    figd = px.scatter(dff,
                      x="Years in Business",
                      y="Maximum Salary (k)",
                      title="Maximum Salary (k) by Years in Business")

    return figd


@app.callback(
    Output(component_id="Figure_5", component_property='figure'),
    [Input(component_id="Sector_Dropdown", component_property='value')]
)
def update_bar(sec_dropdown):
    dff1 = df[df['Sector'].isin(sec_dropdown)]
    dfg = dff1.groupby('Sector', as_index=False).sum()

    fige = px.bar(dfg, x="Sector", y="Maximum Salary (k)")
    return fige
