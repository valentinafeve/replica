import json
from datetime import datetime

from unidecode import unidecode
import os
from collections import OrderedDict

from replica.chat.base import ChatBase
from replica.chat.utils import replace_words_in_message, emojize, remove_urls
from typing import List, Dict


class SignalChat(ChatBase):
    def __init__(self):
        self.messages = []

    def replace_text_with_captionings(self, captionings_path: str):
        files_without_name_i = 0
        attachments_read = []
        captionings = json.load(open(captionings_path, "r"))
        for message_i, message in enumerate(self.messages):

            for i, text in enumerate(message['text']):
                if 'Attachment' in text:
                    attachment_name = text.split('(')[0].replace('Attachment: ', '').strip()
                    attachment_type = text.split('(')[1].split(')')[0].split(',')[0].strip()

                    captioning_text_type = ''

                    if attachment_type == 'image/jpeg':
                        captioning_text_type = 'Image of'
                    elif attachment_type == 'video/mp4':
                        captioning_text_type = 'Video of'

                    if attachment_name == 'no filename':
                        unnamed_attachment_name = f'attachment-{message["datetime"].strftime("%Y")}-{message["datetime"].strftime("%m")}-{message["datetime"].strftime("%d")}-{message["datetime"].strftime("%H")}-{message["datetime"].strftime("%M")}'
                        captionings_filtered = {k: v for k, v in captionings.items() if k.startswith(unnamed_attachment_name)}
                        captionings_filtered = OrderedDict(sorted(captionings_filtered.items()))

                        image_was_captioned = False
                        for k, v in captionings_filtered.items():
                            if k not in attachments_read:
                                self.messages[message_i]['text'][i] = self.messages[message_i]['text'][i].replace('no filename', f'{captioning_text_type} {v}')
                                attachments_read.append(k)
                                image_was_captioned = True
                        if not image_was_captioned:
                            print(unnamed_attachment_name)
                    else:
                        self.messages[message_i]['text'][i] = captionings[attachment_name]
        return self.messages

    def replace_text_with_transcriptions(self, transcriptions_path):
        files_without_name_i = 0
        attachments_read = []
        captionings = json.load(open(transcriptions_path, "r"))
        for message_i, message in enumerate(self.messages):

            for i, text in enumerate(message['text']):
                if 'Attachment' in text:
                    attachment_name = text.split('(')[0].replace('Attachment: ', '').strip()
                    attachment_type = text.split('(')[1].split(')')[0].split(',')[0].strip()

                    captioning_text_type = ''

                    if attachment_type == 'image/jpeg':
                        captioning_text_type = 'Image of'
                    elif attachment_type == 'video/mp4':
                        captioning_text_type = 'Video of'
                    else:
                        print(attachment_type)


                    if attachment_name == 'no filename':
                        unnamed_attachment_name = f'attachment-{message["datetime"].strftime("%Y")}-{message["datetime"].strftime("%m")}-{message["datetime"].strftime("%d")}-{message["datetime"].strftime("%H")}-{message["datetime"].strftime("%M")}'
                        captionings_filtered = {k: v for k, v in captionings.items() if k.startswith(unnamed_attachment_name)}
                        captionings_filtered = OrderedDict(sorted(captionings_filtered.items()))

                        image_was_captioned = False
                        for k, v in captionings_filtered.items():
                            if k not in attachments_read:
                                self.messages[message_i]['text'][i] = self.messages[message_i]['text'][i].replace('no filename', f'{captioning_text_type} {v}')
                                attachments_read.append(k)
                                image_was_captioned = True
                        if not image_was_captioned:
                            print(unnamed_attachment_name)
                    else:
                        self.messages[message_i]['text'][i] = captionings[attachment_name]
        return self.messages

    def read_messages(self, file_path: str) -> List[Dict]:
        """
        Given a path containing a file of messages exported from Signal, generates a list of dictionaries with basic information about a message, each message contains.
        {
            "from": str. Name of the sender of the message.
            "sent": datetime. Datetime when the message was sent.
            "text": list. List of strings where each string is a single text message.
        }

        :param file_path: Path of the file where the signal messages are located.
        :return: List of a dictionary containing basic information about every message.
        """
        with open(file_path, 'r', encoding="utf-8") as f:
            lines = f.readlines()
            # Current message
            message = {}

            # Last person who has sent the message
            last_from = ""

            # Iterate over every line
            for i, line in enumerate(lines):

                # Ignore the headers
                if i < 2:
                    continue

                # If the line contains From:, it means the following lines are a new message
                if line.startswith("From: "):
                    message_from = line.replace("From: ", "").strip()

                    if '(' in message_from:
                        message_from = message_from.split('(')[0].strip()

                    if not (last_from == message_from):
                        if message and ('text' in message):
                            message = replace_words_in_message(message)
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
                    datetime_format = "%a, %d %b %Y %H:%M:%S %z"
                    dt = datetime.strptime(message_sent, datetime_format)
                    message["datetime"] = dt
                elif line.startswith("Received: "):
                    message_received = line.replace("Received: ", "").strip()
                    datetime_format = "%a, %d %b %Y %H:%M:%S %z"
                    dt = datetime.strptime(message_received, datetime_format)
                    message["datetime"] = dt
                else:
                    message_text = unidecode(line.replace('\n', '').strip())
                    message_text = emojize(message_text)
                    message_text = remove_urls(message_text)
                    message_text = message_text.strip()
                    if message_text and not message_text.startswith(">"):
                        last_messages = message.get("text", [])
                        last_messages.append(message_text)
                        message["text"] = last_messages
        return self.messages
