# Usogui
Created by Carl Shan

## Description
In the manga *Usogui*, the main character does battle with enemies through a series of gambles and bets.

In one of the final climactic battles, he plays a variation of poker where the loser will die. In this variation, rather than playing typical five-card hands, players use metal cards engraved with a number (e.g., `47`) that **represents** a poker hand.

Specifically, it represents a poker hand that can be made with any five cards remaining in the deck that sum to that number.

`47`, for example, can be made into the strongest poker hand availabale: a *Royal Straight Flush*.

Specifically, using the cards `King (=13), Queen (=12), Jack (=11), 10` and `Ace (=1)`.

In addition, players need to keep track of which cards are used in previous rounds and cannot try to form a hand using cards already used in previous rounds.

For example, if the smallest possible card `6` was played, the only hand it would represent is `Ace, Ace, Ace, Ace, 2`. At the conclusion of this round, all `Ace` cards are gone from the deck.

If a player tried to play `47` next, expecting to form a *Royal Straight Flush*, they would be unable to.

However in the manga, the protagonist and antagonist do not get to choose which hand is created after they play their cards. Rather, unbeknownst to them, a key ally of each of their's will be the ones who pick the poker hands.

### The Code

The program will simulate playing this variation of poker, to help readers of the manga *Usogui* following along during this final climactic battle and understand why certain rounds of the poker gamble resulted the way it did.