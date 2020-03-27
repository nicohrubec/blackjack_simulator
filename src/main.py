from src.game import Game, Player

p = Player(1000)
g = Game(1, p, 100, .5)
g.play_game()
print(p.capital)
