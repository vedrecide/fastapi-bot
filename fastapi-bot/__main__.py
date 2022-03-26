from __future__ import annotations

import datetime
import argparse

from . import pending_requests, CHANNEL
from . import gateway_bot
from . import rest_bot

import hikari
import uvicorn
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

# Create a new Argparse instance
cli_parser = argparse.ArgumentParser(
    prog="fastapi-bot",
    description="REST/Gateway Bot with Hikari"
)

cli_parser.add_argument("--gateway", action="store_true")
cli_parser.add_argument("--rest",  action="store_true")

args = cli_parser.parse_args()

# Create a new FastAPI instance
app = FastAPI()

# Mount the static directory to the app
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create the Hikari GatewayBot or RESTBot instance via the CLI
bot = None

if args.rest == True:
    bot = rest_bot.bot
else:
    bot = gateway_bot.bot


# Starts the bot when the server starts
@app.on_event("startup")
async def on_startup() -> None:
    await bot.start()


# Closes the bot when the server closes
@app.on_event("shutdown")
async def on_shutdown() -> None:
    await bot.close()


# Returns the index.html page
@app.get("/")
async def index() -> FileResponse:
    return FileResponse("static/index.html")


# Returns the oops.html page
@app.get("/oops")
async def oops() -> FileResponse:
    return FileResponse("static/oops.html")


# Returns the thanks.html page
@app.get("/thanks")
async def thanks() -> FileResponse:
    return FileResponse("static/thanks.html")


# Validates an incoming submission on the index page form
@app.post("/access/request")
async def access_request(req: Request) -> RedirectResponse:
    # Extract form data into variables
    form_data = await req.form()
    userid: int = int(form_data.get("userid"))
    github_link: str = form_data.get("github-link")

    if userid in pending_requests:
        # This user already submitted their info
        return RedirectResponse(
            "/oops?You already have a request pending.", status_code=302
        )

    # This user is now pending
    pending_requests.append(userid)

    # Build an action row with an approve and deny buttons
    action_row = (
        bot.rest.build_action_row()
        .add_button(hikari.ButtonStyle.PRIMARY, f"{userid}-approve-access")
        .set_label("Approve")
        .add_to_container()
        .add_button(hikari.ButtonStyle.DANGER, f"{userid}-deny-access")
        .set_label("Deny")
        .add_to_container()
    )

    # Build an embed to send to the channel
    embed = (
        hikari.Embed(
            title="New application to join",
            description=f"User: <@{userid}>",
            timestamp=datetime.datetime.now(datetime.timezone.utc),
        )
        .add_field("User ID", f"```{userid}```")
        .add_field("Github Link:", github_link)
        .add_field("Status", "```PENDING```")
    )

    # Send the request to join embed to the channel
    await bot.rest.create_message(CHANNEL, embed, component=action_row)

    # Redirect the user on the site to the thanks.html page
    return RedirectResponse("/thanks", status_code=302)


# Run the webserver
uvicorn.run(app, host="0.0.0.0")
