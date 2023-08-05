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


def is_straight_poker(combination):
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
    if len(set(suits)) == 1:
        return PokerHand.FLUSH

    if is_straight_poker([card[0] for card in cards]):
        return PokerHand.STRAIGHT


hand_counts = {hand: 0 for hand in COMBINATIONS}


# Ouro, Copas, Espadas, Paus
# cards = [
#     ("10", "Ouro"),
#     ("9" "Paus"),
#     ("8", "Copas"),
#     ("7", "Espadas"),
#     ("6", "Ouro"),
# ]  # straight

cards = [
    ("10", "Ouro"),
    ("9", "Ouro"),
    ("8", "Ouro"),
    ("7", "Ouro"),
    ("6", "Ouro"),
]  # flush

print(simulate_hand(cards))
