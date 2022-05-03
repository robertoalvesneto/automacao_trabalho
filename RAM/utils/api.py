from database.database import Database
from utils.utils import Utils

from decouple import config

class My_API:
    """
    Class to controller database manipulations
    """

    def __init__(self) -> None:
        self.db = Database()
        self.utils = Utils()
        self.db.create_db()

    def get_tasks(self):
        rows = self.db.select_all_tasks()

        return rows
    
    def get_tasks_for_current_month(self):
        rows = self.db.select_all_tasks_by_month(self.utils.get_month())

        return rows

    def is_not_empty(self, value) -> bool:
        return False if value in ('', None) else True

    def is_empty(self, value) -> bool:
        return False if value not in ('', None) else True

    def is_valid_fornight(self, value) -> bool:
        valid_values = ('first', '0', 'second', '1', 0, 1)
        return False if value not in valid_values else True

    def is_valid_progress(self, value) -> int:
        try:
            value = int(value)
            return False if value not in range(0, 101) else True
        except:
            return False

    def convert_fornight_to_str(self, value) -> int:
        map_fornight = ['first', 'second']

        if self.is_empty(value):
            raise Exception('Any value pass')
        elif isinstance(value, int) and value in (1, 0):
            return map_fornight[value]
        elif isinstance(value, str) and value in ('1', '0'):
            return map_fornight[int(value)]
    
        raise Exception("invalid value")
    
    def convert_fornight_to_int(self, value) -> str:
        map_fornight = ['first', 'second']

        if self.is_empty(value):
            raise Exception('Any value pass')
        elif isinstance(value, int) and value in (1, 0):
            return value
        elif isinstance(value, str) and value in ('1', '0'):
            return int(value)
        elif isinstance(value, str) and value in map_fornight:
            return map_fornight.index(value)
        
        raise Exception("invalid value")
    
    def convert_progress_to_int(self, value) -> int:
        if self.is_empty(value):
            raise Exception('Any value pass')
        elif isinstance(value, int):
            return value
        elif isinstance(value, str):
            try:
                value = int(value)
                if value not in range(0, 100):
                    return value
                else:
                    raise Exception("invalid range value")
            except ValueError:
                raise Exception("invalid value")
        elif isinstance(value, float):
            return int(round(value))
        
        raise Exception("invalid value")

    def invert_fornight(self, value):
        map_fornight = ['first', 'second']

        if isinstance(value, int):
            return map_fornight[value]
        elif isinstance(value, str):
            return map_fornight.index(value)

        raise Exception('Any value pass')

    def convert_tuple_to_dict(self, tasks):
        l_tasks = []
        for task in tasks:
            task = list(task)

            d_task = {
                'id': task[0],
                'description': task[1],
                'progress': task[2],
                'owner': task[3],
                'fortnight': task[4],
                'month': task[5],
                'last_modify': task[6]
            }

            l_tasks.append(d_task)

        return l_tasks

    def convert_tuple_to_list(self, tasks):
        l_tasks = []
        for task in tasks:
            task = list(task)

            l_tasks.append(task)

        return l_tasks

    def insert_task(self, description, progress, fornight, month, last_modify):
        new_task = {
            'description': description,
            'progress': progress,
            'owner': config('OWNER'),
            'fortnight': fornight,
            'month': month,
            'last_modify': last_modify
        }

        self.db.insert_task_task(new_task)

        return "New task successfully added"

    def update_task(self, task, option, value):
        task = list(task)

        update_task = {
            'id': task[0],
            'description': task[1],
            'progress': task[2],
            'owner': task[3],
            'fortnight': task[4],
            'month': task[5],
            'last_modify': task[6]
        }

        if option == 0:
            update_task['progress'] = value
        elif option == 1:
            update_task['description'] = value
        elif option == 2:
            update_task['fortnight'] = value
        else:
            raise Exception("Invalid option to update")

        self.db.update_task_task(update_task)
        return 'Task successfully updated'

    def delete_task(self, task):
        task = list(task)

        task = {
            'id': task[0],
            'description': task[1],
            'progress': task[2],
            'owner': task[3],
            'fortnight': task[4],
            'month': task[5],
            'last_modify': task[6]
        }

        self.db.delete_task_task(task)
        return "task successfully deleted"
