from typing import List

from models.users.user import User
from models.users.user_factory import UserFactory
from models.users.user_mapping_row import UserMappingRow
from models.users.user_row import UserRow


class UserRegistry:
    def __init__(self, users: List[UserRow], user_mapping_rows: List[UserMappingRow]):
        self.users: List[User] = UserFactory().create_users(users, user_mapping_rows)

    def find_by_uid(self, user_id: int) -> User:
        return next(user for user in self.users if user.uid == user_id)
    
    def find_by_eid(self, entity_id: int) -> User:
        return next(user for user in self.users if user.eid == entity_id)
    
    
