import numpy as np


class Game:

    def __init__(self, num_decks, player, max_rounds, deck_penetration):
        self.num_decks = num_decks
        self.player = player
        self.max_rounds = max_rounds
        self.deck_penetration = deck_penetration

        self.card_deck = self.init_card_deck()
        self.played_cards = []
        self.shuffle_deck()

    def init_card_deck(self):
        deck = []

        for i in range(2, 14):
            if i < 10:
                deck.extend([i] * 4 * self.num_decks)
            elif i < 13:  # 10, boy, queen, king all with value 10
                deck.extend([10] * 4 * self.num_decks)
            else:  # ace init with value 11
                deck.extend([11] * 4 * self.num_decks)

        return deck

    def shuffle_deck(self):
        self.card_deck.extend(self.played_cards)  # put all cards into one stack
        np.random.shuffle(self.card_deck)

        self.played_cards = []  # no cards played after shuffling

    def play_game(self):
        for i in range(self.max_rounds):
            bet = self.player.bet()  # how much does the player wanna play for ?

            if bet > 0:
                self.play_round(bet)
            else:  # terminate game as player does not bet
                break

            if len(self.played_cards) / (52 * self.num_decks) > self.deck_penetration:
                self.shuffle_deck()

    def play_round(self, bet):
        # deal some cards
        player_cards = [self.card_deck.pop(), self.card_deck.pop()]
        dealer_cards = [self.card_deck.pop(), self.card_deck.pop()]
        player_bust = False
        dealer_bust = False
        blackjack = False

        if sum(player_cards) == 21:  # blackjack: ace + value 10 card = 21
            if not sum(dealer_cards) == 21:  # dealer has no blackjack
                print("BLACKJACK")
                self.player.add_capital(2.5 * bet)  # bet + 1.5 * bet
            else:  # dealer has blackjack as well
                self.player.add_capital(bet)  # player gets back his bet

            blackjack = True  # round done

        if not blackjack:  # player does not have a blackjack so just start round
            # player begins
            while True:
                # information of relevance for the decision of the player is the value of his cards and the value of
                # the dealer card he can see
                move = self.player.play(player_cards, dealer_cards[0])

                if move == 'H':  # HIT
                    player_cards.append(self.card_deck.pop())
                elif move == 'S':  # STAND
                    break
                elif move == 'D':  # DOUBLE DOWN
                    self.player.bet_amount(bet)  # double the bet
                    player_cards.append(self.card_deck.pop())  # player gets another card
                    break  # now its the dealers turn

                # check for bust
                if sum(player_cards) > 21:
                    # check if the hand is soft or hard
                    if 11 in player_cards:  # if the hand is soft we can just value the ace as 1
                        player_cards.remove(11)
                        player_cards.append(1)
                    else:  # hard hand so bust
                        player_bust = True
                        print("PLAYER BUSTED")
                        break

            if not player_bust:  # player has not busted  --> dealers turn
                while sum(dealer_cards) < 17:
                    dealer_cards.append(self.card_deck.pop())

                    # check for bust
                    if sum(dealer_cards) > 21:
                        if 11 in dealer_cards:  # hand soft ?
                            dealer_cards.remove(11)
                            dealer_cards.append(1)
                        else:  # hard hand so player wins
                            self.player.add_capital(2 * bet)  # add bet + win to player account
                            dealer_bust = True
                            print("DEALER BUSTED")
                            break

                if not dealer_bust:
                    if sum(player_cards) > sum(dealer_cards):  # player wins
                        print("PLAYER WINS")
                        self.player.add_capital(2 * bet)
                    elif sum(player_cards) == sum(dealer_cards):  # push  --> return bet
                        print("PUSH")
                        self.player.add_capital(bet)
                    else:  # house wins
                        print("HOUSE WINS")

        # store ace values all as value 11 again
        player_cards = [card_value if card_value != 1 else 11 for card_value in player_cards]
        dealer_cards = [card_value if card_value != 1 else 11 for card_value in dealer_cards]
        self.played_cards.extend(player_cards)
        self.played_cards.extend(dealer_cards)


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
