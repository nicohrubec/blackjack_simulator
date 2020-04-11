import pandas as pd

from src.game_simulation.game import Game
from src.game_simulation.players import player_factory
from src import configs


def run_simulation(settings):
    s = Simulator(n_games=settings['n_games'], n_rounds=settings['n_rounds'], num_decks=settings['num_decks'],
                  deck_penetration=settings['deck_penetrations'], player_type=settings['players'],
                  player_capital=settings['player_capital'])
    s.simulate()
    s.save_results()

    return s


class Simulator:
    def __init__(self, n_games, n_rounds, num_decks, deck_penetration, player_type, player_capital):
        self.n_games = n_games
        self.n_rounds = n_rounds
        self.num_decks = num_decks
        self.deck_penetration = deck_penetration
        self.player_type = player_type
        self.capital = player_capital
        self.results = None

    def simulate(self):
        # simulate every defined setting
        for player in self.player_type:
            for n_decks in self.num_decks:
                for penetration in self.deck_penetration:
                    for player_capital in self.capital:
                        setting_results = self.simulate_setting(player, n_decks, penetration, player_capital)

                        if self.results is None:  # no results stored so far --> init results df
                            self.results = pd.DataFrame(data=setting_results, columns=setting_results.columns)
                        else:  # append to previous results
                            self.results = pd.concat([self.results, setting_results])

    def simulate_setting(self, player_type, num_decks, deck_penetration, capital):
        setting_results = pd.DataFrame()

        for i in range(self.n_games):  # simulate one game with given setting
            player = player_factory(player_type, capital)
            game = Game(num_decks, player, self.n_rounds, deck_penetration)
            game_results = game.play_game()

            run_id = 'run_' + str(i)
            setting_results[run_id] = game_results

        self.calc_stats(setting_results)
        setting_results['player'] = player_type
        setting_results['num_decks'] = num_decks
        setting_results['deck_penetration'] = deck_penetration
        setting_results['capital'] = capital

        return setting_results

    @staticmethod
    def calc_stats(df):
        df['step_mean'] = df.mean(axis=1)
        df['step_std'] = df.std(axis=1)

        return df

    def save_results(self):
        path = configs.results_folder / 'results.csv'
        self.results.to_csv(path, index=False)

    def get_results(self):
        return self.results
