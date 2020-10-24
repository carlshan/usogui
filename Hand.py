"""
Class that holds a hand.
"""
import functools
from collections import Counter
from Cards import Card

class Hand(object):
    hand_rankings = {
        "Royal Straight Flush": 10,
        "Straight Flush": 9,
        "Four of a Kind": 8,
        "Full House": 7,
        "Flush": 6,
        "Straight": 5,
        "Three of a Kind": 4,
        "Two Pair": 3,
        "One Pair": 2,
        "High Card": 1
    }

    def __init__(self, cards):
        assert len(cards) == 5, "Must have exactly five cards."
        # Sorting to place Aces first when hands are converted to Aces
        # this helps with comparisons between hands of the same class later on
        self._cards = sorted(cards, key=lambda c: c.value, reverse=True)
        self._counter = Counter(self._get_values())

    @property
    def counter(self):
        return self._counter

    @property
    def best_hand(self):
        return self._get_best_hand()

    def _show_cards(self):
        to_show = [str(card) for card in self._cards]
        return to_show

    def __str__(self):
        return ', '.join(self._show_cards())

    def _get_values(self):
        return [c.value for c in self._cards]

    def _is_straight_hand(self):

        values = self._get_values()
        # Handle the case of a royal straight
        if sorted(values) == [1, 10, 11, 12, 13]: return True

        min_value = min(values)
        max_value = max(values)

        to_check = list(range(min_value, max_value + 1))

        return sorted(values) == to_check

    def _is_royal_hand(self):
        values = self._get_values()
        result = sorted(values) == [1, 10, 11, 12, 13]
        return result

    def _is_flush_hand(self):
        # all cards are the same suit
        return len(set(c.suit for c in self._cards)) == 1

    def _is_four_of_kind_hand(self):
        return self._has_N_of_same_value(4)

    def _is_full_house_hand(self):
        first_most_common_card_value = self.counter.most_common()[0][1]
        second_most_common_card_value = self.counter.most_common()[1][1]

        return first_most_common_card_value == 3 and second_most_common_card_value == 2

    def _is_three_of_kind_hand(self):
        return self._has_N_of_same_value(3)

    def _is_two_pair_hand(self):
        card_values = self._get_values()
        c = Counter(card_values)
        if len(set(card_values)) != 3:
            # Definitely not a two-pair
            return False
        else:
            counter_values = [p[1] for p in c.items()] # creating container with c.items() b/c of Counter dict_keys not being iterable
            twos = Counter(counter_values)
            return twos[2] == 2 # There are exactly two 2s

    def _is_one_pair_hand(self):
        card_values = self._get_values()
        c = Counter(card_values)
        if len(set(card_values)) > 4:
            # Definitely not a pair
            return False
        else:
            counter_values = [p[1] for p in c.items()] # creating container with c.items() b/c of Counter dict_keys not being iterable
            twos = Counter(counter_values)
            return twos[2] == 1 # There are exactly one pair

    def _has_N_of_same_value(self, N):
        values = self._get_values()
        c = Counter(values)
        return N in c.values()

    def _get_best_hand(self):
        """
            Returns the best possible type of hand that can be formed with these cards.
        """
        is_flush = self._is_flush_hand()
        is_straight = self._is_straight_hand()
        is_royal = self._is_royal_hand()
        is_four_of_kind = self._is_four_of_kind_hand()
        is_full_house = self._is_full_house_hand()
        is_three_of_kind = self._is_three_of_kind_hand()
        is_two_pair = self._is_two_pair_hand()
        is_one_pair = self._is_one_pair_hand()

        if is_flush and is_straight and is_royal:
            return "Royal Straight Flush"
        elif is_straight and is_flush:
            return "Straight Flush"
        elif is_four_of_kind:
            return "Four of a Kind"
        elif is_full_house:
            return "Full House"
        elif is_flush:
            return "Flush"
        elif is_straight:
            return "Straight"
        elif is_three_of_kind:
            return "Three of a Kind"
        elif is_two_pair:
            return "Two Pair"
        elif is_one_pair:
            return "One Pair"
        else:
            return "High Card"

    @functools.total_ordering
    def __lt__(self, other):
        return not self.__ge__(other)

    @functools.total_ordering
    def __ge__(self, other):
        """
            Poker rankings (best to worst):
                * Royal straight flush
                * Straight flush
                * Four of a kind
                * Full house
                * Flush
                * Straight
                * Three of a kind
                * Two pair
                * One pair
                * High card
        """
        h1_best_hand = self._get_best_hand()
        h2_best_hand = other._get_best_hand()
        # Checks to see if we have tie in the "class/type" of hands in which case we need to do
        # more nuanced comparisons, and also handle aces.
        # E.g., if the class is Four of a kind, then 4 aces is better than 4 twos.
        equal_class = Hand.hand_rankings[h1_best_hand] == Hand.hand_rankings[h2_best_hand]
        if equal_class:
            return self._compare_same_class(other, h1_best_hand)
        return Hand.hand_rankings[h1_best_hand] > Hand.hand_rankings[h2_best_hand]

    def _handle_aces(self):
        # converts all 1s to 14s
        # returns a new hand with 1s as 14s
        cards = []
        for c in self._cards:
            if c.value == 1:
                new_card = Card(value=14, suit=c.suit)
                cards.append(new_card)
            else:
                cards.append(c)

        return Hand(cards=cards)

    def _compare_same_class(self, other, hand_class):
        """
            Compares hands of the same class, and also handles aces
        """
        hand1 = self._handle_aces()
        hand2 = other._handle_aces()

        if hand_class == "Royal Straight Flush":
            return True # True due to equality
        elif hand_class in ("Straight Flush", "Flush", "High Card"):
            # Who has the higher max card, knowing that it's straight flush or flush.
            # If it's the same straight flush
            max1 = max(hand1._get_values())
            max2 = max(hand2._get_values())
            return max1 >= max2
        # else in all other cases ("Four of a Kind", "Full House", "Three of a Kind", "Two Pair") we compare
        # in descending frequency of cards, their respective values.
        # Note that hands are also already sorted by card value, in desc order, so this also works
        # in the case of same hand class but one has Ace listed later in the hand.
        h1_card_values = [tup[0] for tup in hand1.counter.most_common()]
        h2_card_values = [tup[0] for tup in hand2.counter.most_common()]
        # Card values are examined in desc. of most common occurrence, with ties broken by the value of the card (so Aces are put first).
        for c1, c2 in zip(h1_card_values, h2_card_values):
            if c1 != c2:
                return c1 >= c2
            else: continue
        # Otherwise all cards have the same value but different suits, return True
        return True

if __name__ == "__main__":
    cards1 = [
        Card(value=3, suit='H'),
        Card(value=3, suit='S'),
        Card(value=9, suit='H'),
        Card(value=11, suit='H'),
        Card(value=11, suit='H')
    ]
    cards2 = [
        Card(value=3, suit='H'),
        Card(value=3, suit='S'),
        Card(value=9, suit='H'),
        Card(value=1, suit='H'),
        Card(value=12, suit='H')
    ]
    h1 = Hand(cards1)
    h2 = Hand(cards2)
    print(h1, h1.best_hand)
    print(h2, h2.best_hand)
    if h1 >= h2:
        print("Hand 1 is better.")
    else:
        print("Hand 2 is better.")