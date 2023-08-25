import emoji
import re
import logging


class ChatBase:
    def __init__(self):
        self.messages = []

    def read_messages(self, file_path: str):
        pass

    def replace_text_with_captionings(self, captionings_path: str):
        pass

    def replace_text_with_transcriptions(self):
        pass
