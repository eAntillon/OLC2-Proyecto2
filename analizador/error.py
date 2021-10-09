from datetime import datetime

class BreakError(Exception):
    pass

class ContinueError(Exception):
    pass

class ReturnError(Exception):
    def __init__(self, expresion):
        self.expresion = expresion

class errorTabla(Exception):
    def __init__(self, dictionary):
        self.valor = dictionary

class error():
    ''' Lanza un error y rompe la ejecucion de instrucciones'''

    def __init__(self, mensaje, tipo, linea):
        str_err = ("ERROR: %s en %s linea: %s" %(mensaje, tipo, linea))
        print('\x1b[6;30;42m' + str_err + '\x1b[0m')
        er = {"desc": mensaje, "linea": linea, "time": datetime.now()}
        raise errorTabla(er)
        
class error_lex(Exception):
    ''' Lanza un error de sintaxis y rompe la ejecucion de instrucciones'''

    def __init__(self, mensaje, tipo, linea):
        str_err = ("ERROR: %s en %s linea: %s" %(mensaje, tipo, linea))
        # Añadir a tabla de errores
        print(str_err)
        raise Exception (str_err)
