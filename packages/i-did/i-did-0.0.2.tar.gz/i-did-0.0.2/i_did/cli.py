"""Tool to keep track of what you did today."""
import datetime
import json
from pathlib import Path

import click

EDITOR = "vim --cmd ':set tw=79'"
STORE_DIR = Path("~/.i-did").expanduser()

MARKER = (
    "# ------------------------ >8 ------------------------\n"
    "# Do not delete the line above: everything below it will be discarded\n"
    "# Type your message above the line\n"
)


def remove_extra_newlines(message):
    """Limit the number of newlines in a message to 2."""
    while "\n\n\n" in message:
        message = message.replace("\n\n\n", "\n\n")
    return message


@click.group()
def cli():
    """Keep track of what you did today."""
    # Make sure the directory for storing files exists.
    if not STORE_DIR.is_dir():
        assert (
            not STORE_DIR.exists()
        ), f"{STORE_DIR} already exists but is not a directory"
        STORE_DIR.mkdir()


@cli.command()
@click.option("--message", "-m", nargs=1)
def new(message):
    """Add an item to the list of things you've done.

    If no message is given, open vim to get a new message.
    """
    # Get the message to add.
    if not message:
        message = click.edit("\n\n" + MARKER, editor=EDITOR)
        if message is not None:
            message = message.split(MARKER, 1)[0].rstrip("\n")
        if not message:
            click.echo("No message to add", err=True)
            return

    # Create a file for today if it does not exist.
    today = datetime.date.today()
    today_file = STORE_DIR.joinpath(f"{today.isoformat()}.json")
    if not today_file.exists():
        with open(today_file, "w") as fd:
            json.dump({"items": []}, fd)

    # Add the item to today's file
    with open(today_file, "r") as fd:
        today_data = json.loads(fd.read())
    new_item = {"message": message, "time": datetime.datetime.now().isoformat()}
    today_data["items"].append(new_item)
    with open(today_file, "w") as fd:
        json.dump(today_data, fd)
    click.echo("New item added.", err=True)


@cli.command()
@click.option("-v", "--verbose", count=True)
def show(verbose):
    """Show what you've already done this week."""
    today = datetime.date.today()

    # Get range of days to show.
    num_days = 7
    days = (today - datetime.timedelta(days=n) for n in range(num_days))

    # Show data for each day.
    for day in days:
        # Get data from file.
        day_file = STORE_DIR.joinpath(f"{day.isoformat()}.json")
        if not day_file.exists():
            continue
        else:
            with open(day_file, "r") as fd:
                data = json.loads(fd.read())

        # Format data.
        day_str = day.strftime("%A %B %d, %Y")
        output = f"\n{day_str}\n{'-'*len(day_str)}\n\n"
        data["items"].sort(key=lambda item: item["time"])
        for item in data["items"]:
            time = datetime.datetime.fromisoformat(item["time"])
            time_str = click.style(time.strftime("%H:%M"), fg="yellow")
            message = remove_extra_newlines(item["message"])
            message_header = message.split("\n", 1)[0]
            output += f"{time_str}  {message_header}" + "\n"
            if verbose:
                message_body = message.split("\n")[1:]
                for line in message_body:
                    output += f"           {line}\n"
                if message_body:
                    output += "\n"

        # Show data.
        click.echo(output)
