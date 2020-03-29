import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def generate_table(df, rows=5):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(min(len(df), rows))
        ]),
    ])


def get_dropdown(title, id, options):
    return html.Div([
        html.H4(title),
        dcc.Dropdown(
            id=id,
            options=[{'label': i, 'value': i} for i in options],
            value=options[0]
        )
    ], style={'margin': '2%'})


def get_app(data):
    dashboard = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    dashboard.layout = html.Div([
        html.H1('Blackjack Simulation'),
        html.H3('Simulation Settings'),
        get_dropdown('Player', 'player_dd', data.player.unique()),
        get_dropdown('Num Decks', 'num_decks_dd', data.num_decks.unique()),
        get_dropdown('Deck Penetration', 'penetration_dd', data.deck_penetration.unique()),
        get_dropdown('Player Capital', 'capital_dd', data.capital.unique()),
        generate_table(data)
    ], style={'width': '80%', 'margin': '2%'})

    return dashboard


if __name__ == '__main__':
    results = pd.read_csv("../../results/results.csv")
    app = get_app(data=results)
    app.run_server(debug=True)
