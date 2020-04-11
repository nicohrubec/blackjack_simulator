import sys

sys.path.append('..')

from src.configs import get_settings
from src.game_simulation.simulation import run_simulation
from src.dashboard.app import get_app


if __name__ == '__main__':
    settings_dict = get_settings()
    simulator = run_simulation(settings_dict)
    app = get_app(simulator.get_results())
    app.run_server(debug=False)
