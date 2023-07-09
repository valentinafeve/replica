import click
from replica.chat.signal import SignalChat
import json


@click.group()
def cli():
    pass


messaging_apps = {
    "signal": SignalChat
}


def generate_jsonl_file(messages, file_path="messages.jsonl"):
    with open(file_path, "w") as f:
        for i, message in enumerate(messages):
            if i < 1:
                continue
            input_prompt = ""
            # for j in range(5, 0, -1):
            message_index = i - 1
            input_prompt += '##' + messages[message_index]["from"] + '##' + ": " + '. '.join(messages[message_index]["text"])
            input_prompt += '. '

            input_prompt += '##' + messages[i]["from"] + '##'
            input_prompt += ": "
            prompt_response = {
                "prompt": input_prompt,
                "completion": ' ' + '. '.join(messages[i]["text"]) + ".",
            }
            f.write(json.dumps(prompt_response) + '\n')


@cli.command()
@click.option('--file-path', default='messages.txt', help='')
@click.option('--messaging-app', default='', help='')
@click.option('--you', default='', help="Name of the person owner of the chat. Replica will replace the messages coming from 'you' with this name")
def prepare_messages(file_path, messaging_app, you):
    chat = messaging_apps[messaging_app]()
    chat.prepare_messages(file_path, you)
    generate_jsonl_file(chat.messages, "messages.jsonl")


if __name__ == '__main__':
    cli()
