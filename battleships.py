#see the readme.md file for description and data
import random


def _calculate_ship_coordinates(ship):
    # returns a set of tuple coordinates
    ship_coords = list()
    for x in range(ship[3]):
        if ship[2] == True:
            ship_coords.append((ship[0], ship[1] + x))
        else:
            ship_coords.append((ship[0] + x, ship[1]))
    return set(ship_coords)


def is_sunk(ship):
    coords = _calculate_ship_coordinates(ship)
    if coords == ship[4]:
        return True
    else:
        return False


def ship_type(ship):
    if ship[3] == 1:
        return "submarine"
    elif ship[3] == 2:
        return "destroyer"
    elif ship[3] == 3:
        return "cruiser"
    elif ship[3] == 4:
        return "battleship"
    else:
        raise Exception("Unknown ship type!")


def is_open_sea(row, column, fleet):
    # calculate coords for all ships in fleet
    total_ship_coords = list()
    for ship in fleet:
        total_ship_coords.extend(_calculate_ship_coordinates(ship))
    total_ship_coords = list(total_ship_coords)
    # distance of given coord from all ships coords must be >1 for not being adjacent to any ship
    for point in total_ship_coords:
        if abs(point[0] - row) > 1 or abs(point[1] - column) > 1:
            continue
        else:
            return False
    return True


def ok_to_place_ship_at(row, column, horizontal, length, fleet):
    candidate_ship = (row, column, horizontal, length)
    coords = _calculate_ship_coordinates(candidate_ship)
    coords = list(coords)
    for point in coords:
        # check if coords fall out of map
        if 9 < point[0] < 0 or 9 < point[1] < 0:
            return False
        # and check if are in open sea
        if is_open_sea(point[0], point[1], fleet):
            continue
        else:
            return False
    return True


def place_ship_at(row, column, horizontal, length, fleet):
    fleet.append((row, column, horizontal, length, {}))


def randomly_place_all_ships():
    # start with bigger ships (Battleship)
    fleet = list()
    for i in range(4):
        length = 4 - i
        for j in range(i + 1):
            # emulate a do while
            while True:
                row = random.randint(0, 9)
                column = random.randint(0, 9)
                horizontal = bool(random.getrandbits(1))
                if ok_to_place_ship_at(row, column, horizontal, length, fleet):
                    place_ship_at(row, column, horizontal, length, fleet)
                    break
    return fleet


def check_if_hits(row, column, fleet):
    for ship in fleet:
        coords = _calculate_ship_coordinates(ship)
        if (row, column) in coords:
            return True
    return False


def hit(row, column, fleet):
    for idx in range(len(fleet)):
        coords = _calculate_ship_coordinates(fleet[idx])
        if (row, column) in coords:
            fleet[idx][4].add((row, column))
            return fleet, fleet[idx]


def are_unsunk_ships_left(fleet):
    for ship in fleet:
        if not is_sunk(ship):
            return True
    return False


def main():
    #the implementation provided below is indicative only
    #you should improve it or fully rewrite to provide better functionality (see readme file)
    current_fleet = randomly_place_all_ships()

    game_over = False
    shots = 0

    while not game_over:
        loc_str = input("Enter row and colum to shoot (separted by space): ").split()    
        current_row = int(loc_str[0])
        current_column = int(loc_str[1])
        shots += 1
        if check_if_hits(current_row, current_column, current_fleet):
            print("You have a hit!")
            (current_fleet, ship_hit) = hit(current_row, current_column, current_fleet)
            if is_sunk(ship_hit):
                print("You sank a " + ship_type(ship_hit) + "!")
        else:
            print("You missed!")

        if not are_unsunk_shis_left(current_fleet): game_over = True

    print("Game over! You required", shots, "shots.")


if __name__ == '__main__': #keep this in
    main()
