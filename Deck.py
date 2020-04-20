from Hand import Hand
from Cards import Card

class Deck(object):

    def __init__(self):
        """
        A deck has 52 cards
        """
        self._deck = []

        for value in range(1, 14):
            for suit in ("H", "S", "D", "C"):
                self._deck.append(Card(value=value, suit=suit))

    def find_card(self, card):
        card_value = card.value
        card_suit = card.suit

        for c in self._deck:
            if c.value == card_value and c.suit == card_suit:
                return True
        return False

    def remove_card(self, card):
        card_value = card.value
        card_suit = card.suit

        for i, c in enumerate(self._deck):
            if c.value == card_value and c.suit == card_suit:
                break
        else:
            print("Did not find {}".format(card))
            return None

        self._deck.pop(i)

    @property
    def size(self):
        return len(self._deck)
