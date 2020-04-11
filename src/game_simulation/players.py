from src import configs
import pandas as pd
import numpy as np


# creates player instances from predefined options
def player_factory(player_type, capital):
    if player_type == 'basic':
        return BasicPlayer(init_capital=capital)
    elif player_type == 'strategic':
        return StrategicPlayer(init_capital=capital, file_name='thorp_strategy.xlsx')
    elif player_type == 'counter':
        return CountingPlayer(init_capital=capital, file_name='thorp_strategy.xlsx', bet_unit=5)
    else:
        raise ValueError('There is no such player.')


# Meta class from which further player types are inherited. To create new player types from this class you
# will have to implement both the betting strategy and the playing strategy for the player you want to create.
# Examples for how to create players from this player class are given below.
class Player(object):
    def __init__(self, init_capital):
        self.capital = init_capital

    def bet(self):
        raise NotImplementedError  # for a given game situation how much does the player want to bet ?

    def bet_amount(self, amount):
        self.capital -= amount

    def play(self, player_cards, dealer_cards):
        raise NotImplementedError  # for a given game situation what move does the player pick ?

    def add_capital(self, amount):
        self.capital += amount

    def get_capital(self):
        return self.capital

    def is_counter(self):
        return False  # reimplement this to True if the player deploys a card counting strategy


class BasicPlayer(Player):

    def bet(self):
        if self.capital > 5:
            self.capital -= 5
            return 5
        else:
            return 0

    def play(self, player_cards, dealer_cards):
        player_value = sum(player_cards)

        if player_cards[0] == player_cards[1]:
            return 'P'
        elif player_value == 11:
            return 'D'
        elif player_value < 17:
            return 'H'
        else:
            return 'S'


# This player deploys a naive betting strategy but uses a given strategy card (example in strategies folder)
# to guide his moves.
class StrategicPlayer(Player):

    def __init__(self, init_capital, file_name):
        super().__init__(init_capital)
        strategy_path = configs.strategies_folder / file_name
        self.strategy_card = pd.read_excel(strategy_path, index_col=0, header=1)
        self.strategy_card.columns = [str(col) for col in self.strategy_card.columns]  # convert columns to string
        self.strategy_card.index = self.strategy_card.index.map(str)  # convert index to string

    def bet(self, *args, **kwargs):  # naive betting
        if self.capital > 5:
            self.capital -= 5
            return 5
        else:
            return 0

    def play(self, player_cards, dealer_cards):
        player_value = sum(player_cards)

        if player_value == 21:
            return 'S'

        if len(player_cards) == 2:  # first move
            if player_cards[0] == player_cards[1]:  # split possible
                player_selector = 'D' + str(player_cards[0])  # eg D8 for double 8s
                return self.strategy_card.loc[player_selector, str(dealer_cards)]
            elif 11 in player_cards:  # soft hand
                if player_value <= 21:
                    player_selector = 'A' + str(player_value - 11)
                else:
                    player_selector = str(player_value - 10)
                return self.strategy_card.loc[player_selector, str(dealer_cards)]
            else:
                return self.strategy_card.loc[str(player_value), str(dealer_cards)]

        else:  # further moves --> only hit or stand allowed
            if 11 in player_cards:  # soft hand
                if player_value <= 21:
                    player_selector = 'A' + str(player_value - 11)
                else:
                    player_selector = str(player_value - 10)
                return self.strategy_card.loc[player_selector, str(dealer_cards)]
            else:  # hard hand
                return self.strategy_card.loc[str(player_value), str(dealer_cards)] if player_value < 21 else 'S'


# This player plays basic strategy like the strategic player but he spreads his bet sizes according
# to the current count. Count method used here is the HILO system. (+1 for 2-6, 0 for 7-9, -1 for 10 valued cards+ace)
# Bet size is then computed as true count (running_count / number of remaining decks) - 1 * bet unit
class CountingPlayer(StrategicPlayer):
    def __init__(self, init_capital, file_name, bet_unit):
        super().__init__(init_capital, file_name)
        self.bet_unit = bet_unit
        self.running_count = 0
        self.num_seen_cards = 0

    def bet(self, num_decks, *args, **kwargs):
        super(CountingPlayer, self).bet(num_decks, *args, **kwargs)
        return max((self.get_true_count(num_decks) - 1) * self.bet_unit, self.bet_unit)

    def update_count(self, *args):
        for cards in args:
            for card in cards:
                self.running_count += self.get_card_value(card)

            self.num_seen_cards += len(cards)

    def reset_count(self):
        self.running_count = 0
        self.num_seen_cards = 0

    @staticmethod
    def get_card_value(card):
        if card == 1 or card == 11 or card == 10:
            return -1
        elif card < 7:
            return 1
        else:
            return 0

    def get_true_count(self, num_decks):
        num_played_decks = np.round(self.num_seen_cards / 52)
        remaining_decks = num_decks - num_played_decks

        return self.running_count / remaining_decks

    def is_counter(self):
        return True
