from __future__ import annotations

import typing as t
import datetime

from .constants import (
    approved_members,
    pending_requests,
    CHANNEL
)

import hikari


# Approves a user to join the discord
# Creates an invite link with 1 use limit for them
async def do_approve_action(
    bot: t.Union[hikari.GatewayBotAware, hikari.RESTBotAware],
    inter: hikari.ComponentInteraction,
    userid: int,
) -> None:
    # Create a new invite for this user to use
    invite = await bot.rest.create_invite(
        # This is the channel where the invite leads to
        # It should probably be some welcome or rules channel
        CHANNEL,
        max_age=datetime.timedelta(days=7),
        max_uses=1,
        reason=f"Approved by {inter.member}",
    )

    # Update the embed to approved
    embed = inter.message.embeds[0]
    embed.add_field("Status", f"```APPROVED by {inter.user}```")

    try:
        # Try to DM the user
        dm = await bot.rest.create_dm_channel(userid)
        await dm.send(
            "Hi were happy to inform you that you application has been accepted!"
            f" You, and only you, can join with the following link\n{invite}"
        )
    except hikari.ForbiddenError:
        # This can fail if the user has DM's closed
        # Make the embed red since we couldn't DM the user
        # Add the users invite to this embed
        embed.color = hikari.Color(0xF00707)
        embed.add_field("DM failed", str(invite))

    # Create our response to the interaction
    await inter.create_initial_response(
        hikari.ResponseType.MESSAGE_UPDATE, embed, components=[]
    )

    # Remove the user from pending and add to approved
    pending_requests.remove(userid)
    approved_members.append(userid)
