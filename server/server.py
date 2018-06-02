import json
import random

from deck import Deck
from copy import deepcopy
from websocket_server import WebsocketServer

ready_users = {}

def shuffle_deck(deck):
    return(random.shuffle(deck))


def new_client(client, server):
    if (len(server.clients) < 3):
        clients = [x for x in server.clients if x["id"] != client["id"]]

        px = {
            "type": "init",
            "data": {
                "_id": client["id"],
                "users": [x["id"] for x in clients] if clients else ""
            }
        }
        px2 = {
            "type": "player_join",
            "data": {
                "_id": client["id"],
            }
        }

        server.send_message(client, json.dumps(px))
        for i in clients:
            server.send_message(i, json.dumps(px2))
    else:
        px = {
        "type": "error",
            "data": {
                "msg": "Lobby is full"
            }
        }

        server.send_message(client, json.dumps(px))


def client_left(client, server):
    px = {
        "type": "player_leave",
        "data": {
            "_id": client["id"]
        }
    }

    remove_user(client)
    server.send_message_to_all(json.dumps(px))


def remove_user(client):
    if (ready_users.has_key(client["id"])):
        ready_users.pop(client["id"], None)


def message_received(client, server, message):
    px = json.loads(message)
    rx = {
        "type": "",
        "data": { }
    }

    if (px["command"] == "get_users"):
        get_users(rx, client, server, message)
    elif (px["command"] == "get_deck"):
        get_deck(rx, client, server, message)
    elif (px["command"] == "user_waiting"):
        user_waiting(rx, client, server, message)
    elif (px["command"] == "user_standby"):
        user_standby(rx, client, server, message)
    elif (px["command"] == "user_ready"):
        user_ready(rx, client, server, message)
    else:
        pass
        #server.send_message_to_all(repr(server.clients))


def get_users(rx, client, server, message):
    rx["type"] = "get_users"
    rx["data"] = {
        "users": repr(server.clients),
        "user_count": len(server.clients)
    }
    server.send_message(client, json.dumps(rx))
    print server.clients


def user_waiting(rx, client, server, message):
    clients = [x for x in server.clients if x["id"] != client["id"]]

    rx["type"] = "opponent_waiting"
    rx["data"] = {
    }

    remove_user(client)
    server.send_message(clients[0], json.dumps(rx))


def user_standby(rx, client, server, message):
    clients = [x for x in server.clients if x["id"] != client["id"]]

    rx["type"] = "opponent_standby"
    rx["data"] = {
    }

    server.send_message(clients[0], json.dumps(rx))
    add_user_to_match(client, server)


def user_ready(rx, client, server, message):
    player_deck = Deck()
    player_deck.build_deck()

    rx["type"] = "room_ready"
    rx["data"] = { 
        "deck": player_deck.cards_dict()
    }
    server.send_message(client, json.dumps(rx))


def get_deck(rx, client, server, message):
    rx["type"] = "return_deck"
    rx["data"] = {
        "deck": build_deck()
    }

    server.send_message(client, json.dumps(rx))


def add_user_to_match(client, server):
    ready_users[client["id"]] = client

    if (len(ready_users) == 2):
        for k in ready_users.keys():
            user_ready({}, ready_users[k], server, "")


if (__name__ == "__main__"):
    server = WebsocketServer(9001)
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    server.run_forever()
