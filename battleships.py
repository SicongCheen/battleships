# Battleships
# Birkbeck PoP I Module Project 2020
# By Sicong Chen 13185775 sicongchen1219@gmail.com

import random

# global variables
LEN_OCEAN = 10
WIDTH_OCEAN = 10

NUM_OF_SHIPS = 10
NUM_OF_BATTLESHIPS = 1
NUM_OF_CRUISERS = 2
NUM_OF_DESTROYERS = 3
NUM_OF_SUBMARINES = 4

LEN_BATTLESHIP = 4
LEN_CRUISER = 3
LEN_DESTROYER = 2
LEN_SUBMARINE = 1


def is_open_sea(row, column, fleet):
    """
    This method checks if the square given by row and column neither contains nor is adjacent
    (horizontally, vertically, or diagonally) to some ship in fleet.
    :param row: int
    :param column: int
    :param fleet: list
    :returns result: bool - True if so and False otherwise
    """
    result = True
    if fleet:
        for i in range(len(fleet)):
            # get squares occupied by a ship
            squares_occupied = []
            for j in range(fleet[i][3]):
                # if horizontal
                if fleet[i][2]:
                    squares_occupied.append((fleet[i][0], fleet[i][1] + j))
                # if vertical
                else:
                    squares_occupied.append((fleet[i][0] + j, fleet[i][1]))
            # check squares conflicts
            for j in range(len(squares_occupied)):
                if abs(row - squares_occupied[j][0]) <= 1 and abs(column - squares_occupied[j][1]) <= 1:
                    result = False
                    return result
    return result


def ok_to_place_ship_at(row, column, horizontal, length, fleet):
    """
    This method checks if addition of a ship, specified by row, column, horizontal, and length,
    to the fleet results in a legal arrangement.
    :param row: int
    :param column: int
    :param horizontal: bool
    :param length: int
    :param fleet: list
    :returns result: bool - True if so and False otherwise
    """
    result = True
    if horizontal:
        # check ocean boundary horizontally
        if column + length > WIDTH_OCEAN:
            result = False
        else:
            # check ship conflict
            for i in range(length):
                if not is_open_sea(row, column + i, fleet):
                    result = False
                    break
    else:
        # check ocean boundary vertically
        if row + length > LEN_OCEAN:
            result = False
        else:
            # check ship conflict
            for i in range(length):
                if not is_open_sea(row + i, column, fleet):
                    result = False
                    break
    return result


def place_ship_at(row, column, horizontal, length, fleet):
    """
    This method returns a new fleet that is the result of adding a ship, specified by row, column, horizontal,
    and length to fleet.
    :param row: int
    :param column: int
    :param horizontal: bool
    :param length: int
    :param fleet: list
    :returns fleet: list
    """
    hits = set()
    fleet.append((row, column, horizontal, length, hits))
    return fleet


def randomly_place_all_ships():
    """
    This method returns a fleet that is a result of a random legal arrangement of the 10 ships in the ocean.
    :returns fleet: list
    """
    fleet = []
    len_of_ships = [LEN_BATTLESHIP] * NUM_OF_BATTLESHIPS + [LEN_CRUISER] * \
        NUM_OF_CRUISERS + [LEN_DESTROYER] * NUM_OF_DESTROYERS + \
        [LEN_SUBMARINE] * NUM_OF_SUBMARINES
    i = 0

    while len(fleet) < NUM_OF_SHIPS:
        # get random values for row, column and horizontal
        row = random.randint(0, LEN_OCEAN - 1)
        column = random.randint(0, WIDTH_OCEAN - 1)
        horizontal = random.choice([True, False])

        if ok_to_place_ship_at(row, column, horizontal, len_of_ships[i], fleet):
            fleet = place_ship_at(row, column, horizontal,
                                  len_of_ships[i], fleet)
            i += 1

    return fleet


def check_if_hits(row, column, fleet):
    """
    This method checks if the shot of the human player at the square represented by row and column
    hits any of the ships of fleet.
    :param row: int
    :param column: int
    :param fleet: list
    :returns result: bool - True if so and False otherwise
    """
    result = False
    for i in range(len(fleet)):
        # check if guess already in hits set:
        if (row, column) in fleet[i][4]:
            break
        for j in range(fleet[i][3]):
            # if horizontal
            if fleet[i][2]:
                if row == fleet[i][0] and column == fleet[i][1] + j:
                    result = True
                    break
            # if vertical
            else:
                if row == fleet[i][0] + j and column == fleet[i][1]:
                    result = True
                    break
    return result


def hit(row, column, fleet):
    """
    This method returns a tuple (fleet, ship) where ship is the ship from the fleet that receives a hit
    by the shot at the square represented by row and column, and fleet is the fleet resulting from this hit.
    :param row: int
    :param column: int
    :param fleet: list
    :returns fleet, ship: tuple
    """
    for i in range(len(fleet)):
        for j in range(fleet[i][3]):
            # if horizontal
            if fleet[i][2]:
                if row == fleet[i][0] and column == fleet[i][1] + j:
                    fleet[i][4].add((row, column))
                    return fleet, fleet[i]
            # if vertical
            else:
                if row == fleet[i][0] + j and column == fleet[i][1]:
                    fleet[i][4].add((row, column))
                    return fleet, fleet[i]


def is_sunk(ship):
    """
    This method checks if a ship is sunk or not after getting a shot from user.
    :param ship: tuple
    :returns result: bool - True if so and False otherwise
    """
    result = True
    for i in range(ship[3]):
        # if horizontal
        if ship[2]:
            if(ship[0], ship[1] + i) not in ship[4]:
                result = False
                break
        # if vertical
        else:
            if(ship[0] + i, ship[1]) not in ship[4]:
                result = False
                break
    return result


def ship_type(ship_hit):
    """
    This method returns one of the strings "battleship", "cruiser", "destroyer", or "submarine"
    identifying the type of ship.
    :param ship_hit: tuple
    :returns ship_type: string
    """
    if ship_hit[3] == LEN_BATTLESHIP:
        ship_type = "battleship"
    if ship_hit[3] == LEN_CRUISER:
        ship_type = "cruiser"
    if ship_hit[3] == LEN_DESTROYER:
        ship_type = "destroyer"
    if ship_hit[3] == LEN_SUBMARINE:
        ship_type = "submarine"
    return ship_type


def are_unsunk_ships_left(fleet):
    """
    This method checks if there is any ship left unsunk in the fleet.
    :param fleet: list
    :returns result: bool - True if so and False otherwise
    """
    result = False
    for i in range(len(fleet)):
        if not is_sunk(fleet[i]):
            result = True
            break
    return result


def check_if_input_valid(guess):
    """
    This method checks if the input from users are valid or not.
    :param guess: list
    :returns valid: bool - True if so and False otherwise
    """
    valid = True
    if len(guess) != 2:
        valid = False
    else:
        valid_guess = [str(i) for i in range(0, 10)]
        if guess[0].strip() not in valid_guess or guess[1].strip() not in valid_guess:
            valid = False
    return valid


def setup_ocean():
    """
    This method sets up ocean graphically.
    :returns ocean: list
    """
    ocean = []
    for i in range(LEN_OCEAN):
        ocean.append(["."] * WIDTH_OCEAN)
    return ocean


def update_shots_graphic(ocean, fleet, missed_shots):
    """
    This method updates the graphic after user has a shot each time.
    :param ocean: list
    :param fleet: list
    :param missed_shots: set
    """
    for element in missed_shots:
        row = element[0]
        col = element[1]
        ocean[row][col] = "-"
    for i in range(len(fleet)):
        hits = fleet[i][4]
        if len(hits) == fleet[i][3]:
            if fleet[i][3] == 4:
                letter = "B"
            elif fleet[i][3] == 3:
                letter = "C"
            elif fleet[i][3] == 2:
                letter = "D"
            elif fleet[i][3] == 1:
                letter = "S"
        else:
            letter = "*"
        for element in hits:
            row = element[0]
            col = element[1]
            ocean[row][col] = letter


def print_shots_graphic(ocean):
    """
    This method prints the graphic to the console.
    :param ocean: list
    """
    print("     0 1 2 3 4 5 6 7 8 9 ")
    print("    ---------------------")
    for i in range(LEN_OCEAN):
        print(" " + str(i) + " | ", end="")
        for j in range(WIDTH_OCEAN):
            if j == WIDTH_OCEAN - 1:
                print(ocean[i][j])
            else:
                print(ocean[i][j], end=" ")


def main():
    """
    This method prompts the user to call out rows and columns of shots and outputs the responses of the computer
    iteratively until the game stops.
    """
    game_over = False
    quit_game = False
    shots = 0
    missed_shots = set()

    # set up ocean and fleet
    ocean = setup_ocean()
    current_fleet = randomly_place_all_ships()

    # main game loop
    while not game_over:

        # game visualization (console)
        update_shots_graphic(ocean, current_fleet, missed_shots)
        print_shots_graphic(ocean)

        # get input from users
        while True:
            user_input = input(
                "Enter row and column to shoot (Press \'Q\' to quit): ").strip()
            if user_input != "Q" and user_input != "q":
                guess = user_input.split()
                if check_if_input_valid(guess):
                    guess_row = int(guess[0].strip())
                    guess_column = int(guess[1].strip())
                    break
                else:
                    print(
                        "****************************************************************************")
                    print("Invalid inputs.")
                    print(
                        "Both row and column should be integers between 0 and 9 (separated by space).")
                    print(
                        "****************************************************************************")
            else:
                quit_game = True
                break

        if quit_game:
            break

        shots += 1

        # evaluate shot result
        if check_if_hits(guess_row, guess_column, current_fleet):
            print("\n**************************")
            print("You have a hit!")
            current_fleet, ship_hit = hit(
                guess_row, guess_column, current_fleet)
            if is_sunk(ship_hit):
                print("You sank a " + ship_type(ship_hit) + "!")
            print("**************************")
        else:
            missed_shots.add((guess_row, guess_column))
            print("\n**************************")
            print("You missed!")
            print("**************************")

        if not are_unsunk_ships_left(current_fleet):
            game_over = True

    if game_over:
        # print last shot
        update_shots_graphic(ocean, current_fleet, missed_shots)
        print_shots_graphic(ocean)
        # print GAME OVER message
        print("**********************************")
        print("GAME OVER!")
        print("You required", shots, "shots.")
        print("**********************************")


# if start from battleships.py
if __name__ == '__main__':
    main()
