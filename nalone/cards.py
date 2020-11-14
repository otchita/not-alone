"""Card classes module."""


class Card:
    """Generic class for cards."""


class HelperCard(Card):
    """Helper cards i.e. (Hunt or survival)."""


class SurvivalCard(HelperCard):
    """Survival card class for hunted players."""


class HuntCard(HelperCard):
    """Hunt card class for creature."""


class PlaceCard(Card):
    """Place card class."""

    def __init__(self):
        self.number = None

    @classmethod
    def from_int(cls, card_number: int):
        """Initilize place card from number.

        Parameters
        ----------
        card_number
            A number between 1 and 10 that corresponds to a place card.

        Returns
        -------
        PlaceCard
        """
        if not 1 <= card_number <= 10:
            raise ValueError(
                f'Place card number must be between 1 and 10 {card_number} was'
                ' given.'
            )
        place_card = cls()
        place_card.number = card_number
        return place_card


class HandPlaceCard(PlaceCard):
    """Place card class that are in player's hands."""


class MapPlaceCard(PlaceCard):
    """Place card class that are in the map."""

    def __hash__(self):
        return hash((self.number, ))

    def __eq__(self, other):
        if isinstance(other, MapPlaceCard):
            return hash(self) == hash(other)
        raise ValueError(
            'A MapPlaceCard can only be compared with another MapPlaceCard.'
        )
