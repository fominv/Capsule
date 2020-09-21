# Capsule

Capsule is a simple command line utility to snapshot all calendars and contacts on a Nextcloud instance.

## Installation

To install Capsule use the following steps and make sure that you have at least Python version 3.7.

```bash
# Clone the repository to your desired directory.
git clone https://github.com/fominv/Capsule && cd Capsule

# Install the poetry dependency manager for python.
pip3 install poetry

# Install all dependencies.
poetry install --no-dev
```

## Usage

Define your servers, users, calendars and contacts to snapshot in a toml file with the following structure.

```toml
["<SERVER>"."<USER>"]
password = "<PASSWORD>"
calendar_names = ["<CALENDAR_NAME>", "..."]
ignore_contacts = false
```

You can define multiple servers, users and calendars. The name of a calendar can be found on your Nextcloud instance while hovering over the download button for some particular calendar.

After defining your _config.toml_ you can snapshot all specified calendars and contacts with:

```bash
poetry run python capsule snapshot
```

For any additional information please consult the help messages with:

```bash
poetry run python capsule -h
poetry run python capsule snapshot -h
```

## Security

Make sure that your Nextcloud instance has a valid SSL certificate. Nextcloud instances without one are not supported as otherwise all users and passwords would be transmitted in clear text.

Additionally, make sure to secure the configuration file as there are passwords embedded inside. A possible way is to create a system user specifically for running this application and lock down file permissions.
