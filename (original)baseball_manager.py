import csv

def display_separator():
    print("================================================================")

def display_title():
    print("                   Baseball Team Manager")

def display_menu():
    print("MENU OPTIONS")
    print("1 – Display lineup")
    print("2 - Add player")
    print("3 - Remove player")
    print("4 - Move player")
    print("5 - Edit player position")
    print("6 - Edit player stats")
    print("7 - Exit program")
    print("")
    print("POSITIONS")
    print("C, 1B, 2B, 3B, SS, LF, CF, RF, P")

def get_batting_avg(at_bats, hits):
    if at_bats == 0:
        return 0
    avg = hits / at_bats
    return round(avg, 3)

def get_int(prompt):
    while True:
        try:
            i = int(input(prompt))
            if 0 <= i <= 10000:
                return i
            else:
                print("Invalid integer. Must be from 0 to 10,000.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def write_lineup(lineup):
    try:
        with open("line_up.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(lineup)
    except IOError:
        print("An error occurred while writing to the file.")

def read_lineup():
    try:
        with open("line_up.csv", newline="") as file:
            reader = csv.reader(file)
            return list(reader)
    except IOError:
        print("An error occurred while reading the file.")
        return []

def display_lineup():
    lineup = read_lineup()
    print("{:<20} {:<10} {:<10} {:<10} {:<10}".format("Name", "Pos", "AB", "H", "AVG"))
    display_separator()
    for player in lineup:
        print("{:<20} {:<10} {:<10} {:<10} {:<10}".format(player[0], player[1], player[2], player[3], player[4]))

def add_player():
    name = input("Enter player's name: ")
    position = input("Enter player's position (C, 1B, 2B, 3B, SS, LF, CF, RF, P): ")
    at_bats = get_int("Enter official number of at bats: ")
    hits = get_int("Enter number of hits: ")
    avg = get_batting_avg(at_bats, hits)
    lineup = read_lineup()
    lineup.append([name, position, at_bats, hits, avg])
    write_lineup(lineup)

def remove_player():
    name = input("Enter player's name to remove: ")
    lineup = read_lineup()
    lineup = [player for player in lineup if player[0] != name]
    write_lineup(lineup)

def move_player():
    name = input("Enter the name of the player to move: ")
    lineup = read_lineup()

    # Check if player exists in lineup
    player_exists = any(name == player[0] for player in lineup)
    if not player_exists:
        print("Player not found in the lineup.")
        return

    try:
        new_position = int(input("Enter the new position number for the player (1 to {}): ".format(len(lineup))))
        if new_position < 1 or new_position > len(lineup):
            print("Invalid position number. It should be between 1 and {}.".format(len(lineup)))
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    # Find and move the player
    player_to_move = next(player for player in lineup if player[0] == name)
    lineup.remove(player_to_move)
    lineup.insert(new_position - 1, player_to_move)

    write_lineup(lineup)
    print("Player moved successfully.")


def edit_player_position():
    name = input("Enter player's name: ")
    new_position = input("Enter new position (C, 1B, 2B, 3B, SS, LF, CF, RF, P): ")
    lineup = read_lineup()
    for player in lineup:
        if player[0] == name:
            player[1] = new_position
    write_lineup(lineup)

def edit_player_stats():
    name = input("Enter player's name: ")
    new_at_bats = get_int("Enter new official number of at bats: ")
    new_hits = get_int("Enter new number of hits: ")
    lineup = read_lineup()
    for player in lineup:
        if player[0] == name:
            player[2] = new_at_bats
            player[3] = new_hits
            player[4] = get_batting_avg(new_at_bats, new_hits)
    write_lineup(lineup)

def main():
    display_separator()
    display_title()

    while True:
        display_separator()
        display_menu()
        display_separator()
        
        try:
            option = int(input("Menu option: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if option == 1:
            display_lineup()
        elif option == 2:
            add_player()
        elif option == 3:
            remove_player()
        elif option == 4:
            move_player()  # This needs further implementation
        elif option == 5:
            edit_player_position()
        elif option == 6:
            edit_player_stats()
        elif option == 7:
            print("Bye!")
            break
        else:
            print("Not a valid option. Please try again.")


if __name__ == "__main__":
    main()
