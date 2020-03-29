import sys

sys.path.append('..')

from src.game_simulation.simulation import Simulator

if __name__ == '__main__':
    s = Simulator(n_games=100, n_rounds=100, num_decks=[4, 6], deck_penetration=[.4, .5], player_type=['basic'],
                  player_capital=[1000, 2000])
    s.simulate()
    s.save_results()
