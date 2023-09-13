import sqlite3
from sqlite3 import Error
from typing import Literal

from utils.folder import Folder

class Database:
    """
    Class to connect to the database and execute the queries
    """

    def __init__(self):
        self.folder = Folder()
        self.path = self.folder.get_base_path() + "/RAM/database/pythonsqlite.db"

    def __create_connection(self) -> sqlite3.Connection:
        """
        Description:
        Create a database connection to the SQLite database specified by
        the db_file

        :return: Connection object or None
        """

        conn = None
        try:
            conn = sqlite3.connect(self.path)
            return conn
        except Error as e:
            print(e)

        return conn

    def __create_table(self,
                       conn: sqlite3.Connection,
                       create_table_sql: Literal
                       ) -> None:
        """
        Description:
        Run sql instruction to create database

        Parameters:
        :conn:               (sqlite3.Connection) database connection
        :create_table_sql:   (Literal) sql to create table
        """

        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def create_db(self) -> None:
        """
        Description:
        function that declares the table structure and checks if the
        database already exists, if not, tries to create it
        """

        sql_create_task_table = """ CREATE TABLE IF NOT EXISTS task (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            description text NOT NULL,
                                            progress tinyint NOT NULL,
                                            owner text NOT NULL,
                                            fortnight boolean NOT NULL,
                                            month tinyint NOT NULL,
                                            last_modify date NOT NULL
                                        ); """

        conn = self.__create_connection()

        if conn is not None:
            self.__create_table(conn, sql_create_task_table)
        else:
            print("Error! cannot create the database connection.")

    def __validate_dict(self, type: str, task: dict) -> tuple:
        """
        Description:
        Validate task dict and convert to tuple. Each type has its own
        form of validation (insert, delete, update)

        Parameters:
        :type:   (str) type of sql command
        :task:   (dict) with task data

        :return: valid task (tuple)
        """
        valid_keys = ('id', 'name', 'description', 'progress', 'owner',
                      'fortnight', 'month', 'last_modify')
        valid_map = {'id': 0, 'name': 0, 'description': 0, 'progress': 0,
                     'owner': 0, 'fortnight': 0, 'month': 0, 'last_modify': 0}

        t_task = []

        valid_map['id'] = 1 if type == 'insert' else 0

        # Check if is a dict object
        if not isinstance(task, dict):
            raise Exception("invalid type")

        # Validate delete
        if type == 'delete':
            if 'id' not in task:
                raise Exception("key 'id' not exist")
            else:
                return tuple([task['id']])

        # If is a insert or update, get correct data
        for k, v in task.items():
            if k not in valid_keys:
                raise Exception("invalid key: " + str(k))
            elif type == 'insert' and k == 'id':
                # Not add 'id' if tuple is for insert new register
                pass
            else:
                valid_map[k] = 1
                t_task.append(v)

        # Insert need all data
        if type == 'insert' and 0 in valid_map.values():
            names = []
            for k, v in valid_map.items():
                if v == 0:
                    names.append(k)
            raise Exception("Missing data: " + str(names))

        # Update need 'id' in end of list
        elif type == 'update':
            t_task = t_task[1:] + [t_task[0]]

        return tuple(t_task)

    def insert_task_task(self, task: dict) -> None:
        """
        Description:
        Insert a new task on task document

        Parameters:
        :task:   (dict) with task data
        """

        task = self.__validate_dict('insert', task)

        sql = ''' INSERT INTO task(name, description,progress,owner,fortnight,month,last_modify)
                VALUES(?,?,?,?,?,?,?) '''

        resp = self.__run_sql_instruction(sql, task)

    def update_task_task(self, task: dict) -> None:
        """
        Description:
        Update some data for task

        Parameters:
        :task:   (dict) with task data
        """

        task = self.__validate_dict('update', task)

        sql = ''' UPDATE task
                SET name = ?,
                    description = ?,
                    progress = ?,
                    owner = ?,
                    fortnight = ?,
                    month = ?,
                    last_modify = ?
                WHERE id = ?'''

        resp = self.__run_sql_instruction(sql, task)

    def delete_task_task(self, task: dict) -> None:
        """
        Description:
        Delete a task by task id

        Parameters:
        :task:   (dict) with task data
        """

        task = self.__validate_dict('delete', task)

        sql = 'DELETE FROM task WHERE id=?'

        resp = self.__run_sql_instruction(sql, task)

    def select_all_tasks(self) -> list:
        """
        Description:
        Query all rows in the tasks table
        
        :return:    (list) all tasks
        """

        sql = 'SELECT * FROM task ORDER BY month DESC, progress'

        resp = self.__run_sql_instruction(sql, None)

        rows = resp.fetchall()

        return rows

    def select_all_tasks_by_month(self, month: int) -> list:
        """
        Description:
        Query all rows of month (month) in the tasks table
        
        Parameters:
        :month: (int) pass value of month you want get

        :return:    (list) all tasks
        """

        sql = 'SELECT * FROM task WHERE month = ? ORDER BY month DESC, progress'

        resp = self.__run_sql_instruction(sql, [month])

        rows = resp.fetchall()

        return rows

    def __run_sql_instruction(self, sql: str, values: tuple) -> sqlite3.Cursor:
        """
        Description:
        Auxiliar function to run sql queries

        Parameters:
        :sql:     (str) sql struction
        :value:   (tuple) values to insert on query
        """
        
        print(self.folder.get_base_path())
        print(self.path)
        conn = self.__create_connection()

        with conn:
            cur = conn.cursor()

            if values == None: 
                cur.execute(sql)
            else:
                cur.execute(sql, values)
            conn.commit()

        return cur
