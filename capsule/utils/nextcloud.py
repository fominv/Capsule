"""This module defines utility functions to interface with Nextcloud."""

import requests
import click

from requests.auth import HTTPBasicAuth


def get_calendar(host, user, password, calendar):
    """
    Download a calendar.

    Parameters
    ----------
    host : str
        Domain or IP of the server
    user : str
        Name of the user
    password : str
        Password of the user
    calendar : str
        Name of the calendar

    Raises
    ------
    HttpError
        Whenever a request response indicates an error
    """

    # Define the url corresponding to the export button in Nextcloud.
    url = f"https://{host}/remote.php/dav/calendars/{user}/{calendar}/?export"

    # Perform the request and raise any bad codes.
    response = requests.get(url, auth=HTTPBasicAuth(user, password))
    response.raise_for_status()

    return response.text


def get_contacts(host, user, password):
    """
    Download contacts of a user.

    Parameters
    ----------
    host : str
        Domain or IP of the server
    user : str
        Name of the user
    password : str
        Password of the user

    Raises
    ------
    HttpError
        Whenever a request response indicates an error
    """

    # Define the url corresponding to the export button in Nextcloud.
    url = f"https://{host}/remote.php/dav/addressbooks/users/{user}/contacts/?export"

    # Perform the request and raise any bad codes.
    response = requests.get(url, auth=HTTPBasicAuth(user, password))
    response.raise_for_status()

    return response.text
