from datetime import datetime

class Utils:
    """
    Class to simplify access to commonly used functions
    """
    
    def convert_month(self, month):
        map_month = ['january', 'february', 'march', 'april', 'may', 'june',
                     'july', 'august', 'september', 'october', 'november',
                     'december']

        if isinstance(month, int):
            return map_month[month]
        elif isinstance(month, str):
            return map_month.index(month)

        raise Exception('Any value pass')
    
    def get_date_br_format(self):
        return datetime.today().strftime('%d-%m-%Y')

    def get_month(self):
        return int(datetime.today().strftime('%m'))