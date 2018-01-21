import discord
import asyncio
import secret
import diceroller
from matches import get_matches
import markovify

client = discord.Client()

with open("markov.txt") as f:
    text = f.read()

text_model = markovify.Text(text)

@client.event
async def on_ready():
    print("Logged in as {}".format(client.user.name))

@client.event
async def on_message(message):
    for mention in message.mentions:
        if mention.id == "403970167052173312":
            # await client.add_reaction(message, "😎")
            await client.send_message(message.channel, text_model.make_short_sentence(140))
    msg = message.content.lower()
    if msg.startswith("^roll"):
        args = message.content[6:]
        print("Rolling {args} for {client}...".format(args=args, client=message.author))
        roll = diceroller.roll_detailed(args)
        await client.send_message(message.channel, str(roll))
    elif msg.startswith("^matches"):
        print("Getting matches for {client}".format(client=message.author))
        args = message.content[9:]
        matches = get_matches(args)
        reply = ""
        for line in matches:
            reply += line + "\n"
        await client.send_message(message.channel, reply)
client.run(secret.bot_token)