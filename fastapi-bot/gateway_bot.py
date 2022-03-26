from __future__ import annotations

import os
from .listeners import on_interaction, on_member_create

import hikari


bot = hikari.GatewayBot(
    token=os.environ["TOKEN"],
    cache_settings=None,
    intents=hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.GUILD_MEMBERS,
)

bot.subscribe(hikari.InteractionCreateEvent, on_interaction)
bot.subscribe(hikari.MemberCreateEvent, on_member_create)
