import pymysql
import re

class BaseTable:
    table_name = None
    select_parameters = []

    def __init__(self, database_tuple=None):
        pass

    @classmethod
    def create(cls, conn: pymysql.connect, **kwargs):
        """
        class metoda, která vytváří instanci do tabulky

        :param cls: třída, která volá metodu
        :param conn: připojení k MySQL databázi
        :param kwargs: atributy a hodnoty
        :return: id vytvořené instance
        """
        with conn.cursor() as cursor:
            try:
                column_names = ', '.join(kwargs.keys())
                placeholders = ', '.join(['%s'] * len(kwargs))
                query = f'INSERT INTO {cls.table_name} ({column_names}) VALUES ({placeholders})'
                print(query, '==>', kwargs.values())
                values = tuple(kwargs.values())
                cursor.execute(query, values)
                conn.commit()
                return cursor.lastrowid
            except pymysql.IntegrityError as e:
                print(e)
                conn.rollback()
                errno, message = e.args
                if errno == 1062:
                    pattern = r"\'(\d+)\'|'(\w+)_UNIQUE'"
                    match = re.findall(pattern, message)
                    raise UniqueAttributeException(cls.table_name, match[1][1], match[0][0])
            except pymysql.OperationalError as e:
                if e.args[0] == 2013:
                    raise ConnectionLost()
                raise e
            except BaseException as e:
                print(e)

    @classmethod
    def read_one_id(cls, conn: pymysql.connect, instance_id: int, select_parameters: list=None ):
        """
        class metoda, která vrací tuple s atributy tabulky instanci tabulky

        :param cls: třída, která volá metodu
        :param conn: připojení k MySQL databázi
        :param instance_id: id usera, u kterého chceme změnit údaje
        :return: tuple atributů
        """
        try:
            if select_parameters is None:
                select_parameters = cls.select_parameters
            with conn.cursor() as cursor:
                query = f'SELECT {", ".join(select_parameters)} FROM {cls.table_name} WHERE id = %s'
                cursor.execute(query, (instance_id,))
                return cls(database_tuple=cursor.fetchone())
        except pymysql.OperationalError as e:
            if e.args[0] == 2013:
                raise ConnectionLost()
            raise e

    @classmethod
    def update(cls, conn: pymysql.connect, instance_id: int, **kwargs):
        """
        class metoda, která upravuje instanci do tabulky

        :param cls: třída, která volá metodu
        :param conn: připojení k MySQL databázi
        :param instance_id: id usera, u kterého chceme změnit údaje
        :param kwargs: atributy a hodnoty
        :return: None
        """
        try:
            with conn.cursor() as cursor:
                set_values = ', '.join([f'{parameter} = %s' for parameter in kwargs.keys()])
                query = f'UPDATE {cls.table_name} SET {set_values} WHERE id = %s'
                values = tuple(kwargs.values()) + (instance_id,)
                cursor.execute(query, values)
                conn.commit()
        except pymysql.OperationalError as e:
            if e.args[0] == 2013:
                raise ConnectionLost()
            raise e

    @classmethod
    def delete(cls, conn: pymysql.connect, instance_id: int):
        """
        class metoda, která maže instanci tabulky, podle id

        :param cls: třída, která volá metodu
        :param conn: připojení k MySQL databázi
        :param instance_id: id usera, kterého chceme vymazat
        :return: None
        """
        try:
            with conn.cursor() as cursor:
                query = f'DELETE FROM {cls.table_name} WHERE id = %s'
                cursor.execute(query, (instance_id,))
                conn.commit()
        except pymysql.OperationalError as e:
            if e.args[0] == 2013:
                raise ConnectionLost()
            raise e

    @classmethod
    def read_all(cls, conn: pymysql.connect):
        try:
            with conn.cursor() as cursor:
                query = f'SELECT {", ".join(cls.select_parameters)} FROM {cls.table_name}'
                cursor.execute(query, ())
                return [cls(data) for data in cursor.fetchall()]
        except pymysql.OperationalError as e:
            if e.args[0] == 2013:
                raise ConnectionLost()
            raise e
        
    @classmethod
    def read_many_by_atributes(cls, conn: pymysql.connect, **kwargs):
        try:
            with conn.cursor() as cursor:
                order_by: str="ORDER BY "+kwargs.pop("ORDER_BY","id")+" "+kwargs.pop("ORDER","ASC")
                query = f'SELECT {", ".join(cls.select_parameters)} FROM {cls.table_name} WHERE {" and ".join([f"{atribute}=%s" for atribute in kwargs])} {order_by}'
                cursor.execute(query, tuple(kwargs.values()))
                return [cls(data) for data in cursor.fetchall()]
        except pymysql.OperationalError as e:
            print(e)
            print(e.args)
            if e.args[0] == 2013:
                raise ConnectionLost()
            raise e
        
    @classmethod
    def read_one_by_atributes(cls, conn: pymysql.connect,**kwargs):
        try:
            with conn.cursor() as cursor:
                query = f'SELECT {", ".join(cls.select_parameters)} FROM {cls.table_name} WHERE {" and ".join([f"{atribute}=%s" for atribute in kwargs])}'
                cursor.execute(query, tuple(kwargs.values()))
                response = cursor.fetchone()
                if response == None:
                    raise NoResultsFoundException(cls.table_name,**kwargs)
                return cls(database_tuple=response)
        except pymysql.OperationalError as e:
            print(e)
            print(e.args)
            if e.args[0] == 2013:
                raise ConnectionLost()
            raise e
        
class UniqueAttributeException(Exception):
    def __init__(self, table, attribute, value):
        self.table=table
        self.attribute= attribute
        self.value=value
        self.message = f"V {self.table}.{self.attribute} už existuje hodnota {self.value}"
        
class NoResultsFoundException(Exception):
    def __init__(self, table, **kwargs):
        self.table=table
        self.attributes=kwargs
        
class ConnectionLost(Exception):
    def __init__(self, **kwargs) -> None:
        print("proběhla chyba s databází")