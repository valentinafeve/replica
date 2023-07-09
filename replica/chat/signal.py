from replica.chat.base import ChatBase
from unidecode import unidecode
import json
import emoji


class SignalChat(ChatBase):
    def __init__(self):
        self.messages = []

    def prepare_messages(self, file_path: str, you='you'):
        with open(file_path, 'r', encoding="utf-8") as f:
            lines = f.readlines()
            message = {}

            last_from = ""
            for i, line in enumerate(lines):
                if i < 2:
                    continue
                if line.startswith("From: "):
                    message_from = line.replace("From: ", "").strip()

                    if '(' in message_from:
                        message_from = message_from.split('(')[0].strip()
                    if message_from.lower() == 'you':
                        message_from = you

                    if not (last_from == message_from):
                        if message and ('text' in message):
                            self.messages.append(message)
                        message = {
                            "from": message_from
                        }
                    last_from = message_from
                elif line.startswith("Type: "):
                    message_type = line.replace("Type: ", "").strip()
                    message["type"] = message_type
                elif line.startswith("Sent: "):
                    message_sent = line.replace("Sent: ", "").strip()
                    # TODO: Convert to datetime
                    message["sent"] = message_sent
                elif line.startswith("Received: "):
                    message_received = line.replace("Received: ", "").strip()
                    # TODO: Convert to datetime
                    message["type"] = message_received
                else:
                    message_text = emoji.demojize(line, delimiters=(':', ': '))
                    message_text = unidecode(message_text.replace('\n', '').strip())
                    if message_text and not message_text.startswith(">"):
                        last_messages = message.get("text", [])
                        last_messages.append(message_text)
                        message["text"] = last_messages
        return True
