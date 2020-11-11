"""Unit tests for :mod:`nalone.map`."""
import pytest

from nalone.map import ArtemiaMap, ArtemiaMapSetUpError
from nalone.cards import MapPlaceCard


@pytest.fixture(scope='module')
def ordered_map_place_cards():
    """Create fixture for map cards."""
    return [MapPlaceCard.from_int(i) for i in range(1, 11)]


@pytest.fixture(scope='module')
def unordered_map_place_cards():
    """Create fixture for map cards."""
    return [MapPlaceCard.from_int(i) for i in (1, 2, 3, 4, 5, 7, 9, 10, 6, 8)]


def test_map_from_place_cards_wrong_input():
    """Test wrong input for :meth:`nalone.map.Map.from_place_cards`."""
    with pytest.raises(ArtemiaMapSetUpError):
        _ = ArtemiaMap.from_place_cards(
            [MapPlaceCard.from_int(i) for i in range(1, 4)]
        )


@pytest.mark.parametrize(
    'ordered, card_index, neighbors_indexes',
    [
        (True, 1, [2, 6]),
        (True, 2, [1, 3, 7]),
        (True, 5, [4, 10]),
        (True, 9, [8, 10, 4]),
        (False, 1, [2, 7]),
        (False, 2, [1, 3, 9]),
        (False, 4, [3, 5, 6]),
        (False, 7, [1, 9]),
        (False, 10, [9, 6, 3]),
        (False, 8, [6, 5]),
    ]
)
def test_map_from_place_cards(
        ordered_map_place_cards,
        unordered_map_place_cards,
        ordered,
        card_index,
        neighbors_indexes
):
    """Test :meth:`nalone.map.Map.from_place_cards`."""
    if ordered:
        map_ = ArtemiaMap.from_place_cards(ordered_map_place_cards)
    else:
        map_ = ArtemiaMap.from_place_cards(unordered_map_place_cards)
    card = MapPlaceCard.from_int(card_index)
    expected_neighbors = set(map(MapPlaceCard.from_int, neighbors_indexes))
    assert isinstance(map_, ArtemiaMap)
    neighbors = set(map_.get_neighbors(card))
    assert neighbors == expected_neighbors
    assert True
