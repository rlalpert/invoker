import requests
from heroes import heroes

def get_player(steam_id):
    r = requests.get("https://api.opendota.com/api/players/{player_id}".format(player_id=steam_id))

    player = r.json()

    return player["profile"]["personaname"]

def get_matches(steam_id):
    params = {"limit": "5"}
    r = requests.get("https://api.opendota.com/api/players/{player_id}/matches".format(player_id=steam_id), params=params)

    matches = r.json()

    bot_reply = ["__{player}'s Recent Matches__".format(player=get_player(steam_id))]

    for match in matches:
        win_loss = "Loss"
        hero = "*" + heroes[match["hero_id"]] + "*"
        duration = "{minutes}:{seconds}".format(minutes=match["duration"]//60, seconds=match["duration"]%60)
        if len(str(match["player_slot"])) == 1 and match["radiant_win"]:
            win_loss = "Win"
        bot_reply.append("<https://www.opendota.com/matches/{match_id}>\n{hero} -- {k} / {d} / {a} -- {duration} -- {win_loss}".
            format(match_id=match["match_id"], hero=hero, 
                    k=match["kills"], d=match["deaths"], 
                    a=match["assists"], duration=duration, 
                   win_loss="**"+win_loss+"**"))

    return bot_reply
