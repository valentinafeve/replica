from chat.base import ChatBase


class SignalChat(ChatBase):
    def __init__(self):
        self.messages = []

    def prepare_messages(self, file_path: str):
        with open(file_path, 'r') as f:
            lines = f.readlines()
            message = {}

            last_from = ""
            for line in lines:
                if line.startswith("From: "):
                    message_from = line.replace("From: ", "")
                    if not (last_from == message_from):
                        self.messages.append(message)
                        message = {
                            "from": message_from
                        }
                elif line.startswith("Type: "):
                    message_type = line.replace("Type: ", "")
                    message["type"] = message_type
                elif line.startswith("Sent: "):
                    message_sent = line.replace("Sent: ", "")
                    # TODO: Convert to datetime
                    message["sent"] = message_sent
                elif line.startswith("Received: "):
                    message_received = line.replace("Received: ", "")
                    # TODO: Convert to datetime
                    message["type"] = message_received
                else:
                    message_text = message.get("text", "") + line
                    message["text"] = message_text
        return True
