from typing import List

from models.users.user import User
from models.users.user_factory import UserFactory
from models.users.user_mapping_row import UserMappingRow
from models.users.user_row import UserRow


class UserRegistry:
    def __init__(self, users: List[UserRow], user_mapping_rows: List[UserMappingRow]):
        self.users: List[User] = UserFactory().create_users(users, user_mapping_rows)
        self.__max_uid: int = max([user.uid for user in self.users])

    def find_by_uid(self, user_id: int) -> User:
        return next(user for user in self.users if user.uid == user_id)
    
    def find_by_eid(self, entity_id: int) -> User:
        return next(user for user in self.users if user.eid == entity_id)
    
    def add_user(self, user_data: User) -> User:
        new_id = self.__max_uid + 1
        new_user = User(
            eid=-1, # TODO temporary solution, need to deal with entity ids in a cleaner way
            uid=new_id,
            gender=user_data.gender,
            age=user_data.age
        )
        self.users.append(new_user)
        return new_user
