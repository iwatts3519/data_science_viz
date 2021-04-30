import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import datavizFunctions as fx
from app import app
from apps import welcome, years_salary, years_sector, wordclouds

from app import server

# Create sample Wordclouds for two different companies (0 and 4)
fx.createWordCloud(0, 1)
fx.createWordCloud(4, 2)

app.layout = html.Div([

    dbc.Row([
        dbc.Col([
            dbc.NavbarSimple([
                dbc.NavItem([

                    dbc.Button(dbc.NavLink("Salary ", href='/apps/years_salary'), className="lg mx-2",
                               color="primary")
                ]),
                dbc.NavItem([

                    dbc.Button(dbc.NavLink("Sector ", href='/apps/years_sector'), className="lg mx-2",
                               color="primary")
                ]),

                dbc.NavItem([
                    dbc.Button(dbc.NavLink("Wordclouds ", href='/apps/wordclouds'), className="lg mx-2",
                               color="primary")
                ])
            ],
                brand="Data Science Job Analytics",
                brand_href="apps/welcome",
                fluid=True,
                dark=True,
                color="primary")
        ], width=12)
    ]),

    dcc.Location(id="url", refresh=False, pathname="/apps/welcome"),
    html.Div(id='page-content', children=[]),
    dbc.Row(
        dbc.Col(
            html.Div("(c) 2012 - Ian Watts - Keele University -  Built by Dash on Flask",
                     style={"text-align": "center"}))
    )
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')]
              )
def display_page(pathname):
    if pathname == '/apps/years_salary':
        return years_salary.layout
    if pathname == '/apps/years_sector':
        return years_sector.layout
    if pathname == '/apps/wordclouds':
        return wordclouds.layout
    else:
        return welcome.layout


if __name__ == '__main__':
    app.run_server(debug=False)
