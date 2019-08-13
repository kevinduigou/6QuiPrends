import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional

from card import Card
from stack import Stack


@dataclass
class Player:
    name: str
    strategy: bool = False
    cards: List[Card] = field(default_factory=list)

    penalities: List[Card] = field(default_factory=list)

    def add_card(self, card: Card):
        if len(self.cards) < 10:
            self.cards.append(card)

    def number_of_card_in_hand(self):
        return len(self.cards)

    def play(self, stack: Stack = None) -> Optional[Card]:
        card_selected_by_player: Optional[Card] = None

        if not self.strategy:
            card_selected_by_player = self.cards.pop(random.randint(0, len(self.cards) - 1))
        else:
            card_numbers = sorted([card.number for card in self.cards])
            stack_numbers = sorted([queue[-1].number for queue in stack.content])

            card_dict_index: Dict[int, int] = {}
            index = 0
            for card in self.cards:
                card_dict_index[card.number] = index
                index +=1

            card_to_select_index = card_dict_index[card_numbers[-1]]
            card_selected_by_player = self.cards.pop(card_to_select_index)

            queues_ordered_by_penalities : List[List[Card]] = stack.get_queues_ordered_by_penalities()
            queues_ordered_by_penalities[0]

            #print(card_selected_by_player)
            #print("#######")
        return card_selected_by_player

    def count_penalities(self):
        penalities = 0
        for card in self.penalities:
            penalities += card.penality

        return penalities

    def select_queue(self, stack):
        penality_by_queue: Dict[int, List[Card]] = {}
        for queue in stack.content:
            penalities = 0
            for card in queue:
                penalities += card.penality

            penality_by_queue[penalities] = queue

        penalities_sorted = sorted(penality_by_queue.keys())
        queue_with_lowest_penalities: List[Card] = penality_by_queue[penalities_sorted[0]]

        for card in queue_with_lowest_penalities:
            self.penalities.append(card)

        # print(f"{self.name} takes the queue ({queue_with_lowest_penalities}) and drop its card")
        stack.content.remove(queue_with_lowest_penalities)

    def initialize(self):
        self.penalities = []
        self.cards = []
