from persian_tools import digits


def convert_persian_str_number_to_number(persian_number):
     '''
     Get a persian number and return coresponding integer number
     Parameters:
          persian_number (str): a string like "۲۸,۱۰۰,۰۰۰"
     Returns:
          number (integer): a integer number like 28100000
     '''
     return convert_persian_str_number_to_english_str_number(persian_number)
     

def convert_persian_str_number_to_english_str_number(persian_number):
     '''
     Get a persian number and return coresponding integer number
     Parameters:
          persian_number (str): a string like "۴.۴"
     Returns:
          number (integer): a integer number like 4.4
     '''
     return digits.convert_to_en(persian_number).replace(",","")

def write_to_file(name, data):
    fo = open(name, "w")
    fo.write(str(data))
    fo.close()


def read_file(name):
    fo = open(name, "r")
    content = fo.read()
    fo.close()
    return content