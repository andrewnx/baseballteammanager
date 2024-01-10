from bson import ObjectId
import logging
logging.basicConfig(level=logging.DEBUG)
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

def clone_default_lineup_for_user(mongo, user_id):
    players_collection = mongo.db.players  # Access the 'players' collection
    for player_data in default_lineup:
        player_data['user_id'] = user_id
        player_data['avg'] = get_batting_avg(player_data["at_bats"], player_data["hits"])
        logging.debug(f"Cloning player for user {user_id}: {player_data}")
        players_collection.insert_one(player_data)

def get_players(mongo, user_id):
    players_collection = mongo.db.players
    return list(players_collection.find({'user_id': user_id}))

def add_player(mongo, name, position, at_bats, hits, user_id):
    players_collection = mongo.db.players
    avg = get_batting_avg(at_bats, hits)
    new_player = {
        "name": name,
        "position": position,
        "at_bats": at_bats,
        "hits": hits,
        "avg": avg,
        "user_id": user_id
    }
    players_collection.insert_one(new_player)

def update_player(mongo, player_id, name, position, at_bats, hits):
    players_collection = mongo.db.players
    avg = get_batting_avg(at_bats, hits)
    players_collection.update_one(
        {'_id': ObjectId(player_id)},
        {'$set': {
            "name": name,
            "position": position,
            "at_bats": at_bats,
            "hits": hits,
            "avg": avg
        }}
    )

def remove_player(mongo, player_id, user_id):
    players_collection = mongo.db.players
    players_collection.delete_one({'_id': player_id, 'user_id': user_id})

def get_player(mongo, player_id):
    players_collection = mongo.db.players
    return players_collection.find_one({'_id': player_id})

def add_user(mongo, user_data):
    users_collection = mongo.db.users
    new_user = users_collection.insert_one(user_data)
    return new_user.inserted_id

def get_user(mongo, username):
    users_collection = mongo.db.users
    return users_collection.find_one({'username': username})