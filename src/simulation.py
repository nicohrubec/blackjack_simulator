import pandas as pd

from src.game import Game
from src.players import player_factory


class Simulator():
    def __init__(self, n_games, n_rounds, num_decks, deck_penetration, player_type, player_capital):
        self.n_games = n_games
        self.n_rounds = n_rounds
        self.num_decks = num_decks
        self.deck_penetration = deck_penetration
        self.player_type = player_type
        self.capital = player_capital
        self.results = pd.DataFrame()

    def simulate(self):
        for i in range(self.n_games):
            player = player_factory(self.player_type, self.capital)
            game = Game(self.num_decks, player, self.n_rounds, self.deck_penetration)
            game_results = game.play_game()

            run_id = 'run_' + str(i)
            self.results[run_id] = game_results

        self.calc_stats()

        return self.results

    def calc_stats(self):
        self.results['step_mean'] = self.results.mean(axis=1)
        self.results['step_std'] = self.results.std(axis=1)
