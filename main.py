"""
Created by Epic at 9/5/20
"""

import speedcord
from speedcord.http import Route
from os import environ as env
from logging import basicConfig, DEBUG
from ujson import load

client = speedcord.Client(intents=512)
basicConfig(level=DEBUG)


async def on_ready():
    await client.connected.wait()
    print("h!")
    if env.get("ENVIRONMENT", "production") == "production":
        r = Route("POST", "/applications/{user_id}/commands", user_id=env["USER_ID"])
    else:
        r = Route("POST", "/applications/{user_id}/guilds/{guild_id}/commands", user_id=env["USER_ID"],
                  guild_id=env["GUILD_ID"])
    with open("commands.json") as f:
        commands = load(f)

    for command in commands:
        await client.http.request(r, json=command)


client.loop.create_task(on_ready())
client.token = env["TOKEN"]
client.run()
