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
    line: int
    col: int

    def __init__(self, id, valor, tipo, entorno, linea, columna):
        self.id = id
        self.valor = valor
        self.tipo = tipo
        self.entorno = entorno
        self.line = linea
        self.col = columna

    def print(self):
        print("id: ",self.id, ", valor: ", self.valor, ", tipo: ", self.tipo.value, ", entorno: ", self.entorno, ", linea: ", self.linea, ", columna: ")
    
    def toString(self):
        if isinstance(self.valor, list):
            return "id: %s, valor: %s, tipo: %s, entorno: %s, linea: %s, columa: %s"%(self.id, self.arrayString(self.valor), self.tipo.value, self.entorno, self.line, self.col)
        elif isinstance(self.valor, dict):
            return "id: %s, valor: %s, tipo: %s, entorno: %s, linea: %s, columa: %s"%(self.id, self.dictString(self.valor), self.tipo.value, self.entorno, self.line, self.col)
        else:
            return "id: %s, valor: %s, tipo: %s, entorno: %s, linea: %s, columa: %s"%(self.id, self.valor, self.tipo.value, self.entorno, self.line, self.col)

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

    def add(self, simbolo):
        self.simbolos[simbolo.id] = simbolo
    
    def get(self, id):
        ''' Retorna el simbolo si existe, sino devuelve None'''
        return self.simbolos.get(id, None)
    
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
    
    # STRUCTS
    def add_struct(self,tipo, id, parametros):
        self.structs[id] = [tipo, id, parametros]

    def get_struct(self, id):
        ''' Retorna la informacion de un tipo de struct definido'''
        return self.structs.get(id, None)

    def print_structs(self):
        print("--- Tabla de structs ---")
        if len(self.structs) > 0:
            for s in self.structs.values():
                print(" ->", s)
        else:
            print("Tabla vacia")
        print("-------------------------")
        
    def add_variabe_struct(self, id, tipo):
        self.variable_struct[id] = tipo
    
    def get_variable_struct(self, id):
        v = self.variable_struct.get(id, None)
        return v

    def print_variable_struct(self):
        print("--- Tabla de variable structs ---")
        for key, value in self.variable_struct.items():
            print(key, value)
        print("--- Fin Tabla de variable structs ---")


    # FUNCIONES
    def add_func(self, id, params, instrucciones):
        self.funcs[id] = [id, params, instrucciones]

    def get_func(self, id):
        return self.funcs.get(id)

    def print_funcs(self):
        print("--- Tabla de funciones ---")
        for key, value in self.funcs.items():
            print(key, value)
        print("-------------------------")

    def copy(self):
        return tabla_simbolos(self.simbolos, self.structs, self.variable_struct, self.funcs)

    def add_funcion_print(self, name, parametros, entorno, linea, columna):
        dic = {}
        dic["id"] = name
        dic["tipo"] = "function("+",".join(parametros)+")"
        dic["entorno"] = entorno
        dic["linea"] = linea
        dic["columna"] = columna
        self.funciones_print.append(dic)

    def get_table(self):
        lista_simbolos = []
        for key,value in self.simbolos.items():
            valor = {}
            valor["id"] = key
            valor["tipo"] = value.tipo
            valor["entorno"] = value.entorno
            valor["linea"] = value.line
            valor["columna"] = value.col
            lista_simbolos.append(valor)
        lista_completa = lista_simbolos + self.funciones_print
        return lista_completa
