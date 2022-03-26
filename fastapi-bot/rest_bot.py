from __future__ import annotations

import os
from .listeners import on_interaction, on_member_create

import hikari


bot = hikari.RESTBot(token=os.environ["TOKEN"], token_type=hikari.TokenType.BOT)

bot.set_listener(hikari.InteractionCreateEvent, on_interaction)
bot.set_listener(hikari.MemberCreateEvent, on_member_create)
