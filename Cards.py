"""
Creates class to hold Card abstractions
"""
import functools

class Card(object):
    values = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
    suits = ("H", "S" , "C", "D")
    suit_str_mappings = {"H": "♥", "S": "♠", "C": "♣", "D": "♦"}

    def __init__(self, value, suit):
        if not self._check_valid(value, suit):
            raise Exception("Value - {} and Suit - {} are not valid options. They must be in: {} - {} ".format(value, suit, Card.values, Card.suits))

        self._value = value
        self._suit = suit

    def _check_valid(self, value, suit):
        return value in Card.values and suit in Card.suits

    @property
    def value(self):
       return self._value

    @property
    def suit(self):
        return self._suit

    @functools.total_ordering
    def __ge__(self, other):
        """
        Returns whether a Card is >= another Card
        """
        if self.value >= other.value:
            return True
        return False

    def __str__(self):
        return str(self._value) + Card.suit_str_mappings[self._suit]

if __name__ == "__main__":
    # Testing
    c1 = Card(8, 'H')
    c2 = Card(1, 'H')
    print(c1 >= c2)