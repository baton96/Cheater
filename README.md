# 🃏 Cheater Bot Player 🃏

This project was created during the course of "Elements of Computational Intelligence" and its goal was to implement a
strategy for a bot player, based on the given example, for the card game called "Cheater". At first this player was
tested in the game with, unknown at that moment, lecturer’s players, and then it took part in the tournament within
laboratory group in which it got the highest possible score as **this player has beaten all players provided by both
lecturer and my colleagues**.

## Rules

The rules in this project were based on the rules in card game called "Cheater". Game is played with one deck of cards
from 9 to 14 (ace) – each with 4 color variants (24 cards in total). Cards are dealt randomly to two players – 8 cards
for each player. The goal is to get rid of all your cards. Players take their turns alternately. A turn consists of
placing on the common pile one card face-down declaring which card you placed (so you may lie). Declared card must have
at least the same value as the previously declared card on the top of the common pile. Next the other player may or may
not check if you lied. If you get caught lying you have to take 3 cards from the top of the heap, if not – the player
who was checking takes 3 cards.

## [Putting](MyPlayer.py#L25) and [Checking](MyPlayer.py#L62) Strategies
* Counting how many cards are left in opponent hand  
* Sorting hand after each draw  
* Keeping record of all cards that were put on pile  
* Taking into account difference between number of cards within players  
