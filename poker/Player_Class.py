from collections import Counter
# This is the class that stores the information about the players.

class User():
    def __init__(self, name, hand, chips=1000, previous_move=None, amount_bet=0):
        self.name = name
        self.hand = hand
        self.chips = chips
        self.previous_move = previous_move
        self.amount_bet = amount_bet

    def display_hand(self):
        print(self.name + "'s hand is: " + str(self.hand))

    def reset(self):
        self.hand = []
        self.previous_move = None
        self.amount_bet = 0

    # This is the function to call when folding.
    # Input is the amount needed to make a call and the amount currently in the pot.
    # OUTPUT: fold which is the kind of move the new amount in the pot, and the new amount to call
    def fold(self, call_amount, pot_amount):
        print(self.name + ' folded.')
        # Set's the previous move to fold so the computer knows to skip it.
        self.previous_move = 'fold'
        # We return 0 to indicate a fold, we return the unchanged pot amount and amount bet
        return 'fold', pot_amount, call_amount

    def check_or_call(self, call_amount, pot_amount):
        print(self.name + ' checked or called')
        bet = max(0, call_amount - self.amount_bet)
        pot_amount += bet
        self.amount_bet += bet
        self.chips -= bet
        print('The amount in the pot is now ' + str(pot_amount) + ' the amount bet was ' + str(bet))
        return 'check_or_call', pot_amount, call_amount

    # This is the function to call when raising.
    # Takes input of the amount we want to increase by,
    # the amount needed to make a call,
    # and the amount currently in the pot.
    # Returns the type of move the player made in this case 'raise'
    # the current amount in the pot
    # and the new call amount
    def raise_bet(self, bet, call_amount, pot_amount):
        to_call = max(0, call_amount - self.amount_bet)
        total_bet = min(self.chips, to_call + bet)  # never more than chips

        self.chips -= total_bet
        self.amount_bet += total_bet
        pot_amount += total_bet
        call_amount = self.amount_bet

        return 'raise', pot_amount, call_amount

    def evaluate_hand(self, hand):
        ranks = sorted([card[:len(card)-1] for card in hand], reverse=True)
        suits = [card[len(card)-1] for card in hand]
        rank_counts = Counter(ranks)
        suits_counts = Counter(suits)
        # We want to see if there is a flush.
        # We can do this by checking if all suits are the same.

        # Convert ranks into numbers
        for i in range(len(ranks)):
            if ranks[i] == '10':
                ranks[i] = 10
            elif ranks[i] == 'J':
                ranks[i] = 11
            elif ranks[i] == 'Q':
                ranks[i] = 12
            elif ranks[i] == 'K':
                ranks[i] = 13
            elif ranks[i] == 'A':
                ranks[i] = 14
            else:
                ranks[i] = int(ranks[i])


        ranks.sort(reverse=True)

        is_flush = False
        is_straight = False
        is_flush = len(set(suits)) == 1
        print(set(suits))
        # We do this by checking if the ranks is in order.
        is_straight = ranks == list(range(int(ranks[0]), int(ranks[0])-5, -1))

        if not is_straight:
            if ranks == [14,5,4,3,2]:
                is_straight = True

        print('is flush ', is_flush)
        print('test ', list(range(ranks[0], ranks[0]-5, -1)))

        # Check if straight flush
        if is_flush and is_straight:
            return (9, max(ranks))
        
        # Check if four of a kind.
        rank_set = set(ranks)
        for i in rank_set:
            if ranks.count(i) == 4:
                return (8, max(ranks))
            
        # Check if full house
        has_triple = False
        has_pair   = False
        for i in rank_counts.values():
            if i == 3:
                has_triple = True
            elif i == 2:
                has_pair = True
        if has_pair and has_triple:
            return (7, max(ranks))
        
        # Check if flush.
        # A flush is when all cards have the same suit.
        if len(set(suits)) == 1:
            return(6, max(ranks))
        
        # Check if straight
        # A straight is when we have 5 cards in a row.
        if is_straight:
            return (5, max(ranks))

        # Check if three of a kind.
        # Three of a kind is when we have three cards with the same number.
        for i in ranks:
            if ranks.count(i) >= 3:
                return (4, max(ranks))

        # Check if two pair.
        # Two pair is when we have two sets of cards with the same numerical value.
        one_pair = False
        for i in set(ranks):
            if ranks.count(i) == 2 and one_pair == True:
                return (3, max(ranks))
            elif ranks.count(i) == 2:
                one_pair = True

        # Check if we have two cards with the same value.
        # Check if one pair.
        if one_pair == True:
            return (2, max(ranks))
        
        # This is the option if nothing else happens.
        return (1, max(ranks))
    

class Computer(User):
    def __init__(self, name, hand, chips=1000, previous_move=None, amount_bet=0):
        super().__init__(name, hand, chips, previous_move, amount_bet)
    # This is the function that will decide what move shouls be made.
    # This function takes in amount in the pot.
    def make_move(self, pot_amount=0, call_amount=0):
        import random as rd
        moves = ['fold', 'check', 'raise']

        choice = rd.choice(moves)
        print('Amount of money before player ' + self.name + ' made a bet is ' + str(pot_amount))
        if choice == 'fold':
            return self.fold(call_amount, pot_amount)
        elif choice == 'check':
            return self.check_or_call(call_amount, pot_amount)
        elif choice == 'raise':
            to_call = max(0 ,call_amount - self.amount_bet)
            max_raise = self.chips - to_call
            print(self.name + ' raised.')
            if max_raise <= 0:
                return self.check_or_call(call_amount, pot_amount)
            bet = rd.randint(1, max_raise)
            return self.raise_bet(bet, call_amount, pot_amount)
        else:
            print('Invalid input entered. You entered ', choice, ' default to fold.')
            return self.fold(pot_amount, call_amount)
    
    


class Player(User):
    def __init__(self, name, hand, chips=1000, previous_move=None, amount_bet=0):
        super().__init__(name, hand, chips, previous_move, amount_bet)


    # This is the function that will decide what move should be made.
    # This function takes in amount in the pot.
    def make_move(self, pot_amount=0, call_amount=0):
        print('Amount of chips ' + self.name + ' has is ' + str(self.chips))
        choice = input('Enter your move: 0 to fold, 1 to check, 2 to raise.\n')
        # This is the case where the player folds.
        if choice == '0':
            return self.fold(pot_amount, call_amount)
        
        # This is the case where the player checks.
        elif choice == '1':
            return self.check_or_call(call_amount, pot_amount)
        
        # This is the case where the player raises.
        elif choice == '2':
            print("Input the amount that you want to bet.\n")
            bet = int(input())
            bet = max(0 , bet)
            return self.raise_bet(bet, call_amount, pot_amount)
        else:
            print('Invalid input entered. You entered ', choice, ' default to fold.')
            return 0, pot_amount, call_amount
        
    def display_hand(self):
        print(self.name + "'s hand is: " + str(self.hand))


def make_deck():
    import random as rd
    # Spades hearts dimonds clubs
    suits = ['\u2660', '\u2665', '\u2666', '\u2663']
    deck = []

    # Creating the cards with numbers
    for num in range(2,11):
        for suit in suits:
            deck.append(str(num) + suit)
    
    faces = ['J', 'Q', 'K', 'A']
    for face in faces:
        for suit in suits:
            deck.append(face + suit)

    rd.shuffle(deck)

    return deck

# In the event where a round of betting ends is handled here.
# We pass the players list and i which is the index.
def deal_with_win(players, i, pot_amount):
    players[i].check += pot_amount
    for player in players:
        player.amount_bet = 0


# This function takes in a list of class playres.
# Takes in the amount of money in the pot.
# The dealer index is used to keep track in which part of the loop we start
# this is used to handle the fact the dealer changes each round.

# We have removed cashed out players so now we need to remove players in this loop.
def Round_of_Betting(players, pot_amount,dealer_index=0):
    # This is a loop that all allows each player to make thier choice
    i=0
    call_amount = 0
    while i < len(players):

        player = players[i]

        # This removes a player from the list if they have folded, else we increment by 1.
        if player.previous_move == 'fold':
            pass

        # If we come back to a player that raised last we break the loop
        if player.previous_move == 'raise':
            break
        
        if player.previous_move != 'fold':
            player.previous_move, pot_amount, call_amount = player.make_move(pot_amount, call_amount)

        # This make it so all players other then the current player have previous move none.
        if player.previous_move == 'raise':
            for j in range(len(players)):
                if j == i:
                    pass
                else:
                    if player.previous_move == 'fold':
                        pass
                    else:
                        players[j].previous_move = None



        # If all but one players have folded.            
        if len(players) <= 1:
            break

        # We now deal with the call.

        i = (i+1)%len(players)

        if player.chips <= 0:
            player.previous_move = 'fold'

    return players, pot_amount

# I need a function that determines the winner then gives the pot to the player with the strongest card.
# It must be able to deal with ties and side bets.
# A side bet occurs when the player has money in but is unable to bet more.
# This function also asigns money to the winning player.
def determine_winner(players, pot_amount):
    # Create list of tuples with the name of the player and thier evaluated hand.    
    print('pot amount in determine winnners is ' + str(pot_amount))
    evaluated_hands = []
    for player in players:
        hand_value = player.evaluate_hand(player.hand)
        evaluated_hands.append((player.name, hand_value))


    max_tuple = max(hand for name, hand in evaluated_hands)
    winners = [name for name, hand in evaluated_hands if hand == max_tuple]

    num_winners = len(winners)
    share = pot_amount // num_winners
    remainder = pot_amount % num_winners

    for player in players:
        if player.name in winners:
            player.chips += share

    if remainder > 0:
        players[0].chips += remainder

    for player in players:
        print(f"Player {player.name} has {player.chips} chips after the round.")
    
# This function takes as input a player, the amount of cards that will be dealt from the deck, and the deck.
# This function is used to add cards from the deck to the players hand.
def deal_table_cards(player, amount_to_deal, deck):
    on_table = []
    for i in range(amount_to_deal):
        on_table.append(deck.pop())
    player.hand.extend(on_table)
