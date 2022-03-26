from __future__ import annotations

from . import (
    do_approve_action,
    approved_members,
    CHANNEL,
    ADMIN_ROLE_ID
)

import hikari


async def on_member_create(event: hikari.MemberCreateEvent) -> None:
    if event.member.id not in approved_members:
        # This user never got approved - they've gone rogue!
        await event.member.ban()


async def on_interaction(event: hikari.InteractionCreateEvent) -> None:
    inter = event.interaction

    if not isinstance(inter, hikari.ComponentInteraction):
        # This interaction isn't related to buttons
        return None

    if inter.channel_id != CHANNEL:
        # This isn't the channel we send our requests to
        return None

    if inter.member and ADMIN_ROLE_ID not in inter.member.role_ids:
        # This user cant approve or deny other members
        return None

    try:
        userid, action, access = inter.custom_id.split("-")
    except ValueError:
        # This custom id does not match our format
        return None

    if access != "access":
        # This must be related to some other interactions, bail!
        return None

    if action == "deny":
        # Update the embed to denied
        embed = inter.message.embeds[0]
        embed.add_field("Status", f"```DENIED by {inter.user}```")

        # Create our response to the interaction
        await inter.create_initial_response(
            hikari.ResponseType.MESSAGE_UPDATE, embed, components=[]
        )

    elif action == "approve":
        # We want to approve them - someone clicked the approve button
        await do_approve_action(event.app, inter, int(userid))
