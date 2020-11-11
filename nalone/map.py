"""Map module."""
from typing import Dict, Iterable, List, Optional
from copy import deepcopy

from nalone.cards import MapPlaceCard


class ArtemiaMapSetUpError(ValueError):
    """Exception raised when the game's map is not properly set up.

    Parameters
    ----------
    message
        An optional message.
    """

    def __init__(self, message: Optional[str] = None):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        """Pretty print error message."""
        res = 'Game map cannot be properly set up'
        if self.message:
            res += self.message
        return res


class ArtemiaMap:
    """The Artemia map class."""

    def __init__(self):
        self._graph = None
        self._cards = None

    @classmethod
    def from_place_cards(cls, cards: List[MapPlaceCard]) -> 'ArtemiaMap':
        """Initialize map class from ordered map place cards."""
        # pylint: disable=protected-access
        cards_len = len(cards)
        if cards_len != 10:
            raise ArtemiaMapSetUpError(
                f': Fed Place cards must be exactly 10. {cards_len} was were '
                'given.'
            )

        map_ = cls()
        graph: Dict[int, List[int]] = dict()
        for i in range(10):
            vertical_neighbor = i + 5 if i < 5 else i - 5
            if i in (0, 5):
                horizontal_neighbors = [i + 1]
            elif i in (4, 9):
                horizontal_neighbors = [i - 1]
            else:
                horizontal_neighbors = [i - 1, i + 1]
            graph.setdefault(i, []).extend(
                [*horizontal_neighbors, vertical_neighbor]
            )

        map_._graph = graph
        map_._cards = deepcopy(cards)
        return map_

    def _get_card_index(self, id_: int) -> int:
        """Get map place card index by id."""
        for i, card in enumerate(self._cards):
            if card.number == id_:
                return i
        raise ValueError(f'No card corresponding to the given id {id_}.')

    def get_card(self, id_: int) -> MapPlaceCard:
        """Get map place card by id.

        Parameters
        ----------
        id_
            The identifier of the map place card.

        Returns
        -------
        MapPlaceCard
            The corresponding map place card.
        """
        return self._cards[self._get_card_index(id_)]

    def get_neighbors_by_id(self, id_: int) -> Iterable[MapPlaceCard]:
        """Get neighbors of a map place card by its id.

        Parameters
        ----------
        id_
            The identifier of the map place card.

        Returns
        -------
        Iterbale[MapPlaceCard]
            A interable containing the neighboring map place cards.
        """
        if not 1 <= id_ <= 10:
            raise ValueError(
                f'map place id must be between 1 and 10. {id} was given.'
            )
        card_index = self._get_card_index(id_)
        return map(lambda x: self._cards[x], self._graph[card_index])

    def get_neighbors(
            self,
            map_place_card: MapPlaceCard
    ) -> Iterable[MapPlaceCard]:
        """Get neighbors of a map place card.

        Parameters
        ----------
        map_place_card
            The map place card in question.

        Returns
        -------
        Iterbale[MapPlaceCard]
            A interable containing the neighboring map place cards.
        """
        return self.get_neighbors_by_id(map_place_card.number)
