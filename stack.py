from dataclasses import dataclass
from operator import itemgetter
from typing import List, Dict

from card import Card


@dataclass
class Stack:
    content: List[List[Card]]

    def add(self, card: Card, player):
        queue: List[Card]
        queues_available: Dict[int, List[Card]] = {}
        for queue in self.content:
            last_card: Card = queue[-1]
            if last_card.number < card.number:
                queues_available[last_card.number] = queue

        if len(queues_available) == 0:
            player.select_queue(self)
            self.content.append([card])
        else:

            last_numbers = sorted(queues_available.keys(), reverse=True)
            queue_where_card_must_be_played: List[Card] = queues_available[last_numbers[0]]

            # print(f"{player.name} adds its Card on the stack with"
            #       f" the last card {queue_where_card_must_be_played[-1]}")

            queue_where_card_must_be_played.append(card)

    def get_queue_penalities(self,queue : List[Card]) -> int:
        penalities = 0
        for card in queue:
            penalities += card.penality

        return penalities

    def get_queues_ordered_by_penalities(self):
        queues = []
        for queue in self.content:
            queues.append({"penalities": self.get_queue_penalities(queue),"queue":queue})

        queues_dict_sorted =  sorted(queues, key = lambda i: i['penalities'])

        queues_sorted_by_penalities = [elmt["queue"] for elmt in queues_dict_sorted]

        return queues_sorted_by_penalities
