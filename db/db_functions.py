import sqlite3
from dataclasses import fields
from sqlite3 import Error
from pickle import dumps, loads
from typing import List
from contextlib import closing



not_pickle_list = [str, int, float, bool]


def db_create_connection(db_file: str = 'db/embyupdate.db') -> sqlite3.Connection:
    """
    create a database connection to a SQLite database

    :param db_file: Path to database file
    :type db_file: str
    :return: Returns the connection
    :rtype: sqlite3.Connection
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
    except Error as e:
        print(e)

    return conn


def db_select_value(conn: sqlite3.Connection, table, value, where, where_what) -> sqlite3.Row:
    """
    Select single row/values from a table with WHERE clause

    SELECT {value(s)} FROM {table} WHERE {where} = {where_what}

    EX: SELECT weight FROM items WHERE name = Dagger

    Returns a sqlite3 addressable row ex: row['name']

    :param conn: Db connection
    :type conn: sqlite3.Connection
    :param table: Table to pull from
    :type table: str
    :param value: Value(s) to pull. Can be multiple, separated by a ,
    :type value: str
    :param where: Column for where query
    :type where: str
    :param where_what: Value to match for where query
    :type where_what: Any
    :return: row
    :rtype: sqlite3.Row
    """
    with conn:
        with closing(conn.cursor()) as cur:
            cur = conn.cursor()
            sql = f"SELECT {value} FROM {table} WHERE {where} = ? "
            param = [where_what]
            cur.execute(sql, param)
            rows = cur.fetchone()

    return rows[value]


def db_select_values_where(conn: sqlite3.Connection, table, value, where, where_what) -> List[sqlite3.Row]:
    """
    Select multiple rows/values from a table with WHERE clause

    SELECT {value(s)} FROM {table} WHERE {where} = {where_what}

    EX: SELECT name FROM races WHERE mob = False

    Returns a sqlite3 addressable list of rows ex: row['name']

    :param conn: DB connection
    :type conn: sqlite3.Connection
    :param table: table to pull from (single value)
    :type table: str
    :param value: Column value(s) to pull. Can be multiple, separated by a ,
    :type value: str
    :param where: Column for where query
    :type where: str
    :param where_what: Value for where query
    :type where_what: any
    :return: Rows
    :rtype: sqlite3.Row
    """

    sql = f"SELECT {value} FROM {table} WHERE {where} = ?"
    with conn:
        with closing(conn.cursor()) as cur:
            cur = conn.cursor()
            param = [where_what]
            cur.execute(sql, param)
            rows = cur.fetchall()

    return rows


def db_select_values(conn: sqlite3.Connection, table, value) -> List[sqlite3.Row]:
    """
    Select multiple rows/values from a table with WHERE clause

    SELECT {value(s)} FROM {table}

    EX: SELECT name FROM races

    Returns a sqlite3 addressable list of rows ex: row['name']

    :param conn: DB connection
    :type conn: sqlite3.Connection
    :param table: table to pull from (single value)
    :type table: str
    :param value: Column value(s) to pull. Can be multiple, separated by a ,
    :type value: str
    :return: Rows
    :rtype: sqlite3.Row
    """

    sql = f"SELECT {value} FROM {table}"
    with conn:
        with closing(conn.cursor()) as cur:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()

    return rows


def db_insert_class_in_table(conn: sqlite3.Connection, dataclass: any, table: str):
    """
    Inserts an entire dataclass object into the specified table. Builds the insert query dynamically.

    INSERT into {table} ({inserts}) VALUES({val_param_placeholders})

    :param conn: DB connection
    :type conn: sqlite3.Connection
    :param dataclass: Dataclass to insert into table
    :type dataclass: any
    :param table: Table to insert into
    :type table: str
    :return: Returns query rowcount results
    :rtype: int
    """
    class_dict = {}

    # We pull all the fields to insert into the table from the dataclass object and build a dictionary of them
    # along with their values, of special note, we are pickling some of the fields values as well
    for field in fields(dataclass):
        if field.type in not_pickle_list:
            class_dict[field.name.lower()] = getattr(dataclass, field.name)
        else:
            class_dict[field.name.lower()] = dumps(getattr(dataclass, field.name))

    # Here we are getting list of the column names(keys) and values so we can count them to build our dynamic query
    # then using the lists to populate the query
    col_names = class_dict.keys()
    params = list(class_dict.values())
    col_num = len(col_names)
    inserts = ', '.join(col_names)
    val_param_placeholders = ('?,' * col_num)[:-1]
    sql = f'INSERT into {table} ({inserts}) VALUES({val_param_placeholders})'
    with conn:
        with closing(conn.cursor()) as cur:
            cur = conn.cursor()
            result = cur.execute(sql, params)

    return result.rowcount


def db_update_class_in_table(conn: sqlite3.Connection, dataclass, table, where, where_what):
    """
    Pass this function any dataclass object and it will take it apart and pickle any python
    types the DB can't store on it's own. Then update the row. The query is built dynamically.

    UPDATE {table} SET {inserts} WHERE {where} = ?

    :param conn: DB connection
    :type conn: sqlite3.Connection
    :param dataclass: dataclass to store in the DB
    :type dataclass: any
    :param table: Table to update into
    :type table: str
    :param where: Column to id row to update
    :type where: str
    :param where_what: value to use for identifying row to update
    :type where_what: str
    :return: Returns the query rowcount results
    :rtype: int
    """
    class_dict = {}

    # We pull all the fields to insert into the table from the dataclass object and build a dictionary of them
    # along with their values, of special note, we are pickling some of the fields values as well
    for field in fields(dataclass):
        if field.type in not_pickle_list:
            class_dict[field.name.lower()] = getattr(dataclass, field.name)
        else:
            class_dict[field.name.lower()] = dumps(getattr(dataclass, field.name))

    # Here we are getting list of the column names(keys) and values so we can count them to build our dynamic query
    # then using the lists to populate the query

    params = list(class_dict.values())
    set_names = []
    for key in class_dict.keys():
        set_names.append(f'{key} = ?')
    inserts = ', '.join(set_names)
    params.append(where_what)
    sql = f'UPDATE {table} SET {inserts} WHERE {where} = ?'
    with conn:
        with closing(conn.cursor()) as cur:
            cur = conn.cursor()
            result = cur.execute(sql, params)

    return result.rowcount


def db_return_class_object(conn: sqlite3.Connection, table, where_field, where_what, dataclass):
    """
    Returns an entire dataclass object from a table.

    :param conn: DB connection
    :type conn: sqlite3.Connection
    :param table: Table to pull from
    :type table: str
    :param where_field: Where query column name
    :type where_field: str
    :param where_what: Where query value
    :type where_what: str
    :param dataclass: Dataclass to fill
    :type dataclass: any
    :return: Filled dataclass instance
    :rtype: dataclass
    """
    sql = f'SELECT * FROM {table} WHERE {where_field} = ?'
    param = [where_what]
    with conn:
        with closing(conn.cursor()) as cur:
            cur = conn.cursor()
            cur.execute(sql, param)
            row = cur.fetchone()

    # We have to do some special stuff to fill the dataclass. We have to know to unpickle certain fields and to
    # swap the bool values from int back to bool.
    for field in fields(dataclass):
        if field.type == bool:
            setattr(dataclass, field.name, False if row[field.name.lower()] == 0 else True)
        elif field.type in not_pickle_list:
            setattr(dataclass, field.name, row[field.name.lower()])
        else:
            setattr(dataclass, field.name, loads(row[field.name.lower()]))

    return dataclass


def db_delete_row(conn: sqlite3.Connection, table, where, where_what):
    """
    Delete row(s) from table with a singe where clause.

    DELETE FROM {table} WHERE {where} = ?

    :param conn: Connection to the Db
    :type conn: sqlite3.Connection
    :param table: Table to delete from
    :type table: str
    :param where: Where column to use for delete
    :type where: str
    :param where_what: Value to use to find row in column
    :type where_what: str
    :return: Returns query rowcount as integer
    :rtype: any
    """
    param = [where_what]
    sql = f'DELETE FROM {table} WHERE {where} = ?'

    with conn:
        with closing(conn.cursor()) as cur:
            cur = conn.cursor()
            result = cur.execute(sql, param)

    return result.rowcount


def db_insert_inventory_char_creation(conn, inv_dict):
    """
    Special function used only in initial character creation. Inserts the class items into player inventory.
    No other uses.

    :param conn: Connection to DB
    :type conn: sqlite3.Connection
    :param inv_dict: Dictionary built during character creation
    :type inv_dict: dict
    """
    for each in inv_dict:
        db_insert_class_in_table(conn, inv_dict[each], 'inventory')


def db_create_inventory_dict(conn, player_name):
    """
    Creates a dictionary with numbers for keys and Items dataclass for values.

    :param conn: Connection to DB
    :type conn: sqlite3.Connection
    :param player_name: Name of player to pull data for
    :type player_name: str
    :return: Returns a dictionary of inventory items
    :rtype: dict
    """
    inventory_dict = {}
    with conn:
        rows = db_select_values_where(conn, 'inventory', 'id', 'player_name', player_name)
        num = 0
        for row in rows:
            inventory_dict[num] = db_return_class_object(conn, 'inventory', 'id', row['id'], Inventory)
            num += 1
    return inventory_dict


def db_update_value(conn: sqlite3.Connection, table, value, update_value, where, where_what):
    """
    Updates a single value in a table.

    UPDATE {table} SET {value}= ? WHERE {where} = ?

    :param conn: Connection to DB
    :type conn: sqlite3.Connection
    :param table: Table to do update in
    :type table: str
    :param value: Column to update
    :type value: str
    :param update_value: Value to update to
    :type update_value: any
    :param where: Where column for finding row to update
    :type where: str
    :param where_what: Where value to match
    :type where_what: str
    :return: Returns query rowcount
    :rtype: int
    """
    sql = f'UPDATE {table} SET {value}= ? WHERE {where} = ?'
    params = (update_value, where_what)
    with conn:
        with conn:
            with closing(conn.cursor()) as cur:
                cur = conn.cursor()
                result = cur.execute(sql, params)

    return result.rowcount
