from re import S
from analizador.expresiones.expresiones import expresion_binaria, valorExpresion, expresion
import sys
sys.path.append('../')
from analizador.tabla_simbolos import simbolo, Tipo, tabla_simbolos as  ts
from analizador.write import write
from abc import ABC, abstractmethod
from analizador.error import ContinueError, ReturnError, error, BreakError

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
        if existance is not None:
            if existance.isGlobal == False:
                pos = f"T{wr.getPointer()}"
                wr.place_operation(pos, "P", existance.apuntador, "+")
                wr.insert_stack(pos,expresion.value)
            else:
                wr.insert_stack(existance.apuntador,expresion.value)
            tabla_simbolos.update(self.id, expresion.type)
        else:
            tabla_simbolos.add(self.id, expresion.type, (expresion.type == Tipo.String or expresion.type == Tipo.Struct))
            expresion1 = tabla_simbolos.get(self.id)
            pos = tabla_simbolos.getPos() - 1
            temp = f"L{wr.getLabel()}"
            if tabla_simbolos.entorno is not None and expresion.type != Tipo.Bool:
                pos = f"T{wr.getPointer()}"
                wr.place_operation(pos, "P", expresion1.apuntador, "+")

            if expresion.type == Tipo.Bool:
                wr.place_label(expresion.truelbl)
                if tabla_simbolos.entorno is not None:
                    pos = f"T{wr.getPointer()}"
                    wr.place_operation(pos, "P", expresion1.apuntador, "+")
                wr.insert_stack(pos,1)
                wr.place_goto(temp)
                wr.place_label(expresion.falselbl)
                if tabla_simbolos.entorno is not None:
                    pos = f"T{wr.getPointer()}"
                    wr.place_operation(pos, "P", expresion1.apuntador, "+")
                wr.insert_stack(pos,0)
                wr.place_label(temp)
            else:
                wr.insert_stack(pos,expresion.value)

class asignacion_array(instruccion):
    def __init__(self, id: str, expresiones, tipo, linea: int, columna: int):
        self.id = id
        self.expresion = expresiones
        self.tipo = tipo
        self.line = linea
        self.col = columna

    def interpretar(self, tabla_simbolos, wr:write):
        # ASIGNAR EXPRESION
        expresion = self.expresion.interpretar(tabla_simbolos,wr)
        existance:simbolo = tabla_simbolos.get(self.id)

        if existance is not None:
            if tabla_simbolos.entorno is not None:
                pos = f"T{wr.getPointer()}"
                wr.place_operation(pos, "P", existance.apuntador, "+")
                wr.insert_stack(pos,expresion.value)
            else:
                wr.insert_stack(existance.apuntador,expresion.value)
        else:
            dim = 1
            if self.tipo is not None:
                cadena = self.tipo.split("{")
                if len(cadena) > 2:
                    dim = len(cadena) - 1
            tabla_simbolos.add(self.id, Tipo.Array, (expresion.type == Tipo.String or expresion.type == Tipo.Struct), "", dim)
            expresion1 = tabla_simbolos.get(self.id)
            pos = tabla_simbolos.getPos() - 1
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
                
class asignacion_array_posicion(instruccion):
    def __init__(self, id: str, posiciones, expresion, linea: int, columna: int):
        self.id = id
        self.posiciones = posiciones
        self.expresion = expresion
        self.line = linea
        self.col = columna

    def interpretar(self, tabla_simbolos,wr:write):
        
        expresion = self.expresion.interpretar(tabla_simbolos,wr)
        existance:simbolo = tabla_simbolos.get(self.id)

        if existance is not None:
            wr.comment("ACCESO ARRAY")
            posiciones = []
            for pos in self.posiciones:
                valor = pos.interpretar(tabla_simbolos,wr)
                posiciones.append(valor)
            
            apuntador = existance.apuntador
            posicion = f"T{wr.getPointer()}"
            wr.get_stack(posicion, apuntador)
            valor = f"T{wr.getPointer()}"
            wr.place_operation(valor, 0)
            
            t0 = f"T{wr.getPointer()}" # POSICION A ACCEDER
            
            t1 = f"T{wr.getPointer()}" # VALOR ACCEDIDO
            tamano = f"T{wr.getPointer()}"

            lblerr1 = f"L{wr.getLabel()}"
            lblerr2 = f"L{wr.getLabel()}"
            lblerrfinal = f"L{wr.getLabel()}"
            lblfinal = f"L{wr.getLabel()}"
            
            for pos in posiciones:
                wr.comment(f"ACCESO POS {pos.value} ")
                wr.place_operation(t0, posicion)
                
                temp = f"T{wr.getPointer()}"
                wr.place_operation(temp,pos.value)

                wr.get_heap(t1, t0)
                wr.place_if(t1, "-2", "!=", lblerr1)
                wr.place_operation(t0,t0,"1","+")
                wr.get_heap(t1, t0)
                wr.place_operation(tamano,t1)
                wr.place_operation(t0,t0,"1","+")

                wr.place_if(temp, tamano, ">", lblerr2)
                wr.place_operation(t0, t0, temp, "+")
                wr.get_heap(t1, t0)
                wr.get_heap(valor, t1)

                lblcontinue = f"L{wr.getLabel()}"
                wr.place_if(valor, "-2", "==", lblcontinue)
                wr.place_goto(lblfinal)
                
                wr.place_label(lblcontinue)
                wr.place_operation(posicion, t1) # CAMBIO DE ARRAY 
                wr.place_goto(lblfinal)
                

            wr.place_label(lblerr1)
            wr.insert_code("fmt.Printf(\"No es un array\");\n")
            wr.insert_code("fmt.Printf(\"%c\", int(10));\n")
            wr.place_goto(lblerrfinal)

            wr.place_label(lblerr2)
            wr.insert_code("fmt.Printf(\"Posicion fuera de los limites del array\");\n")
            wr.insert_code("fmt.Printf(\"%c\", int(10));\n")
            wr.place_goto(lblerrfinal)

            wr.place_label(lblfinal)
            wr.insert_heap(t1, expresion.value)
            wr.place_label(lblerrfinal)
        else:
            print("ERROR ARRAY NO ENCONTRADO")

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


        tabla_simbolos = ts(tabla_simbolos)
        tabla_simbolos.cicloInicio = inicio
        tabla_simbolos.pos = 1
        valor = self.expresion.interpretar(tabla_simbolos,wr)
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
    def __init__(self, id, expresion, instrucciones, linea, columna):
        self.id = id
        self.expresion = expresion
        self.instrucciones = instrucciones
        self.line = linea
        self.col = columna

    def interpretar(self, tabla_simbolos, wr:write):
        expresion = self.expresion[0].interpretar(tabla_simbolos,wr)
        rangeD = self.expresion[1].interpretar(tabla_simbolos,wr)

        # ASIGNAR EXPRESION
        tabla_simbolos = ts(tabla_simbolos)
        existance:simbolo = tabla_simbolos.get(self.id)
        pos = ""
        if existance is not None:
            if tabla_simbolos.entorno is not None:
                pos = f"T{wr.getPointer()}"
                wr.place_operation(pos, "P", existance.apuntador, "+")
                wr.insert_stack(pos,expresion.value)
            else:
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

        wr.comment("INSTRUCCION FOR")
        inicio = f"L{wr.getLabel()}"
        temp = f"T{wr.getPointer()}"
        wr.place_operation(temp, expresion.value, "", "")
        wr.place_label(inicio)

        truelbl1 = f"L{wr.getLabel()}"
        falselbl1 = f"L{wr.getLabel()}"
        
        wr.place_if(temp, rangeD.value, "<=", truelbl1)
        wr.place_goto(falselbl1)

        
        tabla_simbolos.cicloInicio = inicio

        tabla_simbolos.cicloFinal = falselbl1

        wr.place_label(truelbl1)
        for inst in self.instrucciones:
                inst.interpretar(tabla_simbolos,wr)

        wr.place_operation(temp, temp, 1, "+")
        
        existance:simbolo = tabla_simbolos.get(self.id)
        if tabla_simbolos.entorno is not None:
            apos = f"T{wr.getPointer()}"
            wr.place_operation(apos, "P", existance.apuntador, "+")
            wr.insert_stack(apos,temp)
        else:
            wr.insert_stack(pos,temp)


        wr.place_goto(inicio)
        wr.place_label(falselbl1)
        tabla_simbolos.cicloInicio = ""
        tabla_simbolos.cicloFinal = ""

class instruccion_print(instruccion):
    def __init__(self, expresiones, tipo):
        self.expresiones = expresiones
        self.tipo = tipo

    def interpretar(self, tabla_simbolos, wr:write):
        for expresion in self.expresiones:
            v:valorExpresion = expresion.interpretar(tabla_simbolos,wr)
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
            elif v.type == Tipo.Array:
                temp = f"T{wr.getPointer()}"
                wr.place_operation(temp, "P", tabla_simbolos.pos + 1, "+")
                wr.insert_stack(temp, v.value)
                wr.new_env(tabla_simbolos.pos)
                wr.call_function("printArrNative")
                wr.get_stack(temp, "P")
                wr.return_evn(tabla_simbolos.pos)
                wr.addPrintArray()


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
        returnlbl = f"L{wr.getLabel()}"
        tabla_simbolos_copy = ts(tabla_simbolos)
        tabla_simbolos_copy.pos = 1
        tabla_simbolos_copy.returnlbl = returnlbl
        tabla_simbolos_copy.entorno = True
        wr.addFunc(self.id, 1)
        for param in self.parametros:
            tipo = Tipo.Int64
            if param[1] == "Int64":
                tipo = Tipo.Int64
            elif param[1] == "Float64":
                tipo = Tipo.Float64
            elif param[1] == "String":
                tipo = Tipo.String
            elif param[1] == "Char":
                tipo = Tipo.Char
            elif param[1] == "Bool":
                tipo = Tipo.Bool
            elif param[1] == "Struct":
                tipo = Tipo.Struct
            else:
                if param[1] is not None:
                    if param[1].split("{")[0] == "Vector":
                        tipo = Tipo.Array
            
            tabla_simbolos_copy.add(param[0], tipo,  (param[1] == "String" or param[1] == "Struct"))

        for inst in self.instrucciones:
            inst.interpretar(tabla_simbolos_copy,wr)

        wr.place_goto(returnlbl)
        wr.place_label(returnlbl)
        wr.endFunc()
        tabla_simbolos_copy.entorno = False

class instruccion_llamada_funcion(instruccion):
    def __init__(self, id, parametros, linea, columna):
        self.id = id
        self.parametros = parametros
        self.linea = linea
        self.columna = columna

    def interpretar(self, tabla_simbolos:ts, wr:write):

        tabla_simbolos.entorno = True
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
            tabla_simbolos.entorno = False
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