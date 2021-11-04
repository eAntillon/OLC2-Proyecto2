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
    tipo: Tipo
    apuntador: int
    line: int
    col: int

    def __init__(self, id, tipo, apuntador, isGlobal, isHeap, tipoStruct):
        self.id = id
        self.tipo = tipo    
        self.apuntador = apuntador
        self.isGlobal = isGlobal
        self.inHeap = isHeap
        self.structType = tipoStruct

    def print(self):
        print("id: ",self.id, ", tipo: ", self.tipo.value, "apuntador: ", self.apuntador)
    
    def toString(self):
        return "id: %s, tipo: %s, apuntador: %s"%(self.id, self.tipo.value, self.apuntador)

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

    simbolos = {} # DICT CON VARIABLES
    structs = {} # INFORMACION DE STRUCTS
    variable_struct = {} # VARIABLES Y SU TIPO DE STRUCT
    funcs = {} # FUNCIONES
    funciones_print = []
    cicloInicio = ""
    cicloFinal = ""
    returnlbl = ""

    entorno = None

    def __init__(self, ts = None):
        if ts is not None:
            self.simbolos = ts.simbolos
            self.structs = ts.structs
            self.variable_struct = ts.variable_struct
            self.funcs =ts.funcs
            self.funciones_print =ts.funciones_print
            self.pos = ts.pos
            self.cicloInicio = ts.cicloInicio
            self.cicloFinal = ts.cicloFinal
            self.returnlbl = ts.returnlbl
            self.entorno = True
        else:
            self.simbolos = {} # DICT CON VARIABLES
            self.structs = {} # INFORMACION DE STRUCTS
            self.variable_struct = {} # VARIABLES Y SU TIPO DE STRUCT
            self.funcs = {} # FUNCIONES
            self.funciones_print = []
            self.pos = 1
            self.cicloInicio = ""
            self.cicloFinal = ""
            self.returnlbl = ""


    def newEnv(self, nombre):
        self.entorno = nombre

    def returnEnv(self):
        self.entorno = None

    def add(self, id, tipo, inHeap, strucType = ""):
        simb = simbolo(id,tipo, self.pos, (self.entorno == None), inHeap, strucType)
        self.simbolos[simb.id] = simb
        self.pos += 1
        
    
    def get(self, id):
        ''' Retorna el simbolo si existe, sino devuelve None'''
        return self.simbolos.get(id, None)
    
    def addFunc(self, id):
        self.funcs[id] = id

    def getFunc(self, id):
        return self.funcs.get(id, None)

    def getPos(self):
        return self.pos

    def update(self, id, tipo):
        if(id in self.simbolos.keys()):
            simb = self.simbolos[id]
            simb.tipo = tipo
            self.simbolos.update({id : simb})
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
        self.simbolos_ent = {}
        self.simbolos = {}
        self.structs = {} # INFORMACION DE STRUCTS
        self.variable_struct = {} # VARIABLES Y SU TIPO DE STRUCT
        self.funcs = {} # FUNCIONES

    def print(self):
        print("--- Tabla de simbolos ---")
        if len(cls.simbolos) > 0:
            for s in cls.simbolos.values():
                print(" ->", s.toString())
        else:
            print("Tabla vacia")
        print("-------------------------")
        #self.print_structs()
        #self.print_funcs()
        #self.print_variable_struct()