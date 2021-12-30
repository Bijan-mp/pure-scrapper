from persian_tools import digits


def convert_persian_number_to_int(persian_number):
     '''
     Get a persian number and return coresponding integer number
     Parameters:
          persian_number (str): a string like "۲۸,۱۰۰,۰۰۰"
     Returns:
          number (integer): a integer number like 28100000
     '''
     return int(digits.convert_to_en(persian_number).replace(",",""))
     