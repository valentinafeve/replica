import emoji
import re
from replica.settings import URL_PATTERN
import json
from typing import Dict


def emojize(text):
    return emoji.demojize(text, delimiters=(':', ': '))


def replace_words_in_message(message: Dict):
    replacements = json.load(open("replacements.json", "r"))
    for replacement_key, replacement_dict in replacements.items():
        message_item = message[replacement_key]
        if isinstance(message_item, list):
            for i, message_item_i in enumerate(message_item):
                for replace_from, replace_to in replacement_dict.items():
                    message_item_i = replace_words_keeping_case(message_item_i, replace_from, replace_to)
                    message[replacement_key][i] = message_item_i
        if isinstance(message_item, str):
            for replace_from, replace_to in replacement_dict.items():
                message[replacement_key] = replace_words_keeping_case(message[replacement_key], replace_from, replace_to)
    return message


def remove_urls(text: str):
    match = re.search(URL_PATTERN, text)
    if match:
        text = text.replace(match.string, '')
    return text


def replace_words_keeping_case(text: str, replace_from: str, replace_to: str):
    i = 0
    while i < len(text):
        find_i = text.lower().find(replace_from.lower(), i)
        if find_i != -1:
            i = find_i + len(replace_from)
        if find_i == -1:
            break

        new_word = ''

        last_case = 'lower'
        min_len = min(len(replace_to), len(replace_from))
        for j in range(min_len):
            if text[find_i + j].islower():
                last_case = 'lower'
                new_word += replace_to[j].lower()
            elif text[find_i + j].isupper():
                last_case = 'upper'
                new_word += replace_to[j].upper()
            else:
                new_word += replace_to[j].lower() if last_case == 'lower' else replace_to[j].upper()
        new_word += replace_to[min_len:].lower() if last_case == 'lower' else replace_to[min_len:].upper()
        text = text[:find_i] + new_word + text[find_i+len(replace_from):]

    return text
