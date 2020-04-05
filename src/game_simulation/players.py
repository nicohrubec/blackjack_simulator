from src import configs
import pandas as pd


def player_factory(player_type, capital):
    if player_type == 'basic':
        return BasicPlayer(init_capital=capital)
    elif player_type == 'strategic':
        return StrategicPlayer(init_capital=capital, file_name='thorp_strategy.xlsx')
    else:
        raise ValueError('There is no such player.')


class Player(object):
    def __init__(self, init_capital):
        self.capital = init_capital

    def bet(self):
        raise NotImplementedError

    def bet_amount(self, amount):
        self.capital -= amount

    def play(self, player_cards, dealer_cards):
        raise NotImplementedError

    def add_capital(self, amount):
        self.capital += amount

    def get_capital(self):
        return self.capital


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


class StrategicPlayer(Player):

    def __init__(self, init_capital, file_name):
        super().__init__(init_capital)
        strategy_path = configs.strategies_folder / file_name
        self.strategy_card = pd.read_excel(strategy_path, index_col=0, header=1)
        self.strategy_card.columns = [str(col) for col in self.strategy_card.columns]  # convert columns to string
        self.strategy_card.index = self.strategy_card.index.map(str)  # convert index to string

    def bet(self):  # naive betting
        if self.capital > 5:
            self.capital -= 5
            return 5
        else:
            return 0

    def play(self, player_cards, dealer_cards):
        player_value = sum(player_cards)

        if player_value == 21:
            return 'S'

        if len(player_cards) == 2:
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

        else:
            if 11 in player_cards:
                if player_value <= 21:
                    player_selector = 'A' + str(player_value - 11)
                else:
                    player_selector = str(player_value - 10)
                return self.strategy_card.loc[player_selector, str(dealer_cards)]
            else:
                return self.strategy_card.loc[str(player_value), str(dealer_cards)] if player_value < 21 else 'S'
