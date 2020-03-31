import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def generate_table(df, rows=5):
    return html.Div([html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(min(len(df), rows))
        ]),
    ])], style={'width': '100%', 'overflowX': 'scroll'})


def get_dropdown(title, id, options):
    return html.Div([
        html.H4(title),
        dcc.Dropdown(
            id=id,
            options=[{'label': i, 'value': i} for i in options],
            value=options[0]
        )
    ], style={'margin': '2%'})


def get_summary_graph(df, capital, stat, title):
    return html.Div([
        html.Div([
            html.H4(title)
        ], style={"align": "bottom"}),
        dcc.Graph(
            id=str(stat) + '_results' + str(capital),
            figure={
                'data': [
                    dict(
                        x=[i for i in range(1, 101)],
                        y=df[(df.num_decks == d) & (df.capital == capital) & (df.deck_penetration == p) &
                             (df.player == i)][('step_' + str(stat))],
                        mode='lines',
                        name=str(i) + ' player, ' + str(p) + ' deck penetration, ' + str(d) + ' decks'
                    ) for d in df.num_decks.unique() for p in df.deck_penetration.unique() for i in df.player.unique()
                ],
                'layout': dict(
                    xaxis={'title': 'Num rounds after game start'},
                    yaxis={'title': 'Mean remaining capital of the player'},
                    legend={'x': 0, 'y': 0}
                )
            }
        )
    ])


def get_summary_graphs(df, capital):
    return html.Div([
        get_summary_graph(df, capital, 'mean', 'Mean remaining capital at a given step for player '
                                               'with init capital of ' + str(capital)),
        get_summary_graph(df, capital, 'std', 'Std of remaining capital at a given step for player '
                                              'with init capital of ' + str(capital))
    ], style={'columnCount': 2})


def get_app(data):
    dashboard = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    dashboard.layout = html.Div([
        html.H1('Blackjack Simulation'),

        html.H2('1. Summary statistics of all Simulations'),
        html.Div([get_summary_graphs(data, c) for c in data.capital.unique()]),

        html.H2('2. Look at specific simulations'),
        html.H3('Simulation Settings'),
        get_dropdown('Player', 'player_dd', data.player.unique()),
        get_dropdown('Num Decks', 'num_decks_dd', data.num_decks.unique()),
        get_dropdown('Deck Penetration', 'penetration_dd', data.deck_penetration.unique()),
        get_dropdown('Player Capital', 'capital_dd', data.capital.unique()),
        generate_table(data)
    ], style={'width': '80%', 'padding-left': '10%', 'padding-right': '10%'})

    return dashboard


if __name__ == '__main__':
    results = pd.read_csv("../../results/results.csv")
    app = get_app(data=results)
    app.run_server(debug=True)
