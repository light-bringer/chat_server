import datetime
import typing

import exceptions


class Message:
    def __init__(self, group_id: int, sender_id: int, body: str):
        self.group_id: int = group_id
        self.sender: int = sender_id
        self.timestamp: datetime.datetime = datetime.datetime.now()
        self.message_body: str = body

    def __str__(self):
        message_str = f"""sender: {self.sender}, time: {self.timestamp}, message: {self.message_body}"""
        return message_str

    def __repr__(self):
        return self.__str__()


class Group:
    def __init__(self, name: str, participants: typing.List[int]):
        self.name: str = name
        if len(participants) < 2:
            raise exceptions.IncorrectParticipantsException
        self.participants: set = set(participants)
        self.messages = []

    def isPrivateConversation(self):
        if len(self.participants) == 2:
            return True
        return False

    def get_participants(self):
        return self.participants

    def get_name(self):
        return self.name

    def add_message(self, group_id: int, sender_id: int, body: str):
        if sender_id not in self.participants:
            exceptions.IncorrectParticipantForGroup
        self.messages.append(Message(group_id, sender_id, body))

    def get_conversation(self) -> typing.List[Message]:
        return self.messages


class Groups:
    def __init__(self):
        self.autoinc = 0
        self.groups: typing.Dict[int, Group] = {}

    def add_group(self, group_name: str, participants: typing.List[int]):
        self.autoinc += 1
        u_id = self.autoinc
        self.groups[u_id] = Group(group_name, participants)

    def get_group_participants(self, group_id):
        return self.groups[group_id].get_participants()

    def get_groups_joined(self, user_id: int) -> typing.List[int]:
        groups = []
        for group_id, group in self.groups.items():
            if user_id in group.get_participants():
                groups.append(group_id)

        return groups

    def get_conversation(self, user_id: int, group_id: int) -> typing.Optional[typing.List[Message]]:
        if group_id not in self.groups:
            print('group_id not present in group')
            return None
        if user_id not in self.groups[group_id].get_participants():
            print('User not present in group')
            return None
        return self.groups[group_id].get_conversation()

    def send_message(self, group_id: int, sender_id: int, body: str):
        try:
            self.groups[group_id].add_message(group_id, sender_id, body)
            return True
        except exceptions.IncorrectParticipantForGroup:
            return False

