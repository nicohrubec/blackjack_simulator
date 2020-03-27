from src.simulation import Simulator

s = Simulator(n_games=100, n_rounds=100, num_decks=6, deck_penetration=.5, player_type='basic', player_capital=1000)
results = s.simulate()
