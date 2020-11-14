"""Unit tests for :mod:`nalone.board`."""
import pytest

from nalone.board import (AssimilationPosition, AssimilationTrack, Board,
                          BoardType, NumberOfPlayersError, PositionError,
                          RescuePosition, RescuePositionType, RescueTrack,
                          assert_number_of_players)


@pytest.mark.parametrize(
    'number_of_players', [1, 35, 10, 8]
)
def test_assert_number_of_players(number_of_players):
    """Test :func:`nalone.board.assert_number_of_players`."""
    with pytest.raises(NumberOfPlayersError):
        assert_number_of_players(number_of_players)


@pytest.mark.parametrize(
    'rescue_position_id, assimilation_position_id',
    [
        (-1, 13),
        (18, 28),
        (120, 17),
        (21, -2)
    ]
)
def test_position_error(rescue_position_id, assimilation_position_id):
    """Test initializing position with faulty id."""
    with pytest.raises(PositionError):
        _ = RescuePosition(rescue_position_id)

    with pytest.raises(PositionError):
        _ = AssimilationPosition(assimilation_position_id)


def test_position_equality():
    """Test position equality."""
    pos1 = AssimilationPosition(0)
    pos2 = AssimilationPosition(10)
    pos3 = RescuePosition(0)
    pos4 = RescuePosition(0)
    pos5 = RescuePosition(0, RescuePositionType.ARTEMIA)
    pos6 = RescuePosition(3, RescuePositionType.ARTEMIA)
    pos6.next = pos3
    pos7 = RescuePosition(3, RescuePositionType.ARTEMIA)
    pos7.next = pos4
    pos8 = RescuePosition(3, RescuePositionType.ARTEMIA)
    pos8.next = pos5

    assert pos1 != pos3
    assert pos3 == pos4
    assert pos1 != pos2
    assert pos3 != pos5
    assert pos6 == pos7
    assert pos6 != pos8


@pytest.mark.parametrize(
    'number_of_players',
    [2, 3, 4, 5, 6, 7]
)
def test_track_construction_stacked_board(number_of_players):
    """Test track construction for stacked board."""
    board_type = BoardType.STACKED
    track1 = RescueTrack.construct(number_of_players, board_type)
    expected1 = RescueTrack()
    expected1.number_of_players = number_of_players
    expected1.board_type = board_type
    for i in range(11 + number_of_players):
        if i < 5 + number_of_players:
            expected1.append_by_id(i, RescuePositionType.REGULAR)
        else:
            expected1.append_by_id(i, RescuePositionType.ARTEMIA)

    assert track1 == expected1

    track2 = AssimilationTrack.construct(number_of_players, board_type)
    expected2 = AssimilationTrack()
    expected2.number_of_players = number_of_players
    expected2.board_type = board_type
    for i in range(5 + number_of_players):
        expected2.append_by_id(i)

    assert track2 == expected2


@pytest.mark.parametrize(
    'number_of_players',
    [2, 3, 4, 5, 6, 7]
)
def test_track_construction_alternating_board(number_of_players):
    """Test track construction for alternating board."""
    board_type = BoardType.ALTERNATING
    track = RescueTrack.construct(number_of_players, board_type)
    expected = RescueTrack()
    expected.number_of_players = number_of_players
    expected.board_type = board_type
    for i in range(11 + number_of_players):
        if i < number_of_players - 1:
            expected.append_by_id(i, RescuePositionType.REGULAR)
        elif (i + number_of_players) % 2 == 0:
            expected.append_by_id(i, RescuePositionType.ARTEMIA)
        else:
            expected.append_by_id(i, RescuePositionType.REGULAR)
    assert track == expected


def test_board_initialization():
    """Test :class:`nalone.board.Board`."""
    number_of_players = 4
    board_type = BoardType.STACKED
    board = Board(number_of_players, board_type)

    assert isinstance(board, Board)
    assert board.number_of_players == number_of_players
    assert board.type == board_type
    assert board.assimilation_track_length == 9
    assert board.rescue_track_length == 15
