def player_factory(player_type, capital):
    if player_type == 'basic':
        return BasicPlayer(init_capital=capital)
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
