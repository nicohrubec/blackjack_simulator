import sys

sys.path.append('..')

from src.simulation import Simulator

s = Simulator(n_games=100, n_rounds=100, num_decks=[4, 6], deck_penetration=[.4, .5], player_type=['basic'],
              player_capital=[1000, 2000])
s.simulate()
s.save_results()
