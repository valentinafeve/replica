import click
from replica.chat.signal import SignalChat
from replica.captioner import caption_files_in_folder
import json


@click.group()
def cli():
    pass


messaging_apps = {
    "signal": SignalChat
}


def generate_prompt_completions_file(messages, file_path="messages.jsonl"):
    with open(file_path, "w") as f:
        for i, message in enumerate(messages):
            if i < 1:
                continue
            input_prompt = ""
            message_index = i - 1
            message_date_past = messages[message_index]["datetime"].strftime('%d-%m-%Y %H:%M:%S')
            message_date_current = messages[i]["datetime"].strftime('%d-%m-%Y %H:%M:%S')
            input_prompt += '##' + messages[message_index]["from"] + ' at ' + message_date_past + '##' + ": " + '. '.join(messages[message_index]["text"])
            input_prompt += '. '

            input_prompt += '##' + messages[i]["from"] + ' at ' + message_date_current + '##' + ": "
            input_prompt += ": "
            prompt_response = {
                "prompt": input_prompt,
                "completion": ' ' + '. '.join(messages[i]["text"]) + ".",
            }
            f.write(json.dumps(prompt_response) + '\n')


@cli.command()
@click.option('--file-path', default='messages.txt', help='')
@click.option('--messaging-app', default='', help='')
def prepare_messages(file_path, messaging_app):
    chat = messaging_apps[messaging_app]()
    chat.read_messages(file_path)
    generate_prompt_completions_file(chat.messages, "messages.jsonl")


@cli.command()
@click.option('--folder-path', default='attachments', help='')
def caption_messages(folder_path):
    captionings = caption_files_in_folder(folder_path)
    f = open('captionings.json', 'w')
    json.dump(captionings, f)


if __name__ == '__main__':
    cli()
