"""
Provide implementation of the command line interface for pattern recognition by interacting with the server.
"""
import click


@click.group()
@click.version_option()
@click.help_option()
def cli():
    """
    Command-line interface to interact with server.
    """
    pass
