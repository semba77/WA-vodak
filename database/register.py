from database.baseTable import BaseTable
from typing import Union

class Register(BaseTable):
    table_name='register'
    select_parameters=['id', 'user_id', 'is_swimming', 'user2_id', 'user2_decision']
    
    def __init__(self, database_tuple=None):
        self.id: int = database_tuple[0]
        self.user_id: int = database_tuple[1]
        self.is_swimming: bool = bool(database_tuple[2])
        self.user2_id: int = database_tuple[3]
        self.user2_decision: Union[bool, None] = database_tuple[4]
        
    def __dict__(self) -> str:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "is_swimming": self.is_swimming,
            "user2_id": self.user2_id,
            "user2_decision": self.user2_decision
        }