import csv

def get_batting_avg(at_bats, hits):
    if at_bats == 0:
        return 0
    avg = hits / at_bats
    return round(avg, 3)

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

def add_player(name, position, at_bats, hits):
    avg = get_batting_avg(at_bats, hits)
    lineup = read_lineup()
    lineup.append([name, position, at_bats, hits, avg])
    write_lineup(lineup)

def remove_player(name):
    lineup = read_lineup()
    lineup = [player for player in lineup if player[0] != name]
    write_lineup(lineup)

def move_player(name, new_position):
    lineup = read_lineup()
    player_exists = any(name == player[0] for player in lineup)
    if not player_exists:
        return "Player not found in the lineup."

    player_to_move = next(player for player in lineup if player[0] == name)
    lineup.remove(player_to_move)
    lineup.insert(new_position - 1, player_to_move)

    write_lineup(lineup)
    return "Player moved successfully."

def edit_player_position(name, new_position):
    lineup = read_lineup()
    for player in lineup:
        if player[0] == name:
            player[1] = new_position
    write_lineup(lineup)

def edit_player_stats(name, new_at_bats, new_hits):
    lineup = read_lineup()
    for player in lineup:
        if player[0] == name:
            player[2] = new_at_bats
            player[3] = new_hits
            player[4] = get_batting_avg(new_at_bats, new_hits)
    write_lineup(lineup)
