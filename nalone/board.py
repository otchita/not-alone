"""Board module."""
import abc
from typing import Optional, Tuple, Union
from enum import Enum


class NumberOfPlayerError(ValueError):
    """Exception raised when the number of given players is invalid.

    Parameters
    ----------
    number_of_players
        The number of players given
    message
        An optional message.
    """

    def __init__(self, number_of_players: int, message: Optional[str] = None):
        self.number_of_players = number_of_players
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        """Pretty print error message."""
        res = f'Illegal number of players {self.number_of_players}'
        if self.message:
            res += self.message
        return res


def assert_number_of_players(number_of_players: int):
    """Check if the number of valid players is legal.

    Parameters
    ----------
    number_of_players
        The number of players given.
    """
    if not 2 <= number_of_players <= 7:
        raise NumberOfPlayerError(number_of_players)


class PositionError(ValueError):
    """Exception raised when the position id is invalid.

    Parameters
    ----------
    position_id
        The position identifier.
    limits
        The limits of the track.
    message
        An optional message.
    """

    def __init__(
            self,
            position_id: int,
            limits: Tuple[int, int],
            message: Optional[str] = None
    ):
        self.position_id = position_id
        self.limits = limits
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        """Pretty print error message."""
        res = (f'Invalid position id {self.position_id}.  Should be contained'
               f' within {self.limits}')
        if self.message:
            res += self.message
        return res


class Position(metaclass=abc.ABCMeta):
    """A position on the board."""

    @property
    @abc.abstractmethod
    def _limits(self) -> Tuple[int, int]:
        """Get the limits of the track."""
        raise NotImplementedError

    def __init__(self, value: int):
        if not self._limits[0] <= value <= self._limits[1]:
            raise PositionError(value, self._limits)

        self.value = value
        self.next = None
        self.previous = None


class AssimilationPosition(Position):
    """An assimilation position on the board."""

    @property
    def _limits(self) -> Tuple[int, int]:
        """Get the limits of the assimilation track."""
        return (0, 11)


class RescuePositionType(Enum):
    """Enumerator of rescue position types."""

    REGULAR = 0
    ARTEMIA = 1


class RescuePosition(Position):
    """A rescue position on the board."""

    @property
    def _limits(self) -> Tuple[int, int]:
        """Get the limits of the rescue track."""
        return (0, 17)

    def __init__(
            self,
            value: int,
            type_: Union[int, RescuePositionType] = RescuePositionType.REGULAR
    ):
        super().__init__(value)
        self.type = RescuePositionType(type_)


class Track(metaclass=abc.ABCMeta):
    """The track of a team on the game board."""

    def __init__(self):
        self.head = None

    @abc.abstractmethod
    def append_by_id(
            self,
            position_id: int,
            rescue_position_type: Optional[RescuePositionType] = None
    ):
        """Append a position into a track by id.

        Parameters
        ----------
        position_id
            The position identifier to be apended to the track.
        rescue_position_type
            The rescue position type in the case of rescue track.
        """

    def append(self, position: Position):
        """Append a position into a track.

        Parameters
        ----------
        position
            The position to be apended to the track.
        """
        if self.head is None:
            self.head = position
        else:
            pointer = self.head
            while pointer.next is not None:
                pointer = pointer.next
            position.previous = pointer
            pointer.next = position

    def get_position(self, id_: int) -> Position:
        """Get a position given its identifier."""
        pointer = self.head
        while pointer.next is not None:
            if pointer.value == id_:
                return pointer
            pointer = pointer.next
        raise ValueError(f'No position found for the given id: {id_}')


class AssimilationTrack(Track):
    """The assimilation track of the game board."""

    def append_by_id(self, position_id: int, rescue_position_type=None):
        """Append an assimilation position into its track by id."""
        position = AssimilationPosition(position_id)
        super().append(position)


class RescueTrack(Track):
    """The assimilation track of the game board."""

    def append_by_id(
            self,
            position_id: int,
            rescue_position_type=RescuePositionType.REGULAR
    ):
        """Append a rescue position into its track by id."""
        position = RescuePosition(position_id, rescue_position_type)
        super().append(position)


class BoardType(Enum):
    """Enumerator of board type.

    - ``STACKED`` refers to the board where the Artemia spots are stacked
    atthe end of the rescue alley.

    - ``ALTERNATING`` refers to the board where the Artemia spots are
    alternating with normal spots.
    """

    STACKED = 1
    ALTERNATING = 2


class Board:
    """Board class object.

    Attributes
    ----------
    number_of_players
        The number of players in the game.
    type
        The board type.
    """

    def __init__(
            self,
            number_of_players: int,
            type_: Union[BoardType, int] = BoardType.STACKED
    ):
        assert_number_of_players(number_of_players)
        self.number_of_players = number_of_players
        self.type = BoardType(type_)
