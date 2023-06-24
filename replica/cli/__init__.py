import click
from chat.signal import SignalChat


@click.group()
def cli():
    pass


messaging_apps = {
    "signal": SignalChat
}


@cli.command()
@click.option('--file-path', default='messages.txt', help='')
@click.option('--messaging-app', default='', help='')
def prepare_messages(file_path, messaging_app):
    chat = messaging_apps[messaging_app]()
    chat.prepare_messages(file_path)
