"""This module defines the data model of the parsed configuration."""

import os
import constants as const

from utils.nextcloud import get_calendar, get_contacts
from utils.callback import Callback


class Calendar:
    """
    Container class for calendar meta data.

    Attributes
    ----------
    name : str
        Name of the calendar
    user : str
        Name of the user
    """

    def __init__(self, name, user=None):
        """Initialize the class."""
        self.name = name
        self.user = user

    def get_path(self):
        """Compute the file path in the archive."""
        return os.path.join(
            self.user.get_path(),
            self.name,
            (
                f"{const.TIMESTAMP.strftime(const.TIMESTAMP_FORMAT)}"
                f"_{self.user.name}_{self.name}.cal"
            ),
        )


class Contacts:
    """
    Container class for contact meta data.

    Attributes
    ----------
    ignore : bool
        Flag specifying if contacts should be ignored on snapshot
    user : str
        Name of the user
    """

    def __init__(self, ignore=False, user=None):
        """Initialize the class."""
        self.ignore = ignore
        self.user = user

    def get_path(self):
        """Compute the file path in the archive."""
        return os.path.join(
            self.user.get_path(),
            "contacts",
            (
                f"{const.TIMESTAMP.strftime(const.TIMESTAMP_FORMAT)}"
                f"_{self.user.name}_contacts.vcf"
            ),
        )


class User:
    """
    Container class for user meta data.

    Attributes
    ----------
    name : str
        Name of the user
    password : str
        Password of the user
    server : Server object
        Server of the user
    calendars : list of Calendar objects
        All calendars of the user
    contacts : Contact object
        Contacts of the user
    """

    def __init__(
        self, name, password, server=None, calendar_names=None, ignore_contacts=False
    ):
        """Initialize the class."""
        self.name = name
        self.password = password
        self.server = server

        # Set 'self.calendars' to an empty list if nothing was passed.
        self.calendars = []
        if calendar_names is None:
            calendar_names = []

        for calendar_name in calendar_names:
            self.calendars.append(Calendar(calendar_name, user=self))

        self.contacts = Contacts(ignore=ignore_contacts, user=self)

    @classmethod
    def from_cfg(self, cfg, server=None):
        """Initialize from a configuration dictionary."""
        user_name = next(iter(cfg.keys()))
        return self(user_name, server=server, **cfg[user_name])

    def get_path(self):
        """Compute the file path in the archive."""
        return os.path.join(self.server.get_path(), self.name)


class Server:
    """
    Container class for server meta data.

    Attributes
    ----------
    host : str
        Domain or IP of the server
    users : list of User objects
        Users of the server
    """

    def __init__(self, host, users=None):
        """Initialize the class."""
        self.host = host

        # Set 'self.users' to an empty list if nothing was passed.
        if users is None:
            users = []
        self.users = users

    @classmethod
    def from_cfg(self, cfg):
        """Initialize from a configuration dictionary."""
        # Set the server as one of the top level dictionary keys.
        # NOTE: If multiple top level keys are present all other keys are ignored.
        server = self(next(iter(cfg.keys())))
        # Initialize all users individually.
        for user_name, user_cfg in cfg[server.host].items():
            server.users.append(User.from_cfg({user_name: user_cfg}, server=server))

        return server

    def get_path(self):
        """Compute the file path in the archive."""
        return self.host.replace(".", "_")


def get_paths_and_callbacks(servers):
    """
    Compute zip archive paths and define callbacks for Nextcloud downloads.

    Parameters
    ----------
    servers : list of Server objects
        List of servers to consider.
    """

    # Build a list containing tuples of zip archive paths and callbacks.
    paths_and_callbacks = []
    for server in servers:
        for user in server.users:
            # Include all specified calendars.
            for calendar in user.calendars:
                paths_and_callbacks.append(
                    (
                        calendar.get_path(),
                        Callback(
                            get_calendar,
                            server.host,
                            user.name,
                            user.password,
                            calendar.name,
                        ),
                    )
                )
            # Include contacts only if not ignored. 
            if not user.contacts.ignore:
                paths_and_callbacks.append(
                    (
                        user.contacts.get_path(),
                        Callback(get_contacts, server.host, user.name, user.password),
                    )
                )

    return paths_and_callbacks
