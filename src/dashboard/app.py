import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import random

from src import configs

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# selection for individual run visualisation
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
    num_decks, deck_penetration, players, budgets = df.num_decks.unique(), df.deck_penetration.unique(), \
                                                    df.player.unique(), df.capital.unique()
    num_settings = len(num_decks) * len(deck_penetration) * len(players) * len(budgets)
    num_rounds = int(len(df) / num_settings)

    return html.Div([
        html.Div([
            html.H4(title)
        ], style={"align": "bottom"}),
        dcc.Graph(
            id=str(stat) + '_results' + str(capital),
            figure={
                'data': [
                    dict(
                        x=[i for i in range(1, num_rounds + 1)],
                        y=df[(df.num_decks == d) & (df.capital == capital) & (df.deck_penetration == p) &
                             (df.player == i)][('step_' + str(stat))],
                        mode='lines',
                        name=str(i) + ' player, ' + str(p) + ' deck penetration, ' + str(d) + ' decks'
                    ) for d in num_decks for p in deck_penetration for i in players
                ],
                'layout': dict(
                    xaxis={'title': 'Num rounds after game start'},
                    yaxis={'title': 'Mean remaining capital of the player'},
                    legend={'x': 1, 'y': 1}
                )
            }
        )
    ])


# create line graphs comparing statistics of the individual simulation setting results
def get_summary_graphs(df, capital):
    return html.Div([
        get_summary_graph(df, capital, 'mean', 'Mean remaining capital at a given step for player '
                                               'with init capital of ' + str(capital)),
        get_summary_graph(df, capital, 'std', 'Std of remaining capital at a given step for player '
                                              'with init capital of ' + str(capital))
    ], style={'columnCount': 1})


# show data.head()
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


# line graph of a sample of the individual run results for a selected setting
def generate_raw_figure(df, sample=100):
    run_cols = [col for col in df.columns if col.startswith('run')]
    return {
        'data': [
            dict(
                x=[i for i in range(1, 101)],
                y=df[run_name],
                mode='lines',
                name=run_name
            ) for run_name in random.sample(run_cols, min(sample, len(run_cols)))
        ],
        'layout': dict(
            xaxis={'title': 'Num rounds after game start'},
            yaxis={'title': 'Remaining capital of the player'}
        )
    }


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
        html.Div(id='my-div'),
        dcc.Graph(id='raw-values-line-plot')
    ], style={'width': '80%', 'padding-left': '10%', 'padding-right': '10%'})

    # adapt shown table and individual run line graph based on user selection
    @dashboard.callback(
        [Output('my-div', 'children'), Output('raw-values-line-plot', 'figure')],
        [Input('player_dd', 'value'), Input('num_decks_dd', 'value'), Input('penetration_dd', 'value'),
         Input('capital_dd', 'value')]
    )
    def update_table(player_value, num_decks_value, penetration_value, capital_value):
        dff = data[data['player'] == player_value]
        dff = dff[dff['num_decks'] == num_decks_value]
        dff = dff[dff['deck_penetration'] == penetration_value]
        dff = dff[dff['capital'] == capital_value]

        return generate_table(dff), generate_raw_figure(dff)

    return dashboard


if __name__ == '__main__':
    path = configs.project_path.parent / 'results' / 'results.csv'
    results = pd.read_csv(path)
    app = get_app(data=results)
    app.run_server(debug=True)
