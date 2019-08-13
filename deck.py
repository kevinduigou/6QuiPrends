from card import Card


class Deck:
    def __init__(self):
        self.content = []

    def import_from(self, path: str):
        with open(path, "r") as f:
            line_nb = 0
            for line in f.readlines():
                if line_nb == 0:
                    line_nb += 1
                else:
                    number, penality = line.split(";")
                    
                    number = int(number)
                    penality = int(penality)

                    c = Card(number, penality)
                    self.content.append(c)
                    line_nb += 1

    def display(self):

        card: Card
        for card in self.content:
            print(card)


if __name__ == "__main__":
    monDeck = Deck()

    monDeck.import_from("input/CardDeckStructure.csv")

    monDeck.display()
