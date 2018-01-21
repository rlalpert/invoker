import discord
import asyncio
import secret
import diceroller
from matches import get_matches

client = discord.Client()

@client.event
async def on_ready():
    print("Logged in as {}".format(client.user.name))

@client.event
async def on_message(message):
    msg = message.content.lower()
    if msg.startswith("roll"):
        args = message.content[6:]
        print("Rolling {args} for {client}...".format(args=args, client=message.author))
        roll = diceroller.roll_detailed(args)
        await client.send_message(message.channel, str(roll))
    elif msg.startswith("matches"):
        print("Getting matches for {client}".format(client=message.author))
        args = message.content[9:]
        matches = get_matches(args)
        reply = ""
        for line in matches:
            reply += line + "\n"
        await client.send_message(message.channel, reply)

client.run(secret.bot_token)