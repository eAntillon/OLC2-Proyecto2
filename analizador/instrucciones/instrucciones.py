from re import S
from analizador.expresiones.expresiones import valorExpresion, expresion
import sys
sys.path.append('../')
from analizador.tabla_simbolos import simbolo, Tipo, tabla_simbolos as  ts
from analizador.write import write
from abc import ABC, abstractmethod
from analizador.error import ContinueError, ReturnError, error, BreakError
import traceback

class instruccion():

    @abstractmethod
    def interpretar(self):
        pass

class asignacion(instruccion):

    def __init__(self, id: str, expresion, linea: int, columna: int):
        self.id = id
        self.expresion = expresion
        self.linea = linea
        self.columna = columna

    def interpretar(self, tabla_simbolos, wr:write):
       
        # ASIGNAR EXPRESION
        expresion = self.expresion.interpretar(tabla_simbolos,wr)
        existance:simbolo = tabla_simbolos.get(self.id)
        # AGregar un simbolo nuevo
        if existance is not None:
            wr.insert_stack(existance.apuntador,expresion.value)
        else:
            tabla_simbolos.add(self.id, expresion.type, (expresion.type == Tipo.String or expresion.type == Tipo.Struct))
            expresion1 = tabla_simbolos.get(self.id)
            pos = tabla_simbolos.getPos()
            temp = f"L{wr.getLabel()}"
            if tabla_simbolos.entorno is not None:
                pos = f"T{wr.getPointer()}"
                wr.place_operation(pos, "P", expresion1.apuntador, "+")

            if expresion.type == Tipo.Bool:
                
                wr.place_label(expresion.truelbl)
                wr.insert_stack(pos,1)
                wr.place_goto(temp)
                wr.place_label(expresion.falselbl)
                wr.insert_stack(pos,0)
                wr.place_label(temp)
            else:
                wr.insert_stack(pos,expresion.value)
            # id, tipo, inHeap, strucType = ""

class asignacion_array(instruccion):
    def __init__(self, id: str, expresiones, linea: int, columna: int):
        self.id = id
        self.expresiones = expresiones
        self.line = linea
        self.col = columna

    def interpretar(self, tabla_simbolos, entorno = "Global"):
        existance = tabla_simbolos.get(self.id)
        valor = self.expresiones.interpretar(tabla_simbolos)

        s = simbolo(self.id, valor, Tipo.Array, entorno, self.line, self.col)
        if existance is None:
            # Agregar nuevo simbolo
            tabla_simbolos.add(s)
        else:
            # Actualizar valor
            tabla_simbolos.update(s)
        
class asignacion_array_posicion(instruccion):
    def __init__(self, id: str, posiciones, expresion, linea: int, columna: int):
        self.id = id
        self.posiciones = posiciones
        self.expresion = expresion
        self.line = linea
        self.col = columna

    def modificar_array(self, ar, indexes, valor):
        mod = ar
        if(len(indexes) == 1):
            mod[indexes[0]] = valor
            return mod
        else:
            mod[indexes[0]] = self.modificar_array(mod[indexes[0]], indexes[1:],valor)
            return mod

    def interpretar(self, tabla_simbolos, entorno = "Global"):
        
        # GET ARRAY ID
        simbolo_array = tabla_simbolos.get(self.id)
        if(simbolo_array is None):
            error("variable %s no definida"%(self.valor), "expresion array posicion", self.line)
        if(simbolo_array.tipo != Tipo.Array):
            error("variable '%s' no es de tipo array, no puede ser accesada por posicion"%(self.id), "acceso array", self.line)
        
        # VALOR EXPRESION
        valor = self.expresion.interpretar(tabla_simbolos)

        #VALORES POSICIONES
        posiciones = []
        for pos in self.posiciones:
            pos = pos.interpretar(tabla_simbolos)
            if(pos.type != Tipo.Int64):
                error("valor de posicion invalido se esperaba un valor de tipo 'Int64',  se obtuvo %s"%(pos.type),"acceso array", self.line)
                break
            posiciones.append(pos.value-1)
        #NUEVO ARRAY
        copia_array = simbolo_array.valor
        nivel = copia_array
        #VERIFICAR INDICES
        for pos in posiciones:    
            if(pos > len(nivel)):
                error("posicion '%s' fuera de los limites del array"%(pos), "acceso array", self.line)
            if(isinstance(nivel, list) is not True):
                error("el valor en posicion '%s' no es de tipo array, no puede ser accesada por posicion"%(pos), "acceso array", self.line)
            else:
                nivel = nivel[pos]
        #print(copia_array, posiciones)
        nuevo_ar = self.modificar_array(copia_array, posiciones, valor)
        #print(nuevo_ar)
        s = simbolo(self.id, nuevo_ar, Tipo.Array, entorno, self.line, self.col)
        # Actualizar valor
        tabla_simbolos.update(s)

class instruccion_if(instruccion):

    def __init__(self, expresion, instrucciones, instruccion_elseif, instrucciones_else, linea, columna):
        self.expresion = expresion
        self.instrucciones = instrucciones
        self.instruccion_elseif = instruccion_elseif
        self.instrucciones_else = instrucciones_else
        self.line = linea
        self.columna = columna

    def insertar_elseif(self, instrucciones):
        self.instrucciones_elseif = instrucciones
    
    def insertar_else(self, instrucciones):
        self.instrucciones_else = instrucciones

    def interpretar(self, tabla_simbolos, wr:write):
        valor_expresion = self.expresion.interpretar(tabla_simbolos,wr)
        if(valor_expresion.type != Tipo.Bool):
            error("se esperaba una expresion de tipo 'Boolean', se obtuvo '%s'"%(valor_expresion.type), "instruccion if", self.line)
        
        wr.comment("INSTRUCCION IF")

        salida = f"L{wr.getLabel()}"
        wr.place_label(valor_expresion.truelbl)
        for instruccion in self.instrucciones:
            # try:
            instruccion.interpretar(tabla_simbolos,wr)
            
        wr.place_goto(salida)
        wr.place_label(valor_expresion.falselbl)
        if(self.instruccion_elseif is not None):
            self.instruccion_elseif.interpretar(tabla_simbolos,wr)
            for inst in self.instrucciones_else:
                inst.interpretar(tabla_simbolos,wr)
            wr.place_label(salida)
        else:
            for inst in self.instrucciones_else:
                inst.interpretar(tabla_simbolos,wr)
            wr.place_label(salida)

class instruccion_while(instruccion):
    def __init__(self, expresion, instrucciones, linea, columna):
        self.expresion = expresion
        self.instrucciones = instrucciones
        self.linea = linea
        self.columna = columna 

    def interpretar(self, tabla_simbolos, wr:write):
        wr.comment("INSTRUCCION WHILE")
        inicio = f"L{wr.getLabel()}"
        wr.place_label(inicio)

        valor = self.expresion.interpretar(tabla_simbolos,wr)
        print("VALOR", valor)

        tabla_simbolos = ts(tabla_simbolos)
        tabla_simbolos.cicloInicio = inicio

        tabla_simbolos.cicloFinal = valor.falselbl

        if(valor.type != Tipo.Bool):
            error("se esperaba una expresion de tipo 'Boolean', se obtuvo '%s'"%(valor.type), "instruccion while", self.linea)

        wr.place_label(valor.truelbl)
        for inst in self.instrucciones:
                inst.interpretar(tabla_simbolos,wr)
        wr.place_goto(inicio)
        wr.place_label(valor.falselbl)
        tabla_simbolos.cicloInicio = ""
        tabla_simbolos.cicloFinal = ""

class instruccion_for(instruccion):
    def __init__(self, id, expresion, instrucciones,tipo, linea, columna):
        self.id = id
        self.expresion = expresion
        self.instrucciones = instrucciones
        self.tipo = tipo
        self.line = linea
        self.col = columna

    def interpretar(self, tabla_simbolos, entorno = "Global"):
        # FOR RANGE
        if self.tipo == "range":
            
            posiciones = self.expresion.interpretar(tabla_simbolos)
            if(len(posiciones) > 0):
                exp = valorExpresion(posiciones[0], Tipo.Int64)
                sim = simbolo(self.id, exp.value, Tipo.Int64, entorno, self.line, self.col)
                tabla_simbolos.add(sim)
                for i in posiciones:
                    try:
                        if(i != posiciones[0]):
                            exp = valorExpresion(i, Tipo.Int64)
                            sim = simbolo(self.id, exp.value, Tipo.Int64, entorno, self.line, self.col)
                            tabla_simbolos.update(sim)
                        for instruccion in self.instrucciones:
                            try:
                                instruccion.interpretar(tabla_simbolos)
                            except BreakError:
                                raise BreakError()
                            except ContinueError:
                                raise ContinueError()
                    except BreakError:
                        break
                    except ContinueError:
                        continue
            else:
                return
        elif self.tipo == "array":
            array = self.expresion.interpretar(tabla_simbolos)
            if(isinstance(array, list)):
                if(len(array) > 0):
                    exp = array[0]
                    sim = simbolo(self.id, exp.value, exp.type, entorno, self.line, self.col)
                    tabla_simbolos.add(sim)
                    for i in array:
                        try:
                            if(i != array[0]):
                                exp = i
                                if(isinstance(i, list)):
                                    sim = simbolo(self.id, i, Tipo.Array, entorno, self.line, self.col)
                                    tabla_simbolos.update(sim)
                                else:
                                    sim = simbolo(self.id, exp.value, exp.type, entorno, self.line, self.col)
                                    tabla_simbolos.update(sim)
                            for instruccion in self.instrucciones:
                                try:
                                    instruccion.interpretar(tabla_simbolos)
                                except BreakError:
                                    raise BreakError()
                                except ContinueError:
                                    raise ContinueError()
                        except BreakError:
                            break
                        except ContinueError:
                            continue
        elif self.tipo == "expresion":
            valor = self.expresion.interpretar(tabla_simbolos)
            
            posicion = 0
            if(valor.type == Tipo.String):
                if(len(valor.value) > 0):
                    exp = valor.value[0]
                    sim = simbolo(self.id, exp, valor.type, entorno, self.line, self.col)
                    tabla_simbolos.add(sim)
                    for i in valor.value:
                        try:
                            if(posicion > 0):
                                exp = i
                                if(isinstance(i, list)):
                                    sim = simbolo(self.id, i, Tipo.Array, entorno, self.line, self.col)
                                    tabla_simbolos.update(sim)
                                else:
                                    sim = simbolo(self.id, exp, valor.type, entorno, self.line, self.col)
                                    tabla_simbolos.update(sim)
                            for instruccion in self.instrucciones:
                                try:
                                    instruccion.interpretar(tabla_simbolos)
                                except BreakError:
                                    raise BreakError()
                                except ContinueError:
                                    raise ContinueError()
                            posicion += 1
                        except BreakError:
                            break
                        except ContinueError:
                            continue
            elif valor.type == Tipo.Array:
                array = valor.value
                if(len(array) > 0):
                    exp = array[0]
                    if isinstance(exp,list):
                        sim = simbolo(self.id, exp, Tipo.Array, entorno, self.line, self.col)
                    else:
                        sim = simbolo(self.id, exp.value, exp.type, entorno, self.line, self.col)
                    tabla_simbolos.add(sim)
                    for i in array:
                        try:
                            if(i != array[0]):
                                exp = i
                                if(isinstance(i, list)):
                                    sim = simbolo(self.id, i, Tipo.Array, entorno, self.line, self.col)
                                    tabla_simbolos.update(sim)
                                else:
                                    sim = simbolo(self.id, exp.value, exp.type, entorno, self.line, self.col)
                                    tabla_simbolos.update(sim)
                            for instruccion in self.instrucciones:
                                try:
                                    instruccion.interpretar(tabla_simbolos)
                                except BreakError:
                                    raise BreakError()
                                except ContinueError:
                                    raise ContinueError()
                        except BreakError:
                            break
                        except ContinueError:
                            continue

class instruccion_print(instruccion):
    def __init__(self, expresiones, tipo):
        self.expresiones = expresiones
        self.tipo = tipo

    def interpretar(self, tabla_simbolos, wr:write):
        for expresion in self.expresiones:
            v:valorExpresion = expresion.interpretar(tabla_simbolos,wr)
            print(v)
            wr.comment("PRINT")
            if v.type == Tipo.String:
                wr.insert_stack(0, v.value)
                wr.insert_code("printString();")
            elif v.type == Tipo.Bool:
                temp = f"L{wr.getLabel()}"
                wr.place_label(v.truelbl)
                wr.print_true()

                wr.place_goto(temp)
                wr.place_label(v.falselbl)
                wr.print_false()
                wr.place_label(temp)

            elif v.type == Tipo.Int64:
                wr.place_print("d", v.value)
            elif v.type == Tipo.Float64:
                wr.place_print("f", v.value)
        if self.tipo == "println":
            wr.place_print("c", 10)

class instruccion_break(instruccion):
    def __init__(self, linea, columna): 
        self.linea = linea
        self.columna = columna 
    
    def interpretar(self, tabla_simbolos, wr:write):
        wr.place_goto(tabla_simbolos.cicloFinal)

class instruccion_continue(instruccion):

    def __init__(self, linea, columna): 
        self.linea = linea
        self.columna = columna 
    
    def interpretar(self, tabla_simbolos, wr:write):
        wr.place_goto(tabla_simbolos.cicloInicio)  

class definicion_struct(instruccion):

    def __init__(self,tipo, id, parametros, linea, columna): 
        self.tipo = tipo
        self.id = id
        self.parametros = parametros
        self.linea = linea
        self.columna = columna 
    
    def interpretar(self, entorno = "Global"):
        if(tabla_simbolos.get(self.id) == None and tabla_simbolos.get_struct(self.id) == None):
            if self.tipo == None:
                tabla_simbolos.add_struct(False , self.id, self.parametros)
            else:
                tabla_simbolos.add_struct(True , self.id, self.parametros)
        else:
            error("no es posible redefinir la constante '%s'"%(self.id), 'struct', self.linea)

class asignacion_prop_struct(instruccion):
    def __init__(self, id, prop, expresion, linea, columna):
        self.id = id
        self.prop = prop
        self.expresion = expresion
        self.linea = linea
        self.columna = columna

    def interpretar(self, tabla_simbolos, entorno = "Global"):
        #VERIFICAR SI EXISTE ESE STRUCT

        valor_interpretado = tabla_simbolos.get(self.id)
        if(valor_interpretado):
            if valor_interpretado.tipo == Tipo.Struct : 
                info_struct = tabla_simbolos.get_struct(valor_interpretado.valor["__tipo_struct"])
                if info_struct is not None:
                    #VARIFICAR SI ES MUTABLE
                    if info_struct[0] == True:
                        # ES MUTABLE
                        #VERIFICAR QUE TENGA ESA PROPIEDAD
                        if self.prop in valor_interpretado.valor.keys():
                            expres = self.expresion.interpretar(tabla_simbolos)
                            valor_interpretado.valor[self.prop] = expres
                            # ACTUALIZAR EN TABLA DE SIMBOLOS
                            tabla_simbolos.update(simbolo(self.id, valor_interpretado.valor, Tipo.Struct, entorno, self.linea,self.columna))
                        else:
                            # PROP NO EXISTE
                            tipo_struct = tabla_simbolos.get_variable_struct(self.id)
                            error("struct %s no tiene el campo '%s'"%(self.id, tipo_struct), "asignacion struct", self.linea)

                    else:
                        # NO ES MUTABLE
                        error("struct %s no es mutable "%(self.id), "asignacion struct", self.linea)
                else:
                    print("NO ES TIPO STRUCT")
            else:
                error("variable %s no es de tipo struct"%(self.id), "acceso struct", self.linea)    
            #return valorExpresion(valor_interpretado.valor, valor_interpretado.tipo)
        else:
            error("variable %s no definida"%(self.id), "acceso struct", self.linea)

class definicion_funcion(instruccion):

    def __init__(self, id, parametros, instrucciones, linea, columna):
        self.id = id
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.linea = linea
        self.columna = columna

    def  interpretar(self, tabla_simbolos, wr:write):
        tabla_simbolos.addFunc(self.id)
        tabla_simbolos  = ts(tabla_simbolos)
        returnlbl = f"L{wr.getLabel()}"
        tabla_simbolos.returnlbl = returnlbl

        wr.addFunc(self.id, 1)
        for param in self.parametros:
            tabla_simbolos.add(param[0], param[1],  (param[1] == "String" or param[1] == "Struct"))

        for inst in self.instrucciones:
            inst.interpretar(tabla_simbolos,wr)

        wr.place_label(returnlbl)
        wr.endFunc()

class instruccion_llamada_funcion(instruccion):
    def __init__(self, id, parametros, linea, columna):
        self.id = id
        self.parametros = parametros
        self.linea = linea
        self.columna = columna

    def interpretar(self, tabla_simbolos:ts, wr:write):

        parametros = []
        if tabla_simbolos.getFunc(self.id) is not None:
            size = tabla_simbolos.pos
            for param in self.parametros:
                parametros.append(param.interpretar(tabla_simbolos,wr))
            temp = f"T{wr.getPointer()}"

            wr.place_operation(temp, "P", size + 1, "+")
            aux  = 0
            for param in parametros:
                aux += 1
                wr.insert_stack(temp, param.value)
                if aux != len(parametros):
                    wr.place_operation(temp, temp, 1, "+")
            wr.new_env(size)
            wr.call_function(self.id)
            wr.get_stack(temp, "P")
            wr.return_evn(size)

            return valorExpresion(temp, Tipo.Float64, True)

class instruccion_return(instruccion):

    def __init__(self, expresion, linea, columna):
        self.expresion = expresion
        self.linea = linea
        self.columna = columna
    
    def interpretar(self,tabla_simbolos, wr:write):
        if tabla_simbolos.returnlbl == "":
            print("ERROR RETURN FUERA DE FUNCION")

        valor = self.expresion.interpretar(tabla_simbolos,wr)
        if valor.type == Tipo.Bool:
            temp = f"L{wr.getLabel()}"
            wr.place_label(temp)
            wr.place_label(valor.truelbl)
            wr.insert_stack('P', '1')
            wr.place_goto(temp)

            wr.place_label(valor.falselbl)
            wr.insert_stack('P', '0')

            wr.place_label(temp)
        else:
            wr.insert_stack('P', valor.value)
        wr.place_goto(tabla_simbolos.returnlbl)


class instruccion_push(instruccion):
    def __init__(self, array, expresion, linea, columna):
        self.array = array
        self.expresion = expresion
        self.linea = linea
        self.columna = columna

    def interpretar(self, tabla_simbolos, entorno = "Global"):
        # ARRAY O ID
        if type(self.array) is str: 
            # ID GET VALOR
            existance = tabla_simbolos.get(self.array)
            if existance is not None:
                if existance.tipo == Tipo.Array:
                    # AGREGAR VALOR Y RETORNAR
                    expresion = self.expresion.interpretar(tabla_simbolos)
                    existance.valor.append(expresion)
                    # Actualizar valor
                    tabla_simbolos.update(existance)
                    return valorExpresion(existance.valor, Tipo.Array)
                else:
                    error("no es posible aplicar la funcion push a un valor de tipo '%s'"%(existance.tipo.value),"instruccion push", self.linea)
            else:
                error("variable '%s' no definida"%(self.array),"instruccion push", self.linea)
        else:
            # INTERPRETAR EXPRESION ARRAY Y RETORNAR
            array = self.array.interpretar(tabla_simbolos)
            expresion = self.expresion.interpretar(tabla_simbolos)
            array.append(expresion)
            return valorExpresion(array, Tipo.Array)
        
class instruccion_pop(instruccion):
    def __init__(self, array, linea, columna):
        self.array = array
        self.linea = linea
        self.columna = columna

    def interpretar(self, tabla_simbolos, entorno = "Global"):
        # ARRAY O ID
        if type(self.array) is str: 
            # ID GET VALOR
            existance = tabla_simbolos.get(self.array)
            if existance is not None:
                if existance.tipo == Tipo.Array:
                    # AGREGAR VALOR Y RETORNAR
                    if(len(existance.valor)) > 0:
                        valor = existance.valor.pop()
                        # Actualizar valor
                        tabla_simbolos.update(existance)
                        return valorExpresion(valor, Tipo.Array)
                    else:
                        return valorExpresion([], Tipo.Array)
                    
                else:
                    error("no es posible aplicar la funcion pop a un valor de tipo '%s'"%(existance.tipo.value),"instruccion pop", self.linea)
            else:
                error("variable '%s' no definida"%(self.arra),"instruccion push", self.linea)
        else:
            # INTERPRETAR EXPRESION ARRAY Y RETORNAR
            array = self.array.interpretar(tabla_simbolos)
            if(len(array)) > 0:
                valor = array.pop()
                return valorExpresion(valor, Tipo.Array)
            else:
                return valorExpresion([], Tipo.Array)

class instruccion_construir_struct(instruccion):
    def __init__(self, id_struct, parametros, linea, columna):
        self.id_struct = id_struct
        self.parametros = parametros
        self.linea = linea
        self.columna = columna

    def interpretar(self, tabla_simbolos, entorno = "Global"):

        info_struct = tabla_simbolos.get_struct(self.id_struct)

        if(info_struct is None):
            error("tipo de struct no definido '%s'"%(self.struct), "construccion struct", self.linea)
        if len(self.parametros) != len(info_struct[2]):
            error("numero de parametros incorrecto '%s'"%(self.id), "construccion struct", self.linea)

        #INTERPRETAR LOS VALORES PARA CREARLO
        valores = []
        for val in self.parametros:
            try:
                valor = val.interpretar(tabla_simbolos)
                valores.append(valor)
            except Exception as e:
                valores.append(val)
        
        count = 0

        valores_struct = {}
        while count < len(valores):
            if (isinstance(valores[count], list)):
                if(info_struct[2][count][1] == None or info_struct[2][count][1] == Tipo.Array.value):
                    valores_struct[info_struct[2][count][0]] = valores[count]
                else:
                    error("tipo de parametro invalido para construccion de struct '%s', parametro '%s' se esperaba un valor de tipo'%s'"%(self.id_struct,info_struct[2][count][0], info_struct[2][count][1]), "construcion struct", self.linea)
                count += 1

            elif(info_struct[2][count][1] == None or info_struct[2][count][1] == valores[count].type.value):
                valores_struct[info_struct[2][count][0]] = valores[count]
            else:
                error("tipo de parametro invalido para construccion de struct '%s', parametro '%s' se esperaba un valor de tipo'%s'"%(self.id_struct,info_struct[2][count][0], info_struct[2][count][1]), "construcion struct", self.linea)
            count += 1

        valores_struct["__tipo_struct"] = self.id_struct
        return valores_struct

        # s = tabla_simbolos.get(self.id)
        # if(s == None):
        #     tabla_simbolos.add(simbolo(self.id, valores_struct, Tipo.Struct, entorno, self.linea,self.columna))
        #     tabla_simbolos.add_variabe_struct(self.id, self.struct)
        # else:
        #     tabla_simbolos.update(simbolo(self.id, valores_struct, Tipo.Struct, entorno, self.linea,self.columna))
        #     tabla_simbolos.add_variabe_struct(self.id, self.struct) 
        # try:
        #     print("asignacion struct",s.valor["actor"].value["nombre"].value)     
        # except Exception:
        #     pass

class instruccion_global(instruccion):
    def __init__(self):
        pass
    def interpretar(self, tabla_simbolos, entorno = "Global"):
        pass