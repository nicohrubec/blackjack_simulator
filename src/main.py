import sys

sys.path.append('..')

from src.game_simulation.simulation import Simulator

if __name__ == '__main__':
    s = Simulator(n_games=1000, n_rounds=100, num_decks=[4, 6], deck_penetration=[.75, .5, .25],
                  player_type=['counter', 'strategic'],
                  player_capital=[10000])
    s.simulate()
    s.save_results()
