"""Card classes module."""
from typing import Iterable, List, Optional, Union
import random


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


class InsuffisantCardsInPackError(ValueError):
    """Exception raised when a drawing operation is performed on an empty pack.

    Parameters
    ----------
    message
        An optional message.
    """

    def __init__(
            self,
            pack_cards: int,
            draws: int,
            message: Optional[str] = None
    ):
        self.pack_cards = pack_cards
        self.draws = draws
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        """Pretty print error message."""
        res = (
            f'Insuffisant number of cards in pack: Cannot draw {self.draws} '
            f'card(s) for pack conytaining {self.pack_cards} cards.'
        )
        if self.message:
            res += self.message
        return res


class Pack:
    """Pack of cards class."""

    def __init__(self):
        self._cards = list()

    def __len__(self):
        return len(self._cards)

    def shuffle(self):
        """Shuffle the pack of cards."""
        random.shuffle(self._cards)

    def draw(self, number: int = 1) -> Union[Card, List[Card]]:
        """Draw cards from the pack.

        Parameters
        ----------
        number
            The number of cards to be drawn.

        Returns
        -------
        Union[Card, List[Card]]
            The card or cards drawn from the pack.
        """
        drawn_cards: List[Card] = []
        if len(self) < number:
            raise InsuffisantCardsInPackError(len(self), number)

        while number > 0:
            drawn_cards.append(self._cards.pop(0))
            number -= 1

        if len(drawn_cards) == 1:
            return drawn_cards[0]
        return drawn_cards

    def append(
            self,
            card: Card,
            where: str = 'bottom',
            shuffle: bool = False
    ):
        """Append a card to the pack.

        Parameters
        ----------
        card
            The card to be added to the pack.
        where
            Where will the card be inserted. Either 'top' or 'bottom'.
        shuffle
            ``True`` if the pack is to be shuffled after card insertion.
            ``False`` otherwise.
        """
        if where not in ('top', 'bottom'):
            raise ValueError(
                f'Unknown card insertion position {where}. Please provide '
                f'either `top` or `bottom`.'
            )

        if where == 'bottom':
            self._cards.append(card)
        else:
            self._cards.insert(0, card)

        if shuffle:
            self.shuffle()

    def extend(
            self,
            cards: Iterable[Card],
            where: str = 'bottom',
            shuffle: bool = False
    ):
        """Extend the pack with multiple cards.

        Parameters
        ----------
        cards
            The cards to be added to the pack.
        where
            Where will the card be inserted. Either 'top' or 'bottom'.
        shuffle
            ``True`` if the pack is to be shuffled after card insertion.
            ``False`` otherwise.
        """
        if where not in ('top', 'bottom'):
            raise ValueError(
                f'Unknown card insertion position {where}. Please provide '
                f'either `top` or `bottom`.'
            )

        if where == 'bottom':
            self._cards.extend(cards)
        else:
            self._cards = list(cards) + self._cards

        if shuffle:
            self.shuffle()

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError('Can only add pack with same type.')

        pack = self.__class__()
        pack._cards = [*self._cards, *other._cards]
        return pack

    def __iadd__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError('Can only add pack with same type.')

        self.extend(other._cards)
        return self


class ActivePack(Pack):
    """A pack of active cards i.e. those that haven't been discarded."""

    @classmethod
    def from_cards(
            cls,
            cards: Iterable[Card],
            shuffle: bool = True
    ) -> 'ActivePack':
        """Create an active pack instance from cards.

        Parameters
        ----------
        cards
            An iterable containing the cards from which the pack is to be
            created.
        shuffle
            ``True`` if the cards are to be shuffled. ``False`` otherwise.

        Returns
        -------
        ActivePack
            The created active pack instance.
        """
        # pylint: disable=protected-access
        pack = cls()
        pack._cards = list(cards)
        if shuffle:
            pack.shuffle()
        return pack


class DiscardPack(Pack):
    """A pack of discarded cards."""
