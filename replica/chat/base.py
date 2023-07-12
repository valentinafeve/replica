import emoji
import re
import logging


class ChatBase:
    def __init__(self):
        self.messages = []

    def read_messages(self, file_path: str):
        pass
