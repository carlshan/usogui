from Cards import Card
from Deck import Deck
from Hand import Hand

deck = Deck()

"""
The game works the following way:
1. Each player is given 5 numbers
2. They can then choose to play the numbers however they'd like.
3. Each number will form the best possible hand with the cards that sum to that number.
4. If two players use the same card in their hands, the higher hand wins.
5. Players also cannot use a card that has already been removed from the deck.
"""

def count_hands(number, num_avail):
    memo = dict()
    def subproblem(number, num_avail):
        # TODO: Maybe add another parameter that keeps track of all the available numbers
        # and if we have used 4 of one, we can't use that number any more
        if (number, num_avail) in memo: return memo[number]
        valid = [num for num in range(1, 14) if num <= number]

        if num_avail == 0:
            return 0
        elif num_avail == 1 and number in valid:
            return 1

        if number < 1: return 0
        elif number == 1: return 1
        elif number == 2: return 2
        else:
            tot = 0
            for num in valid:
                tot += count_hands(number - num, num_avail - 1)

        memo[(number, num_avail)] = tot
        return tot

    return subproblem(number, num_avail)

print(count_hands(5, 3))

def form_hands(number, deck):
    # Given deck, create array of all hands that sum to the number
    # return the array of all hands
    # The numbers are 1 through 13, but only four of each can be chosen
    """
        If the number is <= 0: return []

    """
    hands = []
    if number <= 0: # no hands possible
        return []
    elif number == 1:
        return [[1]]
    # TODO: Update valid_options so that numbers that are too big, and won't leave room for a 5 card hand, will fail
    valid_options = [num for num in range(1, 14) if num <= number] # these are the only valid poker cards that can be used
    for num in valid_options:
        result = form_hands(number - valid_options, deck)
        hands.extend(result)
    return hands
