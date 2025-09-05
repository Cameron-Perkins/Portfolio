import Player_Class
import random as rd

user = Player_Class.Player("Alice", [], 1000)
names = ['Bob', 'Charles', 'Diana', 'Eddy', 'Fiona', 'Grant', 'Hope']

# This is where the player chooses how many people to play with
choice = input('How many players do you want to play with enter a number 1-7.')

# This is where we make the players list which will store all of the information regarding our players.
players = []
for i in range(int(choice)):
    players.append(Player_Class.Computer(names[i], [], 1000))

# We make the deck

# We add the human user to our list
players.append(user)
# Make sure user is the first player.
players.reverse()

dealer_index = 0

safe_players = players

print(len(players), ' players in the game.')
# Game loop
run = True
while run:
    deck = Player_Class.make_deck()
    pot_amount = 0
    on_table = []
    print('Starting a new round.')
    # Here we deal two cards to each player.
    for computer in players:
        Player_Class.deal_table_cards(computer, 2, deck)

    for player in players:
        print(player.name)
        print(player.hand)

    players, pot_increment = Player_Class.Round_of_Betting(players, dealer_index)
    pot_amount += pot_increment

    # This is the loop that deal with each round of betting.
    for i in ['Flop', 'Turn', 'River']:
        # Dealing cards flop cards
        if i == 'Flop':
            print('Dealing flop')
            for player in players:
                Player_Class.deal_table_cards(player, 3, deck)

        # Dealing turn cards
        elif i == 'Turn':
            print('Dealing turn')
            for player in players:
                Player_Class.deal_table_cards(player, 1, deck)

        # Dealing river cards
        elif i == 'River':
            print('Dealing river')
            for player in players:
                Player_Class.deal_table_cards(player, 1, deck)

        for player in players:
            print(player.name)
            print(player.hand)
        
        players, pot_increment = Player_Class.Round_of_Betting(players, dealer_index)
        pot_amount += pot_increment

        # If all but one player has folded, we will break the loop.
        if sum(1 for p in players if p.previous_move != 'fold') <= 1:
            break

    players = [p for p in players if p.previous_move != 'fold']


    if len(players) == 1:
        players[0].chips += pot_amount
        pot_amount = 0
    else:
        Player_Class.determine_winner(players, pot_amount)


    for player in players:
        print(player.hand)

    # Reset
    for player in players:
        player.reset()

    # This is to remove all players who have no chips and can no longer play.
    i = 0
    while i < len(players):
        if players[i].chips <= 0:
            players.pop(i)
            continue
        i+=1


    if len(players) == 1:
        print(players[0].name + ' wins. Congradulations.') 
        run = False
    players = safe_players
print('End of game')