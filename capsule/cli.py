"""This module defines the command line utility to process user input."""

import click
import zipfile
import os
import toml
import datetime as dt
import time

from itertools import chain
from utils import model
from utils.model import get_paths_and_callbacks


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def cli():
    """Snapshot your Nextcloud calendars and contacts."""


@cli.command(help="Snapshot calendars and contacts.")
@click.option(
    "-c",
    "--config",
    default="config.toml",
    type=click.Path(file_okay=True, dir_okay=False, resolve_path=True),
    show_default=True,
    help="Path of the config file.",
)
@click.option(
    "-a",
    "--archive",
    default="archive.zip",
    type=click.Path(file_okay=True, dir_okay=False, resolve_path=True),
    show_default=True,
    help="Path of archive to snapshot to.",
)
def snapshot(config, archive):
    """
    Snapshot calendars and contacts.

    Parameters
    ----------
    config : path
        Configuration file specifying what to snapshot
    archive : path 
        Path of the zip archive to snapshot into
    """

    click.echo("Snapshotting calendars/contacts")

    # Open the configuration file and define all the servers via the configuration file.
    with open(config, "r") as file:
        servers = [
            model.Server.from_cfg({server_name: server_cfg})
            for server_name, server_cfg in toml.load(file).items()
        ]

    # Get the paths and callbacks to download and archive the calendars/callbacks.
    paths_and_callbacks = get_paths_and_callbacks(servers)

    # Open the archive and log a message.
    click.echo(f"Opening archive '{click.format_filename(archive)}'")
    with zipfile.ZipFile(archive, "a", compression=zipfile.ZIP_DEFLATED) as zip:

        for path, callback in paths_and_callbacks:
            click.echo(f"Archiving to root: '{click.format_filename(path)}'")
            # For each path and callback we create a zip file containing information
            # which was returned via the callback.
            zip.writestr(path, callback.run())

    click.echo(click.style("Success!", fg="green"))
