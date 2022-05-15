
import discord
from discord.utils import get
import random
import os
import re

GUILD_ID = 237682693314314240
LOG_CHANNEL_ID = 722820090797490176
WELCOME_CHANNEL_ID = 722877330552520825
WELCOME_MESSAGES = [
    "Hallo %s und willkommen auf dem Server.\nUm vollen Zugriff auf alle (fast) alle Channels zu haben, gehe zu <#513804036550426665> und akzeptiere die Regeln. \nDanach kannst dir in <#721758014763302983> deine Rollen für bestimmte Themen zuweisen.",
    "Moin Moin %s. Willkommen auf dem Server.\nUm vollen Zugriff auf alle (fast) alle Channels zu haben, gehe zu <#513804036550426665> und akzeptiere die Regeln. \nDanach kannst dir in <#721758014763302983> deine Rollen für bestimmte Themen zuweisen.",
    "Servus %s. Willkommen auf dem Server.\nUm vollen Zugriff auf alle (fast) alle Channels zu haben, gehe zu <#513804036550426665> und akzeptiere die Regeln. \nDanach kannst dir in <#721758014763302983> deine Rollen für bestimmte Themen zuweisen."
]

MEMBER_ROLE_ID = 722417372367028296
MEMBER_ROLE_REASON = "Rules accepted"
MEMBER_ROLE_MESSAGE_ID = 722417108637450261
MEMBER_ROLE_REACTION = "👍"

ROLE_ASSIGN_MESSAGE_ID = 722420641206370355
ROLES_TO_ASSIGN = {
    "⌨️": 722815909428723775,    # Programmieren
    "🛠️": 722816050910986313,   # Elektronik
    "🕹️": 722816253114187846    # Gaming
}
ROLE_ASSIGN_REASON = 'User opted-in to topic role'

PING_ROLE_ASSIGN_MESSAGE_ID = 722422434359410708
PING_ROLES_TO_ASSIGN = {
    "🤖": 722168725729706044,    # Apex
    "🦖": 722847166904795196,    # Ark: Survival Evolved
    "🎲": 722847279748481035,    # Community Games
    "🤡": 722846926038368297,    # Fortnite
    "🩸": 722167935489278144,    #Pubg
    "⛏️": 722168026727710773,    # Minecraft
    "🖍️": 722168736584433674,    # Sketchful
    "🔫": 722167815582253067,    # Warzone
    "🔪": 722167601756766268     # Valorant
}
PING_ROLE_ASSIGN_REASON = 'User opted-in to ping role'

RWU_ROLE_ID = 735097341899440228

client = discord.Client()

log_channel = None
welcome_channel = None

@client.event
async def on_ready():
    global log_channel, welcome_channel
    log_channel = client.get_channel(LOG_CHANNEL_ID)
    welcome_channel = client.get_channel(WELCOME_CHANNEL_ID)
    guild = discord.utils.find(lambda g: g.id == GUILD_ID, client.guilds)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})'
    )
    await log_channel.send("SKYNET activated!")


@client.event
async def on_member_join(member):
    global log_channel
    await log_channel.send("**INFO**: <@" + str(member.id) + "> joined this server!")
    welcome_msg = WELCOME_MESSAGES[random.randint(0, len(WELCOME_MESSAGES)-1)]
    await welcome_channel.send(welcome_msg % ("<@" + str(member.id) + ">"))

@client.event
async def on_member_remove(member):
    global log_channel
    await log_channel.send("**INFO**: <@" + str(member.id) + "> left this server!")

@client.event
async def on_raw_reaction_add(payload):
    global log_channel

    if payload.guild_id is None:
        return

    guild = client.get_guild(payload.guild_id)

    if payload.emoji.is_unicode_emoji():
        # Member role assignment
        if payload.message_id == MEMBER_ROLE_MESSAGE_ID:
            if payload.emoji.name == MEMBER_ROLE_REACTION:
                role = get(guild.roles, id=MEMBER_ROLE_ID)
                user = get(guild.members, id=payload.user_id)
                if user is not None:
                    await user.add_roles(role, reason=MEMBER_ROLE_REASON)
                    await log_channel.send("**Success**: Added role <@&" + str(role.id) + "> to <@" + str(payload.user_id) + ">!")
                else:
                    await log_channel.send("**Error**: While assigning role by reaction; user is None")

        # Topic role assignment
        if payload.message_id == ROLE_ASSIGN_MESSAGE_ID:
            if payload.emoji.name in ROLES_TO_ASSIGN:
                role = get(guild.roles, id=ROLES_TO_ASSIGN[payload.emoji.name])
                user = get(guild.members, id=payload.user_id)
                if user is not None:
                    await user.add_roles(role, reason=ROLE_ASSIGN_REASON)
                    await log_channel.send("**Success**: Added role <@&" + str(role.id) + "> to <@" + str(payload.user_id) + ">!")
                else:
                    await log_channel.send("**Error**: While assigning ping role by reaction. User is None")

        # Ping role assignment
        if payload.message_id == PING_ROLE_ASSIGN_MESSAGE_ID:
            if payload.emoji.name in PING_ROLES_TO_ASSIGN:
                role = get(guild.roles, id=PING_ROLES_TO_ASSIGN[payload.emoji.name])
                user = get(guild.members, id=payload.user_id)
                if user is not None:
                    await user.add_roles(role, reason=PING_ROLE_ASSIGN_REASON)
                    await log_channel.send("**Success**: Added role <@&" + str(role.id) + "> to <@" + str(payload.user_id) + ">!")
                else:
                    await log_channel.send("**Error**: While assigning ping role by reaction. User is None.")

@client.event
async def on_raw_reaction_remove(payload):
    global log_channel

    if payload.guild_id is None:
        return

    guild = client.get_guild(payload.guild_id)

    if payload.emoji.is_unicode_emoji():
        # Member role assignment
        if payload.message_id == MEMBER_ROLE_MESSAGE_ID:
            if payload.emoji.name == MEMBER_ROLE_REACTION:
                role = get(guild.roles, id=MEMBER_ROLE_ID)
                user = get(guild.members, id=payload.user_id)
                if user is not None:
                    await user.remove_roles(role, reason=MEMBER_ROLE_REASON)
                    await log_channel.send("**Success**: Removed role <@&" + str(role.id) + "> from <@" + str(payload.user_id) + ">!")
                else:
                    await log_channel.send("**Error**: while assigning role by reaction; user is None")

        # Topic role assignment
        if payload.message_id == ROLE_ASSIGN_MESSAGE_ID:
            if payload.emoji.name in ROLES_TO_ASSIGN:
                role = get(guild.roles, id=ROLES_TO_ASSIGN[payload.emoji.name])
                user = get(guild.members, id=payload.user_id)
                if user is not None:
                    await user.remove_roles(role, reason=ROLE_ASSIGN_REASON)
                    await log_channel.send("**Success**: Removed role <@&" + str(role.id) + "> from <@" + str(payload.user_id) + ">!")
                else:
                    await log_channel.send("**Error**: while assigning ping role by reaction. User is None")

        # Ping role assignment
        if payload.message_id == PING_ROLE_ASSIGN_MESSAGE_ID:
            if payload.emoji.name in PING_ROLES_TO_ASSIGN:
                role = get(guild.roles, id=PING_ROLES_TO_ASSIGN[payload.emoji.name])
                user = get(guild.members, id=payload.user_id)
                if user is not None:
                    await user.remove_roles(role, reason=PING_ROLE_ASSIGN_REASON)
                    await log_channel.send("**Success**: Removed role <@&" + str(role.id) + "> from <@" + str(payload.user_id) + ">!")
                else:
                    await log_channel.send("**Error**: while assigning ping role by reaction. User is None.")

@client.event
async def on_message(payload):
    if payload.author == client.user:
        return
    print(payload)

print("Starting bot...")
client.run("PLACE_DISCORD_TOKEN_HERE")