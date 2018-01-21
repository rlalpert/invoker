import requests
from heroes import heroes

def get_player_name(steam_id):
    r = requests.get("https://api.opendota.com/api/players/{player_id}".format(player_id=steam_id))

    player = r.json()

    return player["profile"]["personaname"]

def get_player_win(match):
    win_loss = "Loss"
    player_team = "Dire"
    winning_team = "Dire"
    if len(str(match["player_slot"])) == 1:
        player_team = "Radiant"
    if match["radiant_win"]:
        winning_team = "Radiant"
    if player_team == winning_team:
        win_loss = "Win"
    return win_loss

def get_matches(steam_id):
    params = {"limit": "5"}
    r = requests.get("https://api.opendota.com/api/players/{player_id}/matches".format(player_id=steam_id), params=params)

    matches = r.json()
    player_name = get_player_name(steam_id)

    bot_reply = ["__**{player}'s Recent Matches**__".format(player=player_name)]

    for match in matches:
        seconds = match["duration"]%60
        if seconds < 10:
            seconds = "0" + str(seconds)
        duration = "{minutes}:{seconds}".format(minutes=match["duration"]//60, seconds=seconds)
        hero = "*" + heroes[match["hero_id"]] + "*"
        bot_reply.append("<https://www.opendota.com/matches/{match_id}>\n{hero} -- {k} / {d} / {a} -- {duration} -- {win_loss}".
            format(match_id=match["match_id"],
                hero=hero, 
                k=match["kills"], 
                d=match["deaths"], 
                a=match["assists"], 
                duration=duration, 
                win_loss="**"+get_player_win(match)+"**"))

    bot_reply.append("\n*All of {player}'s games can be found at..*.\n <https://www.opendota.com/players/{player_id}>".format(player=player_name, player_id=steam_id))

    return bot_reply
