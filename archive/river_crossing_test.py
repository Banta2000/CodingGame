from river_crossing import flip, get_neighbours
import pytest


def test_flip_valid_input():
    assert flip("L") == "R"
    assert flip("R") == "L"


def test_flip_invalid_input():
    with pytest.raises(ValueError, match="Invalid player. Must be 'L' or 'R'."):
        flip("X")
    with pytest.raises(ValueError, match="Invalid player. Must be 'L' or 'R'."):
        flip("")
    with pytest.raises(ValueError, match="Invalid player. Must be 'L' or 'R'."):
        flip(None)


def test_get_neighbours_valid_state():
    # Test with all on the left side
    state = ("L", "L", "L", "L")
    expected = [
        ("R", "L", "R", "L"),
    ]
    assert sorted(get_neighbours(state)) == sorted(expected)

    # Test with all on the right side
    state = ("R", "R", "R", "R")
    expected = [
        ("L", "R", "L", "R"),
    ]
    assert sorted(get_neighbours(state)) == sorted(expected)

    # Test with mixed state
    state = ("L", "R", "L", "R")
    expected = [
        ("R", "R", "L", "R"),
        ("R", "R", "R", "R"),
    ]
    assert sorted(get_neighbours(state)) == sorted(expected)
