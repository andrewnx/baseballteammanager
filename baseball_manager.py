from models import db, User, Player

# Define the default lineup
default_lineup = [
    {"name": "Jordan Bell", "position": "P", "at_bats": 30, "hits": 5},
    {"name": "John Doe", "position": "C", "at_bats": 50, "hits": 15},
    {"name": "Jane Smith", "position": "1B", "at_bats": 70, "hits": 20},
    {"name": "Mike Johnson", "position": "2B", "at_bats": 60, "hits": 18},
    {"name": "Sarah Brown", "position": "3B", "at_bats": 55, "hits": 16},
    {"name": "Alex Lee", "position": "SS", "at_bats": 65, "hits": 22},
    {"name": "Chris Green", "position": "LF", "at_bats": 45, "hits": 12},
    {"name": "Pat Morgan", "position": "CF", "at_bats": 80, "hits": 30},
    {"name": "Taylor King", "position": "RF", "at_bats": 40, "hits": 10}
]

def get_batting_avg(at_bats, hits):
    if at_bats == 0:
        return 0
    avg = hits / at_bats
    return round(avg, 3)

def clone_default_lineup_for_user(user_id):
    user = User.objects.get(id=user_id)
    for player_data in default_lineup:
        avg = get_batting_avg(player_data["at_bats"], player_data["hits"])
        Player(name=player_data["name"], position=player_data["position"],
               at_bats=player_data["at_bats"], hits=player_data["hits"],
               avg=avg, user=user).save()

def get_players(user_id):
    return Player.objects(user=user_id)

def add_player(name, position, at_bats, hits, user_id):
    user = User.objects.get(id=user_id)
    avg = get_batting_avg(at_bats, hits)
    Player(name=name, position=position, at_bats=at_bats, hits=hits, avg=avg, user=user).save()

def update_player(player_id, name, position, at_bats, hits):
    player = Player.objects(id=player_id).first()
    if player:
        player.update(
            name=name,
            position=position,
            at_bats=at_bats,
            hits=hits,
            avg=get_batting_avg(at_bats, hits)
        )

def remove_player(player_id, user_id):
    player_to_remove = Player.objects(id=player_id, user=user_id).first()
    if player_to_remove:
        player_to_remove.delete()

def get_player(player_id):
    return Player.objects(id=player_id).first()
