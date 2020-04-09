from pathlib import Path

project_path = Path.cwd().parent
results_folder = project_path / 'results'
strategies_folder = project_path / 'strategies'


def get_settings():
    settings = {}

    settings['n_games'] = 1000
    settings['n_rounds'] = 100
    settings['players'] = ['strategic', 'counter']
    settings['num_decks'] = [4, 6]
    settings['deck_penetrations'] = [.25, .5, .75]
    settings['player_capital'] = [10000]

    return settings
