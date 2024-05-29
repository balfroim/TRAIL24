import pytest
from models.users.user_registry import UserRegistry
from models.users.user_row import UserRow
from models.users.user_mapping_row import UserMappingRow

class TestUserRegistry:
    def test_find_by_uid(self):
        users = [UserRow({'uid': 1, "gender": "F", 'age': "20"})]
        user_mapping_rows = [UserMappingRow({'rating_id': 1, 'new_id': 1})]
        user_manager = UserRegistry(users, user_mapping_rows)
        user = user_manager.find_by_uid(1)
        assert user.eid == 1
        assert user.uid == 1
        assert user.gender == 'F'
        assert user.age == "20"
