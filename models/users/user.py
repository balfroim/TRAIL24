from models.nodes.fact import Fact
from models.nodes.node import Node
from models.users.user_row import UserRow
from models.users.user_mapping_row import UserMappingRow
from dataclasses import dataclass

@dataclass(frozen=True)
class User(Node):
    uid: int
    gender: str
    age: str

    @staticmethod
    def from_rows(user_row: UserRow, user_mapping_row: UserMappingRow):
        assert user_row.uid == user_mapping_row.rating_id
        return User(
            uid=user_row.uid,
            eid=user_mapping_row.new_id,
            gender=user_row.gender,
            age=user_row.age
        )
    
    def __str__(self):
        return f"User{self.eid}"
    
    def facts(self):
        return [
            Fact("gender", (str(self), str(self.gender))),
            Fact("age", (str(self), str(self.age)))
        ]
    