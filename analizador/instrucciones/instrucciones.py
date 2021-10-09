from re import S
from analizador.expresiones.expresiones import valorExpresion, expresion
import sys
sys.path.append('../')
from analizador.tabla_simbolos import simbolo, Tipo
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

    def interpretar(self, tabla_simbolos, entorno = "Global"):

        existance = tabla_simbolos.get(self.id)
        #ASIGNAR STRUCT
       
        # ASIGNAR EXPRESION
        expresion = self.expresion.interpretar(tabla_simbolos)
        if isinstance(expresion, dict):
            s = tabla_simbolos.get(self.id)
            if(s == None):
                tabla_simbolos.add(simbolo(self.id, expresion, Tipo.Struct, entorno, self.linea,self.columna))
                tabla_simbolos.add_variabe_struct(self.id, expresion["__tipo_struct"])
            else:
                tabla_simbolos.update(simbolo(self.id, expresion, Tipo.Struct, entorno, self.linea,self.columna))
                tabla_simbolos.add_variabe_struct(self.id, expresion["__tipo_struct"])    
        else:  
            s = simbolo(self.id, expresion.value, expresion.type, entorno, self.linea, self.columna)
            if existance is None:
                # Agregar nuevo simbolo
                tabla_simbolos.add(s)
            else:
                # Actualizar valor
                tabla_simbolos.update(s)

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

    def interpretar(self, tabla_simbolos, entorno = "Global"):
        valor_expresion = self.expresion.interpretar(tabla_simbolos)
        if(valor_expresion.type != Tipo.Bool):
            error("se esperaba una expresion de tipo 'Boolean', se obtuvo '%s'"%(valor_expresion.type), "instruccion if", self.line)
        if(valor_expresion.value == True):
            for instruccion in self.instrucciones:
                try:
                    instruccion.interpretar(tabla_simbolos, "IF")
                except BreakError:
                    raise BreakError("break")
                except ContinueError:
                    raise ContinueError("continue")
                except ReturnError as r:
                    raise ReturnError(r.expresion)
        else:
            if(self.instruccion_elseif is not None):
                self.instruccion_elseif.interpretar(tabla_simbolos, "ELIF")
            elif(len(self.instrucciones_else) > 0):
                for inst in self.instrucciones_else:
                    inst.interpretar(tabla_simbolos, "ELSE")

class instruccion_while(instruccion):
    def __init__(self, expresion, instrucciones, linea, columna):
        self.expresion = expresion
        self.instrucciones = instrucciones
        self.linea = linea
        self.columna = columna 

    def interpretar(self, tabla_simbolos, entorno = "Global"):
        RECURSION_MAXIMA = 3000
        COUNT = 0
        valor = self.expresion.interpretar(tabla_simbolos)
        if(valor.type != Tipo.Bool):
            error("se esperaba una expresion de tipo 'Boolean', se obtuvo '%s'"%(valor.type), "instruccion while", self.linea)
        
        flag_continue = False
        while valor.value == True:
            if flag_continue:
                flag_continue = False
                continue
            try:
                for inst in self.instrucciones:
                    try:
                        inst.interpretar(tabla_simbolos)
                    except ContinueError:
                        flag_continue = True
                        break
                    except BreakError:
                        raise BreakError("Break")
                        break
                
                valor = self.expresion.interpretar(tabla_simbolos)
                COUNT += 1
                if(COUNT == RECURSION_MAXIMA):
                    error("recursion maxima alcanzada", "while", self.linea)
                    break;
            except BreakError:
                break

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

    def interpretar(self, tabla_simbolos, entorno = "Global"):
        valores = []
        for expresion in self.expresiones:
            v = expresion.interpretar(tabla_simbolos)
            if(isinstance(v, list)):
                valores.append(self.valorToString(v))
            else:
                valores.append(v.toString())
        string = " ".join(valores)
        if self.tipo == "println":
            string += "\n"
        #     #print(string)
        # else:
        #     #print(string, end='')
        try:
            f = open("./analizador/salida.txt", "a")
            f.write(string)
            f.close()
        except Exception:
            pass
    def valorToString(self, valor):
        if(isinstance(valor, list)):
            cadena = "["
            valores = []
            for v in valor:
                valores.append(str(self.valorToString(v)))
            return cadena + ",".join(valores) + "]"
        else:
            return valor.value

class instruccion_break(instruccion):
    def __init__(self, linea, columna): 
        self.linea = linea
        self.columna = columna 
    
    def interpretar(self, tabla_simbolos, entorno = "Global"):
        raise BreakError("Break")  

class instruccion_continue(instruccion):

    def __init__(self, linea, columna): 
        self.linea = linea
        self.columna = columna 
    
    def interpretar(self, tabla_simbolos, entorno = "Global"):
        raise ContinueError("Continue")  

class definicion_struct(instruccion):

    def __init__(self,tipo, id, parametros, linea, columna): 
        self.tipo = tipo
        self.id = id
        self.parametros = parametros
        self.linea = linea
        self.columna = columna 
    
    def interpretar(self, tabla_simbolos, entorno = "Global"):
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

    def  interpretar(self, tabla_simbolos, entorno = "Global"):
        if(tabla_simbolos.get(self.id) == None and tabla_simbolos.get_func(self.id) == None):
            tabla_simbolos.add_func(self.id, self.parametros, self.instrucciones)
            parametros_print = []
            for param in self.parametros:
                if(param[1] is None):
                    parametros_print.append(param[0])
                else:
                    parametros_print.append(param[0] + "::" + param[1])
            tabla_simbolos.add_funcion_print(self.id, parametros_print, entorno, self.linea, self.columna)
        else:
            error("no es posible redefinir la constante '%s'"%(self.id), 'function', self.linea)

class instruccion_llamada_funcion(instruccion):
    def __init__(self, id, parametros, linea, columna):
        self.id = id
        self.parametros = parametros
        self.linea = linea
        self.columna = columna

    def interpretar(self, tabla_simbolos, entorno = "Global"):
        
        import copy
        #ASIGNAER VALORES A TABLA DE SIMBOLOS

        #CREAR NUEVA TABLA DE SIMBOLOS
        tabla_simbolos_funcion = copy.deepcopy(tabla_simbolos)

        #TOMAR INFOR PARAMETROS
        info_func = tabla_simbolos.get_func(self.id)
        # NO EXISTE ESA FUNCION
        if info_func is None:
            error("no existe la funcion '%s'"%(self.id), 'llamada funcion', self.linea)
        nombres_parametros = info_func[1]
        
        #PARAMETROS AGREGADOS
        count = 0
        for param in self.parametros:
            
            nombre_parametro = nombres_parametros[count][0]
            tipo_parametro = nombres_parametros[count][1]
            valor_parametro = param.interpretar(tabla_simbolos)
            if isinstance(valor_parametro,list) and (tipo_parametro == "Array" or tipo_parametro == 'None'):
                pass
            else:
                if(tipo_parametro == valor_parametro.type.value) or tipo_parametro == None:
                    pass
                else:
                    error("tipo de parametro '%s' incorrecto "%(nombre_parametro), "llamada funcion", self.linea)

            existance = tabla_simbolos.get(nombre_parametro)
            if isinstance(valor_parametro,list):
                s = simbolo(nombre_parametro, valor_parametro, Tipo.Array, self.id, self.linea, self.columna)
                if existance is None:
                    # Agregar nuevo simbolo
                    tabla_simbolos_funcion.add(s)
                else:
                    # Actualizar valor
                    tabla_simbolos_funcion.update(s)  
            else:

                s = simbolo(nombre_parametro, valor_parametro.value, valor_parametro.type, self.id, self.linea, self.columna)
                if existance is None:
                    # Agregar nuevo simbolo
                    tabla_simbolos_funcion.add(s)
                else:
                    # Actualizar valor
                    tabla_simbolos_funcion.update(s)
            count += 1

        # EJECUTAR INSTRUCCIONES
        for inst in info_func[2]:
            try:
                inst.interpretar(tabla_simbolos_funcion)
            except BreakError:
                error("instruccion 'break' fuera de un bucle", 'llamada funcion', self.linea)
            except ContinueError:
                error("instruccion 'continie' fuera de un bucle", 'llamada funcion', self.linea)
            except ReturnError as r:
                return r.expresion
        # print("TABLA FUNCION")
        # tabla_simbolos_funcion.print()
        # print("FIN TABLA FUNCION")

class instruccion_return(instruccion):

    def __init__(self, expresion, linea, columna):
        self.expresion = expresion
        self.linea = linea
        self.columna = columna
    
    def interpretar(self, tabla_simbolos, entorno = "Global"):
        #tabla_simbolos.print()
        if isinstance(self.expresion, dict):
            valor = self.expresion
            parametros_interpretados = []
            for param in valor["parametros"]:
                try:
                    a = param.value
                    parametros_interpretados.append(param)
                except Exception:
                    parametros_interpretados.append(param.interpretar(tabla_simbolos))
            valor["parametros"] = parametros_interpretados
            raise ReturnError(valor)
        else:
            valor = self.expresion.interpretar(tabla_simbolos)
            if isinstance(valor, list):
                s = valorExpresion(valor, Tipo.Array)
                raise ReturnError(s)
            else:
                #if isinstance(valor, expresion) or isinstance(valor, valorExpresion):
                raise ReturnError(valor)
                #else:
                # error("se esperaba un valor de expresion para retornar", "return", self.linea)

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