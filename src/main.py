import sys

sys.path.append('..')

from src.game_simulation.simulation import Simulator

if __name__ == '__main__':
    s = Simulator(n_games=5000, n_rounds=100, num_decks=[4], deck_penetration=[.5],
                  player_type=['strategic'],
                  player_capital=[1000])
    s.simulate()
    s.save_results()
