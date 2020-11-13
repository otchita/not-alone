"""Unit tests for :mod:`nalone.board`."""
import pytest

from nalone.board import NumberOfPlayerError, assert_number_of_players


@pytest.mark.parametrize(
    'number_of_players', [1, 35, 10, 8]
)
def test_assert_number_of_players(number_of_players):
    """Test :func:`nalone.board.assert_number_of_players`."""
    with pytest.raises(NumberOfPlayerError):
        assert_number_of_players(number_of_players)
