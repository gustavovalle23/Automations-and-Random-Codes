from enum import Enum, auto

COMBINATIONS = [
    "High Card",
    "One Pair",
    "Two Pair",
    "Three of a Kind",
    "Straight",
    "Flush",
    "Full House",
    "Four of a Kind",
    "Straight Flush",
    "Royal Flush",
]


class PokerHand(Enum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    STRAIGHT = auto()
    FLUSH = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    STRAIGHT_FLUSH = auto()
    ROYAL_FLUSH = auto()


values = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


def is_straight_poker(combination):
    sorted_combination = sorted(combination, key=lambda x: values[x])

    for i in range(len(sorted_combination) - 1):
        current_value = values[sorted_combination[i]]
        next_value = values[sorted_combination[i + 1]]

        if current_value + 1 != next_value:
            return False

    return True


def simulate_hand(cards):
    card_values = [card[0] for card in cards]
    value_counts = {value: card_values.count(value) for value in card_values}

    if 2 in value_counts.values():
        if 3 in value_counts.values():
            return PokerHand.FULL_HOUSE
        return PokerHand.ONE_PAIR
    elif 3 in value_counts.values():
        return PokerHand.THREE_OF_A_KIND
    elif 4 in value_counts.values():
        return PokerHand.FOUR_OF_A_KIND

    suits = [card[1] for card in cards]

    is_straight = is_straight_poker([card[0] for card in cards])
    is_flush = len(set(suits)) == 1

    if is_straight and is_flush:
        if sorted([card[0] for card in cards], key=lambda x: values[x]) == [
            "10",
            "J",
            "Q",
            "K",
            "A",
        ]:
            return PokerHand.ROYAL_FLUSH
        return PokerHand.STRAIGHT_FLUSH

    if is_flush:
        return PokerHand.FLUSH

    if is_straight:
        return PokerHand.STRAIGHT

    return PokerHand.HIGH_CARD


# Ouro, Copas, Espadas, Paus
cards = [
    ("10", "Ouro"),
    ("9" "Paus"),
    ("8", "Copas"),
    ("7", "Espadas"),
    ("6", "Ouro"),
]  # straight

cards = [
    ("10", "Ouro"),
    ("9", "Ouro"),
    ("7", "Ouro"),
    ("6", "Ouro"),
    ("3", "Ouro"),
]  # flush

cards = [
    ("10", "Ouro"),
    ("9", "Ouro"),
    ("8", "Ouro"),
    ("7", "Ouro"),
    ("6", "Ouro"),
]  # straight flush


cards = [
    ("A", "Ouro"),
    ("K", "Ouro"),
    ("Q", "Ouro"),
    ("J", "Ouro"),
    ("10", "Ouro"),
]  # royal flush

print(simulate_hand(cards))
