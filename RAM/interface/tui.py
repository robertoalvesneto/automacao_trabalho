from os import system
from datetime import datetime
from pick import pick

from utils.csv import My_CSV
from utils.folder import Folder
from utils.utils import Utils
from utils.api import My_API


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class pressettext:
    EMPTYINPUT = bcolors.WARNING + \
        "please, insert some value\n" + bcolors.ENDC
    END_EMPTYINPUT = bcolors.WARNING + \
        "you typed nothing twice in a row, process finished" + bcolors.ENDC
    INVALIDVALUE = bcolors.WARNING + \
        "please, insert a valid value\n" + bcolors.ENDC


class TUI:
    """
    Simple Text-based User Interface
    """

    def __init__(self):
        self.csv = My_CSV()
        self.folder = Folder()
        self.utils = Utils()
        self.api = My_API()

    def clear_terminal(self) -> None:
        """
        Description:
        Clean terminal interface
        """
        system('cls||clear')

    def __format_tasks(self, tasks: list) -> list:
        """
        Description:
        Transform tasks from tuple to text format

        Parameters:
        :tasks:   (list) list of tuples with data of tasks

        :return:  (list) list of formated texts
        """

        m_rows = []

        for row in tasks:
            row = list(row)

            name = row[1]
            description = row[2]
            progress = str(row[3])
            fornight = self.api.convert_fornight_to_str(row[5])
            month = self.utils.convert_month(row[6])

            line_text = progress + '\t' + fornight + '\t'
            line_text += month + '\t' + name

            m_rows.append(line_text)

        return m_rows

    def __input_name(self, value: str = None) -> str:
        """
        Name:
        Auxiliar name input interface by terminal

        Parameters:
        :value:    (str) previous value of input

        :return:   (str) new value
        """

        name = ''
        count = 0
        while name == '':
            print("Previous value: ", value)
            print("Insert name:")
            name = input(":: ")

            self.clear_terminal()

            if count == 1 and name == '':
                print(pressettext.END_EMPTYINPUT)
                exit()
            elif name == '':
                print(pressettext.EMPTYINPUT)
                count += 1

        return name

    def __input_description(self, value: str = None) -> str:
        """
        Description:
        Auxiliar description input interface by terminal

        Parameters:
        :value:    (str) previous value of input

        :return:   (str) new value
        """

        description = ''
        count = 0
        while description == '':
            print("Previous value: ", value)
            print("Insert description:")
            description = input(":: ")

            self.clear_terminal()

            if count == 1 and description == '':
                print(pressettext.END_EMPTYINPUT)
                exit()
            elif description == '':
                print(pressettext.EMPTYINPUT)
                count += 1

        return description

    def __input_fornight(self, value:str = None) -> int:
        """
        Description:
        Auxiliar fornight input interface by terminal

        Parameters:
        :value:    (str) previous value of input

        :return:   (int) new value
        """

        fornight = ''
        count = 0
        while not self.api.is_valid_fornight(fornight):
            print("Previous value: ", value)
            print("Insert fornight ('first', 0 or 'second', 1):")
            fornight = input(":: ")

            self.clear_terminal()

            if count == 1 and self.api.is_empty(fornight):
                print(pressettext.END_EMPTYINPUT)
                exit()
            elif self.api.is_empty(fornight):
                print(pressettext.EMPTYINPUT)
                count += 1
            elif not self.api.is_valid_fornight(fornight):
                print(pressettext.INVALIDVALUE)

        fornight = self.api.convert_fornight_to_int(fornight)

        return fornight

    def __input_progress(self, value:str = None) -> int:
        """
        Description:
        Auxiliar progress input interface by terminal

        Parameters:
        :value:    (str) previous value of input

        :return:   (int) new value
        """
        
        progress = ''
        count = 0
        while not self.api.is_valid_progress(progress):
            print("Previous value: ", str(value) + "%")
            print("Insert progress (integer value):")

            progress = input(":: ")

            self.clear_terminal()

            if count == 1 and self.api.is_empty(progress):
                print(pressettext.END_EMPTYINPUT)
                exit()
            elif self.api.is_empty(progress):
                print(pressettext.EMPTYINPUT)
                count += 1
            elif not self.api.is_valid_progress(progress):
                print(pressettext.INVALIDVALUE)
                print("please, insert valid value")

        return progress

    def list_tasks(self, current_month: bool = None) -> list:
        """
        Description:
        Create struct of first menu, show him and return results

        Parameters:
        :current_month: (bool) choose if want get all tasks or only of
                        current month
        
        :return:   (list) name of option, index and list of tasks
        """
        
        title = 'Choose one option:'
        subtitle = '\n   %\tfn\tmonth\tname'
        tasks = None
        if current_month in (False, None):
            tasks = self.api.get_tasks()
        else:
            tasks = self.api.get_tasks_for_current_month()
        text_tasks = self.__format_tasks(tasks)

        text_tasks.append('\n')
        text_tasks.append('+ add tasks')
        text_tasks.append('+ export tasks as a csv')
        text_tasks.append('close')

        if len(text_tasks) > 1:
            title += subtitle

        option, index = pick(text_tasks, title, indicator='=>')

        return option, index, tasks

    def delete_task(self, task: list) -> None:
        """
        Description:
        Create struct of confirmation delete menu, perform operation and
        show result

        Parameters:
        :task:    (list) values of task to remove
        """
        
        title = "Are you sure you want to DELETE this task?"
        resps = ['yes', 'no']

        option, index = pick(resps, title, indicator='=>')

        if option == 'no':
            print("Cancelled operation")
        else:
            message = self.api.delete_task(task)
            print(message)

    def edit_task(self, option: str, task: list) -> None:
        """
        Description:
        Create struct of menu to select option to edit one task, perform
        operation and show result

        Parameters:
        :task:    (list) values of task to remove
        """
        
        title = 'What you want to do?\n:: ' + option
        options = ['update progress', 'edit description',
                   'edit fornight', 'delete']

        option, index = pick(options, title, indicator='=>')

        print(task)
        update_value = None
        if option == 'update progress':
            update_value = self.__input_progress(task[3])
        elif option == 'edit description':
            update_value = self.__input_description(task[2])
        elif option == 'edit fornight':
            update_value = self.__input_fornight(task[5])
        else:
            self.delete_task(task)
            exit()

        message = self.api.update_task(task, index, update_value)
        print(message)

    def add_task(self) -> None:
        """
        Description:
        Call all private method to get values to add new task and passe
        struct to database create him
        """
        
        name = self.__input_name()
        description = self.__input_description()
        fornight = self.__input_fornight()
        progress = self.__input_progress()
        last_modify = self.utils.get_date_br_format()
        month = self.utils.get_month()

        message = self.api.insert_task(
            name,
            description,
            progress,
            fornight,
            month,
            last_modify
        )

        print(message)

    def export_csv(self) -> None:
        """
        Description:
        Export database to CSV format to correct directory
        """
        
        tasks = self.api.get_tasks()

        if len(tasks) == 0:
            print("No record to export !")
        else:
            tasks = self.api.convert_tuple_to_list(tasks)
            header = ['id', 'description', 'progress', 'owner', 'fortnight',
                      'month', 'last_modify']

            dt = datetime.now()
            format_dt_c = dt.strftime('%Y-%m-%d_%Hh-%Mm')

            filename = 'task--' + format_dt_c
            self.csv.write_file(self.folder.source_path,
                                filename, header, tasks)

            print("Successfully exported")

    def menu(self) -> None:
        """
        Description:
        Builder method to interface
        """
        self.clear_terminal()

        option, index, tasks = self.list_tasks(True)

        if index < len(tasks):
            self.edit_task(option, tasks[index])
        elif option == '+ add tasks':
            self.add_task()
        elif option == '+ export tasks as a csv':
            self.export_csv()
        elif option == 'close':
            pass
