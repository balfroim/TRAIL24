from typing import List

from models.users.user import User
from models.users.user_mapping_row import UserMappingRow
from models.users.user_row import UserRow
from models.mapping_factory import MappingFactory

class UserFactory(MappingFactory['User', 'UserMappingRow', 'UserRow']):
    @staticmethod
    def create_users(user_rows: List['UserRow'], user_mapping_rows: List['UserMappingRow']) -> List['User']:
        return MappingFactory.create_items(user_rows, user_mapping_rows, User, 'uid', 'rating_id')