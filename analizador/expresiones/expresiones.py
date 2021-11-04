import sys, math

from analizador.write import write
sys.path.append('../')
from analizador.tabla_simbolos import simbolo, Tipo, tabla_simbolos
from analizador.error import error
from abc import ABC, abstractmethod

class expresion:

    valor = None
    label = 'expresion'
    truelbl = ''
    falselbl = ''

    @abstractmethod
    def interpretar(self):
        pass

class valorExpresion(expresion):

    def __init__(self, value, type, isTemp, true = '', false = ''):
        self.value = value
        self.type = type
        self.isTemp = isTemp
        self.truelbl = true
        self.falselbl = false

    def toString(self):
        if(self.type == Tipo.Array):
            return "[" + ",".join(str(e) for e in self.modificar_array(self.value)) + "]"
        else:
            return str(self.value)

    def modificar_array(self, array):
        aux = []
        for element in array:
            if(isinstance(element, list)):
                aux.append(self.modificar_array(element))
            else:
                aux.append(element.value)
        return aux
        

class validar_tipo_expresion(expresion):

    def __init__(self, expresion, tipo, linea, columna):
        self.expresion = expresion
        self.tipo = tipo
        self.linea = linea
        self.columna = columna
        self.auxType = ""
    
    def interpretar(self, wr):
        valor = self.expresion.interpretar(wr)
        if(isinstance(valor, (list, dict))):
            return valor
        if(self.tipo == valor.type.value or self.tipo == None):
            return valor
        else:
            error("se esperaba un valor de tipo '%s', se obtuvo '%s'"%(self.tipo, valor.type.value),"expresion con tipo", self.linea)
        
class expresion_primitiva(expresion):
    
    def __init__(self, valor, linea, columna):
        self.valor = valor
        self.tipo = None
        self.linea = linea
        self.columna = columna
    
    def interpretar(self, tabla_simbolos, wr:write):      
        tipo_dato = None
        valor_interpretado = self.valor
        if(type(self.valor) is str):
            if len(self.valor) == 0:
                return None      
            elif(self.valor.upper() == "TRUE"):
                if self.truelbl == "":
                    self.truelbl = f"L{wr.getLabel()}"
                if self.falselbl == "":
                    self.falselbl = f"L{wr.getLabel()}"
                wr.place_goto(self.truelbl);
                wr.place_goto(self.falselbl);
                return valorExpresion(1, Tipo.Bool, False, self.truelbl, self.falselbl)
                
            elif(self.valor.upper() == "FALSE"):
                if self.truelbl == "":
                    self.truelbl = f"L{wr.getLabel()}"
                if self.falselbl == "":
                    self.falselbl = f"L{wr.getLabel()}"
                wr.place_goto(self.falselbl);
                wr.place_goto(self.truelbl);
                return valorExpresion(0, Tipo.Bool, False, self.truelbl, self.falselbl)


            elif(self.valor[0] =="'" and len(self.valor) == 3 and self.valor[-1] == "'"):
                # CHAR VALIDO
                tipo_dato = Tipo.Char
                valor_interpretado = self.valor[1:-1]
            elif(self.valor[0] =="'" and len(self.valor) > 3 and self.valor[-1] == "'"):
                # CHAR INVALIDO
                error("sintaxis invalida", "expresion", self.linea)
            else:
                # agregar a heap
                temp = f"T{wr.getPointer()}"
                wr.place_operation(temp, "H", "", "")
                for ch in self.valor:
                    wr.insert_heap("H", ord(ch))
                    wr.next_heap()
                wr.insert_heap("H", -1)
                wr.next_heap()
                tipo_dato = Tipo.String
                valor_interpretado = temp

        elif type(self.valor) is int:
            # INT64 VALIDO
            tipo_dato = Tipo.Int64
            valor_interpretado = str(valor_interpretado) + ".0"

        elif type(self.valor) is float:
            # FLOAT64 VALIDO
            tipo_dato = Tipo.Float64
        else:
            error("tipo no definido","expresion", self.linea)
        
        return valorExpresion(valor_interpretado, tipo_dato, False)
        
class expresion_id(expresion):

    def __init__(self, valor, linea, columna):
        self.valor = valor
        self.linea = linea
        self.columna = columna

    def interpretar(self, tabla_simbolos, wr:write):
        valor = tabla_simbolos.get(self.valor)
        wr.comment("ACCESO ID")
        if (valor is not None):
            tempValue = f"T{wr.getPointer()}"
            tempos = valor.apuntador
            if tabla_simbolos.entorno is not None:
                tempos = f"T{wr.getPointer()}"
                wr.place_operation(tempos, "P", valor.apuntador, "+")
            wr.get_stack(tempValue,tempos)
            if valor.tipo == Tipo.Bool:
                if self.truelbl == "":
                    self.truelbl = f"L{wr.getLabel()}"
                if self.falselbl == "":
                    self.falselbl = f"L{wr.getLabel()}"

                wr.place_if(tempValue,1,"==",self.truelbl)
                wr.place_goto(self.falselbl)
                r = valorExpresion(tempValue, valor.tipo, False)
                r.truelbl = self.truelbl
                r.falselbl = self.falselbl
                return r
            else:
                return valorExpresion(tempValue, valor.tipo, False)
        else:
            error("variable %s no definida"%(self.valor), "expresion id", self.linea)

class expresion_binaria(expresion):
    
    def __init__(self, expI, operador, expD, linea, columna):
        self.expI = expI
        self.expD = expD
        self.operador = operador
        self.linea = linea
        self.columna = columna

    def interpretar(self, tabla_simbolos, wr:write):
        
        # operacion normal binaria
        if self.operador in ["+", "-", "*", "/"]:
            expI = self.expI.interpretar(tabla_simbolos,wr)
            expD = self.expD.interpretar(tabla_simbolos,wr)
            
            if self.operador == "+" and (expI.type == Tipo.String and expD.type == Tipo.String):
                t1 = f"T{wr.getPointer()}"
                temp1 = f"T{wr.getPointer()}"
                temp2 = f"T{wr.getPointer()}"
                size = tabla_simbolos.pos
                wr.place_operation(temp1, "P", size + 1, "+")
                wr.insert_stack(temp1, expI.value)
                wr.place_operation(temp2, temp1, 1, "+")
                wr.insert_stack(temp2, expD.value)
                wr.new_env(size)
                wr.addConcat()
                wr.call_function("concatNative")
                wr.get_stack(t1, "P")

                wr.return_evn(size)
                return valorExpresion(t1, Tipo.String, True)

            temp = f"T{wr.getPointer()}"
            wr.place_operation(temp, expI.value, expD.value, self.operador)
            
            if expI.type == Tipo.Float64 or expD.type == Tipo.Float64:
                return valorExpresion(temp, Tipo.Float64, True)
            if self.operador == "/":
                return valorExpresion(temp, Tipo.Float64, True)
            return valorExpresion(temp, Tipo.Int64, True)

        elif self.operador == "^":
            expI = self.expI.interpretar(tabla_simbolos,wr)
            expD = self.expD.interpretar(tabla_simbolos,wr)
            
            if expI.type == Tipo.String and expD.type == Tipo.Int64:
                t1 = f"T{wr.getPointer()}"
                temp1 = f"T{wr.getPointer()}"
                temp2 = f"T{wr.getPointer()}"
                size = tabla_simbolos.pos
                wr.place_operation(temp1, "P", size + 1, "+")
                wr.insert_stack(temp1, expI.value)
                wr.place_operation(temp2, temp1,1, "+")
                wr.insert_stack(temp2, expD.value)
                wr.new_env(size)
                wr.addRepeat()
                wr.call_function("repeatNative")
                wr.get_stack(t1, "P")

                wr.return_evn(size)
                return valorExpresion(t1, Tipo.String, True)

            elif expI.type == Tipo.Int64 and expD.type == Tipo.String:
                pass
            else:
                temp = f"T{wr.getPointer()}"
                wr.place_operation(temp, "P", 2, "+")
                wr.insert_stack(temp, expI.value)
                wr.place_operation(temp, temp, 1, "+")
                wr.insert_stack(temp, expD.value)
                wr.new_env(1)
                wr.call_function("potenNativeFunc")
                wr.get_stack(temp, "P")
                wr.return_evn(1)
                wr.addPotencia()
                return valorExpresion(temp, Tipo.Float64, True)

            

        elif self.operador in [">", "<", ">=", "<=", "==", "!="]:
            expI = self.expI.interpretar(tabla_simbolos,wr)
            if isinstance(expI,valorExpresion) is False:
                expI = self.expI.interpretar(tabla_simbolos,wr)
            ret = valorExpresion(None, Tipo.Bool, False)
            expD = None

            if expI.type != Tipo.Bool:
                expD = self.expD.interpretar(tabla_simbolos,wr)
                if isinstance(expD,valorExpresion) is False:
                    expD = self.expD.interpretar(tabla_simbolos,wr)
                    
                if (expI.type == Tipo.Int64 or expI.type == Tipo.Float64) and (expD.type == Tipo.Int64 or expD.type == Tipo.Float64):
                    if self.truelbl == '':
                        self.truelbl = f"L{wr.getLabel()}"
                    if self.falselbl == '':
                        self.falselbl = f"L{wr.getLabel()}"
                    wr.place_if(expI.value, expD.value, self.operador, self.truelbl)
                    wr.place_goto(self.falselbl)
                elif expD.type == Tipo.String and expD.type == Tipo.String:
                    print("Comparacion de cadenas")
            else:
                gotoDer = f"L{wr.getLabel()}"
                izqTemp = f"T{wr.getPointer()}"

                wr.place_label(expI.truelbl)
                wr.place_operation(izqTemp, "1", "", "")
                wr.place_goto(gotoDer)

                wr.place_label(expI.falselbl)
                wr.place_operation(izqTemp, "0","","")
                wr.place_label(gotoDer)

                expD = self.expD.interpretar(tabla_simbolos,wr)
                if isinstance(expD,valorExpresion) is False:
                    expD = self.expD.interpretar(tabla_simbolos,wr)
                if expD.type != Tipo.Bool:
                    print("No comparable")
                final = f"L{wr.getLabel()}"
                derTemp = f"T{wr.getPointer()}"
                wr.place_label(expD.truelbl)
                wr.place_operation(derTemp, "1", "", "")
                wr.place_goto(final)
                wr.place_label(expD.falselbl)
                wr.place_operation(derTemp, "0", "", "")
                wr.place_label(final)
                if self.truelbl == '':
                        self.truelbl = f"L{wr.getLabel()}"
                if self.falselbl == '':
                    self.falselbl = f"L{wr.getLabel()}"
                wr.place_if(izqTemp,derTemp, self.operador, self.truelbl)
                wr.place_goto(self.falselbl)
            ret.truelbl = self.truelbl
            ret.falselbl = self.falselbl
            return ret

        elif self.operador in ["||", "&&"]:
            wr.comment("EXPRESION RELACIONAL")
            if self.truelbl == '':
                        self.truelbl = f"L{wr.getLabel()}"
            if self.falselbl == '':
                self.falselbl = f"L{wr.getLabel()}"
            etiqueta = ''
            
            if self.operador == "&&":
                etiqueta = f"L{wr.getLabel()}"
                self.expI.truelbl = etiqueta
                self.expD.truelbl = self.truelbl
                self.expI.falselbl = self.falselbl
                self.expD.falselbl = self.falselbl
                
            elif self.operador == "||":
                etiqueta = f"L{wr.getLabel()}"
                self.expI.truelbl = self.truelbl
                self.expD.truelbl = self.truelbl
                etiqueta = f"L{wr.getLabel()}"
                self.expI.falselbl = etiqueta
                self.expD.falselbl = self.falselbl
            else:
                print("NOT")
            expI = self.expI.interpretar(tabla_simbolos,wr)
            if isinstance(expI,valorExpresion) is False:
                expI = self.expI.interpretar(tabla_simbolos,wr)
            if expI.type != Tipo.Bool:
                print("ERROR")
                return
            wr.place_label(etiqueta)
            expD:valorExpresion = self.expD.interpretar(tabla_simbolos,wr)
            if isinstance(expD,valorExpresion) is False:
                expD = self.expD.interpretar(tabla_simbolos,wr)
            
            r = valorExpresion(None, Tipo.Bool, False)
            r.truelbl = self.truelbl
            r.falselbl = self.falselbl
            return r
            

class expresion_nativa(expresion):
    def __init__(self, funcion, expresion, linea, columna):
        self.funcion = funcion
        self.expresion = expresion
        self.linea = linea
        self.columna = columna
    
    def interpretar(self, tabla_simbolos, wr:write):
        exp = self.expresion.interpretar(tabla_simbolos, wr)
        
        if isinstance(exp,list):
            exp = valorExpresion(exp, Tipo.Array)
        valor = exp.value
        tipo = exp.type
        # LOG10
        if(self.funcion == "log10"):
            if(tipo == Tipo.Int64 or tipo == Tipo.Float64):
                return valorExpresion(math.log10(valor), Tipo.Float64)
            else:
                #ERROR TIPOS
                error("valor no admitido para funcion %s: '%s'"%(self.funcion,tipo.value), "funcion nativa", self.linea)
        if(self.funcion == "sin"):
            if(tipo == Tipo.Int64 or tipo == Tipo.Float64):
                return valorExpresion(math.sin(valor), Tipo.Float64)
            else:
                #ERROR TIPOS
                error("valor no admitido para funcion %s: '%s'"%(self.funcion,tipo.value), "funcion nativa", self.linea)
        if(self.funcion == "cos"):
            if(tipo == Tipo.Int64 or tipo == Tipo.Float64):
                return valorExpresion(math.cos(valor), Tipo.Float64)
            else:
                #ERROR TIPOS
                error("valor no admitido para funcion %s: '%s'"%(self.funcion,tipo.value), "funcion nativa", self.linea)
        if(self.funcion == "tan"):
            if(tipo == Tipo.Int64 or tipo == Tipo.Float64):
                return valorExpresion(math.tan(valor), Tipo.Float64)
            else:
                #ERROR TIPOS
                error("valor no admitido para funcion %s: '%s'"%(self.funcion,tipo.value), "funcion nativa", self.linea)
        if(self.funcion == "sqrt"):
            if(tipo == Tipo.Int64 or tipo == Tipo.Float64):
                return valorExpresion(math.sqrt(valor), Tipo.Float64)
            else:
                #ERROR TIPOS
                error("valor no admitido para funcion %s: '%s'"%(self.funcion,tipo.value), "funcion nativa", self.linea)
        if(self.funcion == "float"):
            if(tipo == Tipo.Int64 or tipo == Tipo.Float64):
                return valorExpresion(float(valor), Tipo.Float64)
            else:
                #ERROR TIPOS
                error("valor no admitido para funcion %s: '%s'"%(self.funcion,tipo.value), "funcion nativa", self.linea)
        if(self.funcion == "string"):
            if(tipo == Tipo.Int64 or tipo == Tipo.Float64 or tipo == Tipo.String or tipo == Tipo.Bool or tipo == Tipo.Char or tipo == Tipo.Nothing):
                return valorExpresion(str(valor), Tipo.String)
            else:
                #ERROR TIPOS
                error("valor no admitido para funcion %s: '%s'"%(self.funcion,tipo.value), "funcion nativa", self.linea)
        if(self.funcion == "typeof"):
            if(tipo == Tipo.Int64 or tipo == Tipo.Float64 or tipo == Tipo.String or tipo == Tipo.Bool or tipo == Tipo.Char or tipo == Tipo.Nothing):
                return valorExpresion(tipo.value, Tipo.String)
            else:
                #ERROR TIPOS
                error("valor no admitido para funcion %s: '%s'"%(self.funcion,tipo.value), "funcion nativa", self.linea)
        if(self.funcion == "length"):
            return valorExpresion(len(exp.value), Tipo.Int64)
        if(self.funcion == "trunc"):
            return valorExpresion(float(int(valor)), Tipo.Float64)
        if(self.funcion == "uppercase"):
            if tipo != Tipo.String:
                return error("valor no admitido para funcion %s: '%s'"%(self.funcion,tipo.value), "funcion nativa", self.linea)
            else:
                t1 = f"T{wr.getPointer()}"
                temp1 = f"T{wr.getPointer()}"
                size = tabla_simbolos.pos
                wr.place_operation(temp1, "P", size + 1, "+")
                wr.insert_stack(temp1, exp.value)
                wr.new_env(size)
                wr.addUpper()
                wr.call_function("upperNative")
                wr.get_stack(t1, "P")

                wr.return_evn(size)
                return valorExpresion(t1, Tipo.String, True)
        if(self.funcion == "lowercase"):
            if tipo != Tipo.String:
                return error("valor no admitido para funcion %s: '%s'"%(self.funcion,tipo.value), "funcion nativa", self.linea)
            else:
                t1 = f"T{wr.getPointer()}"
                temp1 = f"T{wr.getPointer()}"
                size = tabla_simbolos.pos
                wr.place_operation(temp1, "P", size + 1, "+")
                wr.insert_stack(temp1, exp.value)
                wr.new_env(size)
                wr.addLower()
                wr.call_function("lowerNative")
                wr.get_stack(t1, "P")

                wr.return_evn(size)
                return valorExpresion(t1, Tipo.String, True)


class expresion_nativa_log(expresion):
    def __init__(self, op,expresion1, expresion2, linea, columna):
        self.op = op
        self.expresion1 = expresion1
        self.expresion2 = expresion2
        self.linea = linea
        self.columna = columna
    
    def interpretar(self,  entorno = "Global"):
        
        if(self.op == "log"):
            exp1 = self.expresion1.interpretar(tabla_simbolos)
            exp2 = self.expresion2.interpretar(tabla_simbolos)
            valor1 = exp1.value
            tipo1 = exp1.type
            valor2 = exp2.value
            tipo2 = exp2.type

            # LOG
            if((tipo1 == Tipo.Int64 or tipo1 == Tipo.Float64) and (tipo2 == Tipo.Int64 or tipo2 == Tipo.Float64)):
                return valorExpresion(math.log(valor2,valor1), Tipo.Float64)
            else:
                #ERROR TIPOS
                error("valores no admitidos para funcion log: '%s' y 'y '%s"%(tipo1.value, tipo2.value), "funcion nativa", self.linea)
        elif(self.op == "parse"):
            exp2 = self.expresion2.interpretar(tabla_simbolos)
            valor2 = exp2.value
            tipo2 = exp2.type
            if isinstance( self.expresion1, str):
                if(self.expresion1 == "Int64"):
                    if(tipo2 == Tipo.String):
                        return valorExpresion(int(valor2), Tipo.Int64)
                    else:
                        error("tipo de parametro invalido para funcion '%s', se esperaba '%s'"%(self.op,Tipo.String.value), "funcion nativa", self.linea)
                elif(self.expresion1 == "Float64"):
                    if(tipo2 == Tipo.String):
                        return valorExpresion(float(valor2), Tipo.Float64)
                    else:
                        error("tipo de parametro invalido para funcion '%s', se esperaba '%s'"%(self.op,Tipo.String.value), "funcion nativa", self.linea)
                else:
                    error("tipo de parametro invalido para funcion '%s', se esperaba '%s' o '%s'"%(self.op, Tipo.Int64.value, Tipo.Float64.value), "funcion nativa", self.linea)                    
            else:
                error("tipo de parametro invalido para funcion '%s', se esperaba '%s' o '%s'"%(self.op, Tipo.Int64.value, Tipo.Float64.value), "funcion nativa", self.linea)                    
        elif(self.op == "trunc"):
            exp2 = self.expresion2.interpretar(tabla_simbolos)
            valor2 = exp2.value
            tipo2 = exp2.type
            if isinstance( self.expresion1, str):
                if(self.expresion1 == "Int64"):
                    if(tipo2 == Tipo.Int64 or tipo2 == Tipo.Float64):
                        return valorExpresion(int(valor2), Tipo.Int64)
                    else:
                        error("tipo de parametro invalido para funcion '%s', se esperaba '%s'"%(self.op,Tipo.Float64), "funcion nativa", self.linea)
                else:
                    error("tipo de parametro invalido para funcion '%s', se esperaba '%s'"%(self.op, Tipo.Int64.value), "funcion nativa", self.linea)                    
            else:
                error("tipo de parametro invalido para funcion '%s', se esperaba '%s'"%(self.op, Tipo.Int64.value), "funcion nativa", self.linea)

class expresion_array(expresion):
    def __init__(self, expresiones, linea, columna):
        self.expresiones = expresiones
        self.linea = linea
        self.columna = columna

    def countDim(self, ar):
        dim = 1
        last = 0
        for i in ar:
            if isinstance(i, list):
                count = self.countDim(i)
                if count > last:
                    last = count
        return dim + last


    def interpretar(self, tabla_simbolos, wr:write):
        dim = 1
        last = 0
        
        for i in self.expresiones:
            if isinstance(i, list):
                count = self.countDim(i)
                if count > last:
                    last = count
        dim += last

        t1 = f"T{wr.getPointer()}"
        wr.place_operation(t1, "H")
        wr.insert_heap(t1, dim)
        wr.next_heap()
        wr.insert_heap("H", 0)
        wr.next_heap()
        wr.insert_heap("H", len(self.expresiones) - 1)
        wr.next_heap()
        for i in self.expresiones:
            valor = i.interpretar(tabla_simbolos, wr)
            wr.insert_heap("H", valor.value)
            wr.next_heap()
        return valorExpresion(t1, Tipo.Array, True)



class expresion_acceso_array(expresion):
    def __init__(self, id, posicion, linea, columna):
        self.id = id
        self.posicion = posicion
        self.linea = linea
        self.columna = columna

    def interpretar(self,  entorno = "Global"):
        simbolo = tabla_simbolos.get(self.id)
        array = simbolo.valor
        if(array is None):
            error("variable %s no definida"%(self.valor), "expresion array posicion", self.linea)
        if(isinstance(array, list) is not True):
            error("variable '%s' no es de tipo array, no puede ser accesada por posicion"%(self.id), "acceso array", self.linea)
        
        posiciones = []
        for pos in self.posicion:
            posicion = pos.interpretar(tabla_simbolos)
            if(posicion.type != Tipo.Int64):
                error("se esperaba una posicion de tipo 'Int64' se obutvo '%s'"%(posicion.type.value), "acceso array", self.linea)
                break
            posiciones.append(posicion.value)
        
        nivel = array
        contador = 1
        for pos in posiciones:

            if(pos == posiciones[-1] and contador == len(posiciones)):
                if(len(nivel) < pos):
                    error("posicion '%s' fuera de los limites del array"%(pos), "acceso array", self.linea)
                if(isinstance(nivel, list)):
                    return nivel[pos-1]
                else:
                    #ERROR
                    return valorExpresion(nivel.value, nivel.type)
            else:
                if(len(nivel) < pos):
                    error("posicion '%s' fuera de los limites del array"%(pos), "acceso array", self.linea)
                if(isinstance(nivel, list) is not True):
                    error("el valor accesado '%s' no es de tipo array, valor '%s'"%(self.id. pos), "acceso array", self.linea)
                else:
                    nivel = nivel[pos-1]
            contador+= 1

class expression_array_range(expresion):
    def __init__(self, id, range, linea, columna):
        self.id = id
        self.range = range
        self.linea = linea
        self.columna = columna
    def interpretar(self,  entorno = "Global"):
        simbolo = tabla_simbolos.get(self.id)
        posiciones = self.range.interpretar(tabla_simbolos)
        array = simbolo.valor
        if(array is None):
            error("variable %s no definida"%(self.valor), "expresion array posicion", self.linea)
        if(isinstance(array, list) is not True):
            error("variable '%s' no es de tipo array, no puede ser accesada por posicion"%(self.id), "acceso array", self.linea)
        
        if posiciones[0] < 1:
            error("rango no puede ser negativo '%s'"%(posiciones[0]),"acceso array", self.linea)
        if posiciones[-1] > len(array):
            error("indice fuera de rango '%s'"%(posiciones[-1]),"acceso array", self.linea)

        valores = []
        for pos in posiciones:
            valores.append(array[pos-1])
           
        return valorExpresion(valores, Tipo.Array)

class expresion_range(expresion):
    def __init__(self, expresionIzq, expresionDer, linea, columna):
        self.expI = expresionIzq
        self.expD = expresionDer
        self.linea = linea
        self.columna = columna
    
    def interpretar(self, tabla_simbolos, entorno = "Global"):
        expI = self.expI.interpretar(tabla_simbolos)
        expD = self.expD.interpretar(tabla_simbolos)
        valorI = expI.value
        valorD = expD.value
        tipoI = expI.type
        tipoD = expD.type
        if((tipoI != Tipo.Int64 and tipoI != Tipo.Float64) or (tipoD != Tipo.Int64 and tipoD != Tipo.Float64)):
            error("valores incorrectos para construir un rango se esperaban valores de tipo 'Int64' o 'Float64'",'rango', self.linea);
        valores = []
        contador  = valorI
        while valorI <= valorD:
            valores.append(contador)
            contador+=1
            valorI +=1
        return valores

class expresion_nothing(expresion):
    def __init__(self):
        pass

    def interpretar(self, tabla_simbolos, entorno = "Global"):
        return valorExpresion(None, Tipo.Nothing)

class expresion_acceso_struct(expresion):

    def __init__(self, id, prop, linea, columna):
        self.id = id
        self.prop = prop
        self.linea = linea
        self.columna = columna
    
    def interpretar(self, tabla_simbolos, entorno = "Global"):
        valor_interpretado = tabla_simbolos.get(self.id)
        if(valor_interpretado):
            if valor_interpretado.tipo == Tipo.Struct : 
                if(self.prop[0] in valor_interpretado.valor.keys()):
                        if len(self.prop) == 1:
                            if  isinstance(valor_interpretado.valor[self.prop[0]], dict) :
                                return valorExpresion(valor_interpretado.valor[self.prop[0]], valor_interpretado.valor[self.prop[0]].type)
                            else:
                                return valorExpresion(valor_interpretado.valor[self.prop[0]].value, valor_interpretado.valor[self.prop[0]].type)
                        elif len(self.prop) > 1:
                            nuevo_valor = valor_interpretado.valor[self.prop[0]]
                            if isinstance(nuevo_valor, dict):
                                # INTERPRETAR STRUCT ANIDADO

                                #VERIFICAR SI EXISTE ESE STRUCT
                                struct = nuevo_valor["id_struct"]
                                parametros = nuevo_valor["parametros"]

                                struct = tabla_simbolos.get_struct(struct)
                                if(struct is None):
                                    error("tipo de struct no definido '%s'"%(struct), "construccion struct", self.linea)
                                if len(parametros) != len(struct[2]):
                                    error("numero de parametros incorrecto '%s'"%(struct), "construccion struct", self.linea)

                                #INTERPRETAR LOS VALORES PARA CREARLO
                                valores = []
                                for val in parametros:
                                    try:
                                        valor = val.interpretar(tabla_simbolos)
                                        valores.append(valor)
                                    except Exception as e:
                                        valores.append(val)
                                
                                count = 0

                                valores_struct = {}
                                while count < len(valores):
                                    if (isinstance(valores[count], list)):
                                        if(struct[2][count][1] == None or struct[2][count][1] == Tipo.Array.value):
                                            valores_struct[struct[2][count][0]] = valores[count]
                                        else:
                                            error("tipo de parametro invalido para construccion de struct '%s', parametro '%s' se esperaba un valor de tipo'%s'"%(struct,struct[2][count][0], struct[2][count][1]), "construcion struct", self.linea)
                                        count += 1
                                    elif(struct[2][count][1] == None or struct[2][count][1] == valores[count].type.value):
                                        valores_struct[struct[2][count][0]] = valores[count]
                                    else:
                                        error("tipo de parametro invalido para construccion de struct '%s', parametro '%s' se esperaba un valor de tipo'%s'"%(struct,struct[2][count][0], struct[2][count][1]), "construcion struct", self.linea)
                                    count += 1

                                valores_struct["__tipo_struct"] = valorExpresion(struct, Tipo.String)
                                nuevo_valor = valores_struct
                            elif isinstance(nuevo_valor, valorExpresion):
                                #struct ya interpretado
                                if nuevo_valor.type == Tipo.Struct : 
                                    nuevo_valor = nuevo_valor.value
                                else:
                                    error("variable %s no es de tipo struct"%(self.id), "acceso struct", self.linea)
                            for prop in self.prop[1:]:
                                if isinstance(nuevo_valor, dict):
                                    if(prop in nuevo_valor.keys()):
                                        nuevo_valor[prop]
                                        if prop == self.prop[-1]:
                                            return valorExpresion(nuevo_valor[prop].value, nuevo_valor[prop].type)
                                    else:
                                        # PROP NO EXISTE
                                        tipo_struct = tabla_simbolos.get_variable_struct(self.id)
                                        error("struct %s no tiene el campo '%s'"%(self.id, tipo_struct), "acceso estruct", self.linea)
                                else:
                                    print('\x1b[6;30;41m' + 'ERROR!' + '\x1b[0m')
                else:
                    # PROP NO EXISTE
                    tipo_struct = tabla_simbolos.get_variable_struct(self.id)
                    error("struct %s no tiene el campo '%s'"%(self.id, tipo_struct), "acceso estruct", self.linea)
                
            else:
                error("variable %s no es de tipo struct"%(self.id), "acceso struct", self.linea)    
            #return valorExpresion(valor_interpretado.valor, valor_interpretado.tipo)
        else:
            error("variable %s no definida"%(self.id), "acceso struct", self.linea)