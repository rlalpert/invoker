import discord
import asyncio
import secret
import diceroller
from matches import get_matches
import markovify
import re
from opinions import dota_responses
import random

client = discord.Client()

with open("markov.txt") as f:
    text_us = f.read()
with open("responses.txt") as g:
    text_invoker = g.read()

def discord_id_to_steam_id(discord_id):
    """
    Grabs 32 bit steam id based on message author's discord user id
    """
    return secret.identities[discord_id]

def mention_to_nick(markov_string):
    """
    Takes a sentence and strips out all @ mentions and converts them to server specific user nicknames.
    """
    server = client.get_server(secret.server_id)
    mention_regex_1 = re.compile(r'<@\d+>')
    mention_regex_2 = re.compile(r'<@!\d+>')
    ment1 = mention_regex_1.findall(markov_string)
    ment2 = mention_regex_2.findall(markov_string)
    for mention in ment1:
        member = server.get_member(mention[2:-1])
        markov_string = markov_string.replace(mention, member.display_name)
    for mention in ment2:
        member = server.get_member(mention[3:-1])
        markov_string = markov_string.replace(mention, member.display_name)
    return markov_string

text_model_us = markovify.Text(text_us)
text_model_invoker = markovify.Text(text_invoker)

model_combo = markovify.combine([text_model_us, text_model_invoker], [1, 20])

@client.event
async def on_ready():
    print("Logged in as {}".format(client.user.name))

@client.event
async def on_message(message):
    cmd_key = '!'
    msg = message.content.lower()
    if message.author.bot:
        return
    elif msg.startswith(cmd_key + "roll"):
        args = message.content[6:]
        if args == "":
            args = "1d20"
        print("Rolling {args} for {client}...".format(args=args, client=message.author))
        roll = diceroller.roll_detailed(args)
        roll["rolls"] = [str(roll) for roll in roll["rolls"]]
        formatted_rolls = ', '.join(roll["rolls"])
        roll["modifiers"] = [str(mod) for mod in roll["modifiers"]]
        formatted_modifiers = ', '.join(roll["modifiers"])
        reply = "{friendo},\nYour total is **{total}**.".format(friendo=message.author.mention, total=roll["total"])
        if len(roll["rolls"]) > 1:
            reply += "\nYour rolls were **{rolls}**.".format(rolls=formatted_rolls)
        if roll["modifiers"]:
            reply += "\nYour modifiers were **{modifiers}**".format(modifiers=formatted_modifiers)
        await client.send_message(message.channel, reply)
        return
    elif msg.startswith(cmd_key + "matches"):
        print("Getting matches for {client}".format(client=message.author))
        args = message.content[9:]
        if args.strip() == "":
            args = discord_id_to_steam_id(message.author.id)
        elif message.raw_mentions:
            args = discord_id_to_steam_id(message.raw_mentions[0])
        matches = get_matches(args)
        reply = ""
        for line in matches:
            reply += line + "\n"
        await client.send_message(message.channel, reply)
        return
    elif msg.startswith(cmd_key + "dota"):
        reply = random.choice(dota_responses)
        await client.send_message(message.channel, reply)
    for mention in message.mentions:
        if mention.id == "403970167052173312":
            sentence = model_combo.make_short_sentence(140)
            await client.send_message(message.channel, mention_to_nick(sentence))
            return
    else:
        with open("markov.txt", "a") as file:
            file.write(message.content + "\n")

client.run(secret.bot_token)