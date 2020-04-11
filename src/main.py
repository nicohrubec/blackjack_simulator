import sys

sys.path.append('..')

from src.configs import get_settings
from src.game_simulation.simulation import Simulator
from src.dashboard.app import get_app


def run_simulation(settings):
    s = Simulator(n_games=settings['n_games'], n_rounds=settings['n_rounds'], num_decks=settings['num_decks'],
                  deck_penetration=settings['deck_penetrations'], player_type=settings['players'],
                  player_capital=settings['player_capital'])
    s.simulate()
    s.save_results()

    return s


if __name__ == '__main__':
    settings_dict = get_settings()
    simulator = run_simulation(settings_dict)
    app = get_app(simulator.get_results())
    app.run_server(debug=False)
