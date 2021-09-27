import pytest
from battleships import *

# global variables - ships to be tested
s1 = (3, 2, True, 1, set())
s2 = (1, 6, True, 2, set())
s3 = (6, 2, True, 3, set())
s4 = (4, 9, False, 4, set())
s5 = (6, 2, True, 3, {(6, 2), (6, 3)})
s6 = (4, 9, False, 4, {(4, 9), (5, 9), (6, 9)})
s7 = (3, 2, True, 1, {(3, 2)})
s8 = (1, 6, True, 2, {(1, 6), (1, 7)})
s9 = (6, 2, True, 3, {(6, 2), (6, 3), (6, 4)})
s10 = (4, 9, False, 4, {(4, 9), (5, 9), (6, 9), (7, 9)})

# global variables - fleets to be tested
f1 = [s1, s2, s3, s4]
f2 = [s1, s2, s5, s6]
f3 = [s7, s8, s9, s10]
f4 = [(0, 9, True, 1, set()), (8, 1, True, 1, set()), (9, 9, True, 1, set()),
      (1, 1, True, 2, set()), (7, 7, False, 2, set()), (3, 6, False, 3, set()), s1, s2, s3, s4]
f5 = [(0, 9, True, 1, {(0, 9)}), (8, 1, True, 1, set()), (9, 9, True, 1, set()),
      (1, 1, True, 2, {(1, 1)}), (7, 7, False, 2, {(8, 7)}), (3, 6, False, 3, {(5, 6)}), s7, s8, s9, s10]
f6 = [(0, 9, True, 1, {(0, 9)}), (8, 1, True, 1, {(8, 1)}), (9, 9, True, 1, {(9, 9)}),
      (1, 1, True, 2, {(1, 1), (1, 2)}), (7, 7, False, 2, {(7, 7), (8, 7)}),
      (3, 6, False, 3, {(3, 6), (4, 6), (5, 6)}), s7, s8, s9, s10]


@pytest.mark.parametrize('row, col, fleet, result', [
    # empty fleet
    (4, 5, [], True),
    # no conflict
    (6, 7, f1, True),
    # contains conflict
    (3, 2, f1, False), (6, 4, f1, False), (7, 9, f1, False),
    # horizontal conflict
    (6, 5, f1, False), (5, 8, f1, False),
    # vertical conflict
    (7, 3, f1, False), (8, 9, f1, False),
    # diagonal conflict
    (2, 8, f1, False), (8, 8, f1, False)
])
def test_is_open_sea(row, col, fleet, result):
    assert is_open_sea(row, col, fleet) == result


@pytest.mark.parametrize('row, col, horizontal, length, fleet, result', [
    # ocean boundary - horizontal
    (0, 9, True, 2, f1, False), (0, 9, True, 1, f1, True),
    # ocean boundary - vertical
    (8, 7, False, 3, f1, False), (7, 7, False, 3, f1, True),
    # contains conflict
    (6, 4, False, 2, f1, False),
    # adjacent conflict
    (1, 5, True, 1, f1, False), (4, 2, True, 2, f1, False), (3, 7, True, 2, f1, False),
    # no conflict
    (4, 5, True, 3, f1, True)
])
def test_ok_to_place_ship_at(row, col, horizontal, length, fleet, result):
    assert ok_to_place_ship_at(row, col, horizontal, length, fleet) == result


@pytest.mark.parametrize('row, col, horizontal, length, fleet, result', [
    # add ship (length 4) to the fleet
    (4, 9, False, 4, [], [s4]),
    # add ship (length 3) to the fleet
    (6, 2, True, 3, [s4], [s3, s4]),
    # add ship (length 2) to the fleet
    (1, 6, True, 2, [s3, s4], [s2, s3, s4]),
    # add ship (length 1) to the fleet
    (3, 2, True, 1, [s2, s3, s4], [s1, s2, s3, s4]),
    # add the 10th ship to the fleet
    (3, 6, False, 3, [(0, 9, True, 1, set()), (8, 1, True, 1, set()), (9, 9, True, 1, set()), (1, 1, True, 2, set()),
                      (7, 7, False, 2, set()), s1, s2, s3, s4], f4)
])
def test_place_ship_at(row, col, horizontal, length, fleet, result):
    actual = place_ship_at(row, col, horizontal, length, fleet)
    actual.sort()
    result.sort()
    assert actual == result


@pytest.mark.parametrize('row, col, fleet, result', [
    # check if guess already in hits set
    (6, 3, f2, False), (6, 9, f2, False),
    # check if hits ship horizontally placed
    (6, 5, f2, False), (6, 4, f2, True),
    # check if hits ship vertically placed
    (8, 9, f2, False), (7, 9, f2, True)
])
def test_check_if_hits(row, col, fleet, result):
    assert check_if_hits(row, col, fleet) == result


@pytest.mark.parametrize('row, col, fleet, result', [
    # check if hit to ship (horizontally placed) added correctly
    (3, 2, [(3, 2, True, 1, set()), s2, s5, s6], [s7, s2, s5, s6]),
    (6, 4, [s1, s2, (6, 2, True, 3, {(6, 2), (6, 3)}), s6], [s1, s2, s9, s6]),
    (0, 9, [(0, 9, True, 1, set()), (8, 1, True, 1, set()), (9, 9, True, 1, set()),
            (1, 1, True, 2, {(1, 1)}), (7, 7, False, 2, {(8, 7)}),
            (3, 6, False, 3, {(5, 6)}), s7, s8, s9, s10], f5),
    # check if hit to ship (vertically placed) added correctly
    (7, 9, [s1, s2, s5, (4, 9, False, 4, {(4, 9), (5, 9), (6, 9)})], [s1, s2, s5, s10]),
    (7, 7, [(0, 9, True, 1, {(0, 9)}), (8, 1, True, 1, {(8, 1)}), (9, 9, True, 1, {(9, 9)}),
            (1, 1, True, 2, {(1, 1), (1, 2)}), (7, 7, False, 2, {(8, 7)}),
            (3, 6, False, 3, {(3, 6), (4, 6), (5, 6)}), s7, s8, s9, s10], f6)
])
def test_hit(row, col, fleet, result):
    actual, ship = hit(row, col, fleet)
    actual.sort()
    result.sort()
    assert actual == result


@pytest.mark.parametrize('ship, result', [
    # check ship with length 1
    (s1, False), (s7, True),
    # check horizontally placed ship
    (s5, False), (s9, True),
    # check vertically placed ship
    (s6, False), (s10, True)
])
def test_is_sunk(ship, result):
    assert is_sunk(ship) == result


@pytest.mark.parametrize('ship_hit, result', [
    (s10, "battleship"), (s9, "cruiser"), (s8, "destroyer"), (s7, "submarine"),
    ((1, 1, True, 4, {(1, 1), (1, 2), (1, 3), (1, 4)}), "battleship")
])
def test_ship_type(ship_hit, result):
    assert ship_type(ship_hit) == result


@pytest.mark.parametrize('fleet, result', [
    # check no unsunk ship left
    (f3, False), (f6, False),
    # check unsunk ship left
    (f1, True), (f2, True), (f4, True), (f5, True)
])
def test_are_unsunk_ships_left(fleet, result):
    assert are_unsunk_ships_left(fleet) == result


@pytest.mark.parametrize('guess, result', [
    # number of inputs
    (['1'], False), (['1', '2'], True), (['1', '2', '1'], False), (['1', '2', '1', '2'], False),
    # types of inputs
    (['1', 'a'], False), (['f', '1'], False), (['f', 'a'], False),
    # value of inputs
    (['0', '9'], True), (['-1', '9'], False), (['9', '10'], False),
    # spaces
    ([' 0 ', ' 9 '], True)
])
def test_check_if_input_valid(guess, result):
    assert check_if_input_valid(guess) == result
