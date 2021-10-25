from dataclasses import dataclass

from enum import Enum
class Tipo(Enum):
    Int64 = "Int64"
    Float64 = "Float64"
    Bool = "Bool"
    Char = "Char"
    String = "String"
    Nothing = "Nothing"
    Array = "Array"
    Struct = "Struct"


@dataclass
class simbolo():

    id: str
    valor: any
    tipo: Tipo
    entorno: str
    apuntador: int
    line: int
    col: int

    def __init__(self, id, tipo, entorno, apuntador, linea, columna):
        self.id = id
        self.tipo = tipo
        self.entorno = entorno
        self.apuntador = apuntador
        self.line = linea
        self.col = columna

    def print(self):
        print("id: ",self.id, ", tipo: ", self.tipo.value, "apuntador: ", self.apuntador, ", entorno: ", self.entorno, ", linea: ", self.linea, ", columna: ")
    
    def toString(self):
        return "id: %s, tipo: %s, apuntador: %s,entorno: %s, linea: %s, columa: %s"%(self.id, self.tipo.value, self.apuntador,self.entorno, self.line, self.col)

    def arrayString(self, array):
        lista = []
        for l in array:
            if isinstance(l, list):
                lista.append(self.arrayString(l))
            elif isinstance(l, dict):
                lista.append(self.dictString(l))
            else:
                lista.append(l.value)
        return lista

    def dictString(self, dictonary):
        dicto = {}
        for key, value in dictonary.items():
            if isinstance(value, list):
                dicto[key] = self.arrayString(value)
            elif isinstance(value, dict):
                dicto[key] = self.dictString(value)
            else:
                try:
                    dicto[key] = value.value
                except Exception:
                    dicto[key] = value
        return dicto

class tabla_simbolos():

    def __init__(self, simbolos={}, structs ={}, variables_struct ={}, funcs ={}):
        self.simbolos = simbolos
        self.structs = structs # INFORMACION DE STRUCTS
        self.variable_struct = variables_struct # VARIABLES Y SU TIPO DE STRUCT
        self.funcs = funcs # FUNCIONES
        self.funciones_print = []
        self.pos = 1

    def add(self, simbolo):
        self.simbolos[simbolo.id] = simbolo
        self.pos += 1
    
    def get(self, id):
        ''' Retorna el simbolo si existe, sino devuelve None'''
        return self.simbolos.get(id, None)
    
    def getPos(self):
        return self.pos

    def update(self, simbolo):
        if(simbolo.id in self.simbolos.keys()):
            self.simbolos.update({simbolo.id : simbolo})
            return True
        else:
            return False
    
    def delete(self, id):
        if(id in self.simbolos.keys()):
            self.simbolos.pop(id)
            return True
        else:
            return False

    def clean(self):
        self.simbolos = {}
        self.structs = {} # INFORMACION DE STRUCTS
        self.variable_struct = {} # VARIABLES Y SU TIPO DE STRUCT
        self.funcs = {} # FUNCIONES

    def print(self):
        print("--- Tabla de simbolos ---")
        if len(self.simbolos) > 0:
            for s in self.simbolos.values():
                print(" ->", s.toString())
        else:
            print("Tabla vacia")
        print("-------------------------")
        #self.print_structs()
        #self.print_funcs()
        #self.print_variable_struct()