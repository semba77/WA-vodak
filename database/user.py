from database.baseTable import BaseTable, NoResultsFoundException, ConnectionLost
from datetime import date
import pymysql
import os, shutil

class User(BaseTable):
    table_name = "user"
    select_parameters = ["id","username","password", "finish", "canSwim"]

    def __init__(self, database_tuple=None):
        self.id: int = database_tuple[0]
        self.username: str = database_tuple[1]
        self.password: str = database_tuple[2]
        self.finish: bool = bool(database_tuple[3])
        self.can_swim: bool = bool(database_tuple[4])
        
    def __str__(self) -> str:
        return self.username
        
    @staticmethod
    def read_one_username(conn: pymysql.Connect, username: str):
        try:
            return User.read_one_by_atributes(conn, username=username)
        except ConnectionLost as e:
            print(e)
            print("nastala chyba")
        except NoResultsFoundException as e:
            raise e
        except Exception as e:
            print(e)
