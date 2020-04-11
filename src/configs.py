from pathlib import Path

project_path = Path.cwd().parent
results_folder = project_path / 'results'
strategies_folder = project_path / 'strategies'


# Ask the user for what to simulate
def get_settings():
    settings = {}

    settings['n_games'] = int(input('Enter the number of games to simulate: (int) '))
    settings['n_rounds'] = int(input('Enter the number of rounds per game to simulate: (int) '))

    player_input = input('Enter the player types you want to simulate: (e.g. basic or counter) ')
    settings['players'] = [str(play.strip()) for play in player_input.split(',')]

    num_decks_input = input('Enter the number of decks you want to simulate: (list of ints eg 4, 6) ')
    settings['num_decks'] = [int(n_decks) for n_decks in num_decks_input.split(',')]

    p_input = input('Enter the deck penetrations you want to simulate: (list of floats eg .25, .5) ')
    settings['deck_penetrations'] = [float(p) for p in p_input.split(',')]

    capital_input = input('Enter the player capitals you want to simulate: (list of ints eg 1000, 5000) ')
    settings['player_capital'] = [int(c) for c in capital_input.split(',')]

    return settings
