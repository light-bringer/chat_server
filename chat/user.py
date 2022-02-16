import typing

class User:
    def __init__(self, name: str):
        self.name: str = name

class Users:
    def __init__(self):
        self.autoinc = 0
        self.users: typing.Dict[int, User] = {}

    def add_user(self, user_name: str) -> int:
        self.autoinc += 1
        u_id = self.autoinc
        self.users[u_id] = User(user_name)
        return u_id


    def get_all_users(self):
        users_with_ids = []
        for u_id, user in self.users.items():
            users_with_ids.append((u_id, user.name))
        return users_with_ids
