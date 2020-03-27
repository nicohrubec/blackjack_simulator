def player_factory(player_type, capital):
    if player_type == 'basic':
        return Player(capital)
    else:
        raise ValueError('There is no such player.')


class Player:

    def __init__(self, init_capital):
        self.capital = init_capital

    def bet(self):  # bet based on strategy
        if self.capital > 5:
            self.capital -= 5
            return 5
        else:
            return 0

    def bet_amount(self, amount):
        self.capital -= amount

    def play(self, player_cards, dealer_card):  # hit or stand for given game setting
        player_value = sum(player_cards)

        if player_value == 11:
            return 'D'
        elif player_value < 17:
            return 'H'
        else:
            return 'S'

    def add_capital(self, amount):
        self.capital += amount

    def get_capital(self):
        return self.capital
