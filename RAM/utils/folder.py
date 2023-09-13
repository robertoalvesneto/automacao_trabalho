import platform
import os
import datetime

from decouple import config

class Folder:
    """
    Manipulate dir and files
    """
    
    def __init__(self) -> None:
        self.source_path = None
        self.work_path = config('PRIMARYDIR')
        self.daily_path = config('SECONDARYDIR')

        self.__check_current_system()
        self.__create_dir()

    def __check_current_system(self) -> None:
        """
        Description:
        Check if my OS is windows or linux and set correct path reading
        .env file

        :init: set correct path
        """
        
        if platform.system() == 'Windows':
            self.source_path = config('WINDOWSPATH')
        elif platform.system() == 'Linux':
            base_path = os.path.expanduser("~")
            relative_path = config('LINUXPATH')
            self.source_path = os.path.join(base_path, relative_path)
        else:
            raise Exception('whoami?')

    def __create_dir(self) -> None:
        """
        Description:
        Check if directory exist
            if not, create and return path
            else, only return path

        :return: path for directory
        """
        
        previous_path = self.source_path
        path = os.path.join(previous_path, self.work_path)

        if self.work_path not in os.listdir(previous_path):
            os.mkdir(path)

        previous_path = path
        path = os.path.join(previous_path, self.daily_path)

        if self.daily_path not in os.listdir(previous_path):
            os.mkdir(path)

        self.source_path = path


    def get_base_path(self) -> str:
        base_path = os.path.expanduser("~")
        relative_path = config('CURRENTCODEDIR')
        return os.path.join(base_path, relative_path)


    def get_create_date(self, filename: str) -> datetime:
        """
        Description:
        Gets the creation date of the folder
        
        Parameters:
        :filename:   (str) name of file
        
        :return: (datetime) creation date of the folder
        """
        
        c_time = os.path.getctime(os.path.join(self.source_path, filename))
        dt_c = datetime.datetime.fromtimestamp(c_time)

        return dt_c

    def date_br_format(self, dt_c: datetime) -> str:
        """
        Description:
        Formats the date to BR style
        
        Parameters:
        :dt_c:   (datetime) date time
        
        :return: (str) date in BR format
        """
        
        format_dt_c = dt_c.strftime('%Y-%m-%d_%Hh-%Mm')

        return format_dt_c
    
    def get_last_created_file(self) -> str:
        """
        Description:
        Get last file created

        :return:    (str) file name
        """

        filenames = os.listdir(self.source_path)

        tmp_filename = ''
        tmp_date = None
        for filename in filenames:
            # Compare only if have previous register
            # OR
            # Get filename with latest date
            create_date = self.get_create_date(filename)
            if tmp_date == None or tmp_date < create_date:
                tmp_filename = filename
                tmp_date = create_date

        if tmp_filename == '':
            return 'folder empty'

        return tmp_filename

    def remove_all_files(self) -> None:
        """
        Description: Cleans the folder
        """

        filenames = os.listdir(self.source_path)

        for filename in filenames:
            os.remove(os.path.join(self.source_path, filename))