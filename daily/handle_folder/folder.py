import platform
import os
import datetime

from decouple import config

class Files:
    """
    Manipulate dir and files
    """
    
    
    def __init__(self) -> None:
        self.source_path = None
        self.work_path = config('PRIMARYDIR')
        self.daily_path = config('SECONDARYDIR')

        self.__check_current_system()

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
            self.source_path = config('LINUXPATH')
        else:
            raise Exception('whoami?')

    def __create_dir(self) -> str:
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

        return path

    def __get_create_date(self, fullpath: str, filename: str) -> datetime:
        """
        Description:
        Gets the creation date of the folder
        
        Parameters:
        :fullpath:   (str) path of folder
        :filename:   (str) name of file
        
        :return: (datetime) creation date of the folder
        """
        
        c_time = os.path.getctime(os.path.join(fullpath, filename))
        dt_c = datetime.datetime.fromtimestamp(c_time)

        return dt_c

    def __get_month(self, dt_c: datetime) -> str:
        """
        Description:
        Gets only the name of the month from the folder creation date
        
        Parameters:
        :dt_c:   (datetime) date time
        
        :return: (str) name of the month
        """
        
        month = dt_c.strftime('%h')

        return month

    def __date_br_format(self, dt_c: datetime) -> str:
        """
        Description:
        Formats the date to BR style
        
        Parameters:
        :dt_c:   (datetime) date time
        
        :return: (str) date in BR format
        """
        
        format_dt_c = dt_c.strftime('%Y-%m-%d_%Hh-%Mm')

        return format_dt_c

    def __rename_file(self, fullpath: str, filename: str) -> None:
        """
        Description:
        Read name of file and rename him for complete name more current
        date
        
        Parameters:
        :fullpath:   (str) path of folder
        :filename:   (str) name of file
        """
        
        dt_c = self.__get_create_date(fullpath, filename)
        format_dt_c = self.__date_br_format(dt_c)

        new_name = ''
        if filename.startswith('d'):
            new_name = 'daily'
        elif filename.startswith('ret'):
            new_name = 'retrospective'
        elif filename.startswith('rev'):
            new_name = 'review'
        elif filename.startswith('p'):
            new_name = 'planning'
        else:
            new_name = 'generic'

        new_name = ''.join([new_name, "--", format_dt_c, '.jpg'])

        current_name_path = os.path.join(fullpath, filename)
        new_name_path = os.path.join(fullpath, new_name)

        os.rename(current_name_path, new_name_path)

    def __get_last_created_files(self, fullpath: str) -> list:
        """
        Description:
        If have many files with same name in folder, the function get
        only last image of each type
        
        Parameters:
        :fullpath:   (str) path of folder
        
        :return:    (list) with the name of each file to be saved
        """
        
        filenames = os.listdir(fullpath)
        names = ['d', 'ret', 'rev', 'p']
        l_filenames = []

        for name in names:
            tmpFilename = ''
            tmpDate = None
            for filename in filenames:
                # Compare files with same names
                if filename.startswith(name):
                    # Compare only if have previous register
                    # OR
                    # Get filename with latest date
                    if tmpDate == None or tmpDate < self.__get_create_date(fullpath, filename):
                        tmpFilename = filename
                        tmpDate = self.__get_create_date(fullpath, filename)

                    filenames.remove(filename)

            if tmpFilename != '':
                l_filenames.append(tmpFilename)

        # Save generic names
        l_filenames = [*l_filenames, *filenames]

        return l_filenames

    def __remove_files(self, fullpath: str) -> None:
        """
        Description:
        If have many files with same name in folder, the function get
        only last image of each type and delete the rest
        
        Parameters:
        :fullpath:   (str) path of folder
        """
        
        filenames = os.listdir(fullpath)
        safe_filenames = self.__get_last_created_files(fullpath)

        for filename in filenames:
            if filename not in safe_filenames:
                os.remove(os.path.join(fullpath, filename))
                
    def remove_all_files(self) -> None:
        """
        Description: Cleans the folder
        """
        
        fullpath = self.__create_dir()
        
        filenames = os.listdir(fullpath)

        for filename in filenames:
            os.remove(os.path.join(fullpath, filename))

    def main(self) -> dict:
        """
        Description:
        Builder method of class.
        Get folder and filenames in folder, rename the last files added,
        deletes the rest, and return dictionary with the filename and 
        creation month
        
        :return:    (dict) filename and creation month
        """
        fullpath = self.__create_dir()
        filenames = self.__get_last_created_files(fullpath)

        d_filenames = {}

        self.__remove_files(fullpath)

        for filename in filenames:
            self.__rename_file(fullpath, filename)
        
        filenames = self.__get_last_created_files(fullpath)
        for filename in filenames:
            dt_c = self.__get_create_date(fullpath, filename)
            month = self.__get_month(dt_c)

            path = os.path.join(fullpath, filename)

            d_filenames[filename] = {'month': month, 'path': path}
            
        return d_filenames