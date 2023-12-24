# Monte Carlo Blackjack Simulator

## what it does
Simulates outcomes of Blackjack games for user given settings and visualises the results in a dash application.
The application will first ask you to enter some settings for the simulation. (number of games, number of rounds to play, number of card decks, deck penetration, player type) The games are then simulated and stored in a dataframe in the results folder. You can then access the data visualisations via your local host.

## sample plots

![Mean Capital Card Counter Plot](https://github.com/nicohrubec/blackjack_simulator/blob/master/sample_plots/mean_capital_card_counter.PNG)

The first snippet compares the on average remaining capital for a card counter with an initial capital of 5000 after n rounds for different number of decks and deck penetrations. The results are averaged over 1000 game outcomes. You can see how much the results you get when counting cards depend on how many decks are used and how often the deck is shuffled. Also you can see the sharp increase in profits towards the end of the deck and how they flatten out again after the deck was shuffled.

![Run Results Card Card Counter Plot](https://github.com/nicohrubec/blackjack_simulator/blob/master/sample_plots/run_results_card_counter.PNG)

The second snippet shows a sample of the individual game results, hence capturing the variation you will face when deploying such a strategy.

## how to use it
1. Clone the repository.
2. Install dependencies. You will need: pandas (+ xldr), numpy and dash
3. Run main. This will run the simulation if you correctly input the settings as well as startup the dash application.
4. Access visualisations via local host.

## ideas to improve
- neater user interface
- improve visualisation (e.g. multidimensional analysis of outcomes with 3D plots)
