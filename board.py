import pprint
import random
from dataclasses import dataclass, field
from itertools import cycle
from operator import itemgetter
from typing import List, Dict

from card import Card
from deck import Deck
from player import Player
from stack import Stack


@dataclass
class Board:
    deck: Deck
    players: List[Player] = field(default_factory=list)
    stack: Stack = Stack([[], [], [], []])

    def initialize(self):
        random.shuffle(deck.content)

        for player_registered in self.players:
            player_registered.initialize()

        pool = cycle(self.players)

        number_of_cards_to_be_distributed: int = len(self.players) * 10
        number_of_cards_to_be_distributed_in_stack: int = 4

        card: Card
        for card in deck.content:

            if number_of_cards_to_be_distributed <= 0:
                if number_of_cards_to_be_distributed_in_stack == 0:
                    break
                else:
                    self.stack.content[4 - number_of_cards_to_be_distributed_in_stack].append(card)
                    number_of_cards_to_be_distributed_in_stack -= 1

            next_player_in_ppol = next(pool)

            next_player_in_ppol.add_card(card)

            number_of_cards_to_be_distributed -= 1

    def play_round(self):

        cards_to_be_played: List[Card] = []
        cards_to_be_played_by_player: Dict[int, Player] = {}
        cards_by_number: Dict[int, Card] = {}

        for p in self.players:
            card_played = p.play(self.stack)
            cards_to_be_played.append(card_played)
            cards_to_be_played_by_player[card_played.number] = p
            cards_by_number[card_played.number] = card_played

        cards_number_to_be_played: List[int] = sorted(cards_to_be_played_by_player.keys())

        card_number: int
        for card_number in cards_number_to_be_played:
            card: Card = cards_by_number[card_number]
            player_of_the_card: Player = cards_to_be_played_by_player[card_number]

            # print(f"{player.name} will play {card}")
            self.stack.add(card, player_of_the_card)


if __name__ == "__main__":
    p1 = Player("Kévin", strategy=True)
    p2 = Player("Sabine", strategy=False)
    p3 = Player("Marine", strategy=False)
    p4 = Player("Alex", strategy=False)
    p5 = Player("Jerome", strategy=False)
    p6 = Player("Anne So", strategy=False)

    log_file = open("output/log.csv", "w")
    log_file.write(";".join(["Party Index", "Player Name", "Penality", "\n"]))

    deck = Deck()
    deck.import_from("input/CardDeckStructure.csv")

    nb_party_to_be_played = 1

    total_scores_by_player: Dict[str, int] = {}

    b = Board(deck, [p1, p2, p3, p4, p5, p6])
    for player in b.players:
        total_scores_by_player[player.name] = 0

    for index in range(nb_party_to_be_played):

        b.initialize()

        while p1.number_of_card_in_hand() != 0:
            b.play_round()

        for player in b.players:
            # print(player.name, player.count_penalities())
            player_penality: int = player.count_penalities()
            total_scores_by_player[player.name] += player_penality
            log_file.write(";".join([str(index), player.name, str(player_penality), "\n"]))

    key = itemgetter(1)
    sorted_total_scores_by_player = sorted(total_scores_by_player.items(), key=key)

    pprint.pprint(sorted_total_scores_by_player)
