class write():

    def __init__(self):
        self.contador = 0
        self.label = 0
        self.code = ''
        self.funciones = ''
        self.nativas = ''
        self.in_native = False
        self.in_function = False
        self.texto_print = self.get_printString()
        self.nativasAgregadas = []
        self.use_mod = False
        
    def get_header(self):
        if self.use_mod:
            header = "package main; \nimport ( \"fmt\"; \"math\");\n"
        else:
            header = "package main; \nimport ( \"fmt\");\n"
        header += "var heap [100000]float64; \nvar stack [100000]float64;\n"
        header += "var P, H float64;\n"
        contador = self.contador
        temps = "var " 
        for i in range(contador+1):
            if i == contador:
                temps += f"T{i} float64;\n\n"
            else:
                temps += f"T{i},"
        header += temps
        return header

    def get_printString(self):
        texto_print = "func printString(){\n" 
        texto_print += f"T{self.getPointer()} = 0;\nT{self.getPointer()} = stack[int(T{self.getLastPointer()-1})];\n"
        texto_print += f"L{self.getLabel()}:\n"
        texto_print += f"T{self.getPointer()} = heap[int(T{self.getLastPointer()-1})];\n"
        texto_print += f"if T{self.getLastPointer()} == -1 "
        texto_print += "{ goto " + f"L{self.getLabel()};" + "}\n"
        texto_print += f'fmt.Printf("%c", int(T{self.getLastPointer()}));\n'
        texto_print += f"T{self.getLastPointer()-1} = T{self.getLastPointer()-1} + 1; \n"
        texto_print += f"goto L{self.getLastLabel()-1};\nL{self.getLastLabel()}: \nreturn;\n" + "}\n"
        return texto_print

    def get_code(self):
        return f'{self.get_header()}{self.texto_print}{self.nativas}\n{self.funciones}\nfunc main(){{\n{self.code}}}'

    def comment(self, comment):
        self.insert_code(f'/* {comment} */\n')
        
    # TEMPORALES
    def getPointer(self):
        temp = self.contador
        self.contador += 1
        return temp

    def getLastPointer(self):
        return self.contador-1

    # ETIQUETAS
    def getLabel(self):
        label = self.label
        self.label += 1
        return label

    def getLastLabel(self):
        return self.label-1

    def insert_code(self, codigo, tab='\t'):
        # escribir en nativas
        if self.in_native:
            if self.nativas == '':
                # comentario
                self.nativas += '/* funciones nativas */\n'
            self.nativas = self.nativas + tab + codigo
        # escribir en funciones
        elif self.in_function:
            if self.funciones == '':
                self.funciones += '/* funciones */\n'
            self.funciones += tab + codigo 
        else:
            self.code += '\t' + codigo

    '''INSERT CODE'''

    # operacion
    def place_operation(self, resultado, izq, der = "", operador = ""):
        self.insert_code(f'{resultado}={izq}{operador}{der}; \n')
    # etiqueta
    def place_label(self, etiqueta):
        self.insert_code(f'{etiqueta}:\n')
    # goto
    def place_goto(self, etiqueta):
        self.insert_code(f'goto {etiqueta};\n')
    # if
    def place_if(self, izq, der, operador, etiqueta):
        self.insert_code(f'if {izq}{operador}{der} {{goto {etiqueta};}}\n')
    # insert stack
    def insert_stack(self, posicion, valor):
        self.insert_code(f'stack[int({posicion})]={valor};\n')
    # get stack
    def get_stack(self, variable, posicion):
        self.insert_code(f'{variable}=stack[int({posicion})];\n')
    # insert heap
    def insert_heap(self, posicion, valor):
        self.insert_code(f'heap[int({posicion})]={valor};\n')
    # get heap
    def get_heap(self, variable, posicion):
        self.insert_code(f'{variable}=heap[int({posicion})];\n')
    # next heap
    def next_heap(self):
        self.insert_code('H = H + 1;\n')
    # print
    def place_print(self, tipo, valor):
        if tipo != 'f':
            self.insert_code(f'fmt.Printf("%{tipo}", int({valor}));\n')
        else:
            self.insert_code(f'fmt.Printf("%{tipo}", {valor});\n')

    def new_env(self, tamano):
        self.insert_code(f'P=P+{tamano};\n')

    def place_mod_op(self, pos, izq, der):
        self.use_mod = True
        self.insert_code(f"{pos} = math.Mod({izq},{der});\n")

    def addFunc(self, id, tipoFunc):
        if tipoFunc == 1:
            self.in_function = True
        else:
            self.in_native = True
        self.insert_code(f'func {id}(){{\n', '')

    def endFunc(self):
        
        self.insert_code('return;\n}\n');
        self.in_function = False
        self.in_native = False
        if(not self.in_native):
            self.in_function = False

    def call_function(self, id):
        self.insert_code(f'{id}();\n')

    def return_evn(self, tamano):
        self.insert_code(f'P=P-{tamano};\n')
    
    # prints varios
    def print_true(self):
        self.place_print('c', 116)#t
        self.place_print('c', 114)#r
        self.place_print('c', 117)#u
        self.place_print('c', 101)#e
    def print_false(self):
        self.place_print('c', 102)#f
        self.place_print('c', 97) #a
        self.place_print('c', 108)#l
        self.place_print('c', 115)#s
        self.place_print('c', 101)#e
    def nothing(self):
        self.place_print('c', 110) #n
        self.place_print('c', 111) #o
        self.place_print('c', 116) #t
        self.place_print('c', 104) #h
        self.place_print('c', 105) #i
        self.place_print('c', 110) #n
        self.place_print('c', 103) #g

    def print(self):
        f = open('./salida.go', 'w')
        f.write(self.get_code())
        f.close()

    def addPotencia(self):
        if "potenNativeFunc" in self.nativasAgregadas:
            return
        i = 0
        e = []
        l = []
        while i < 17:
            e.append(f"T{self.getPointer()}")
            i += 1
        j = 0
        while j < 4:
            l.append(f"L{self.getLabel()}")
            j += 1
        self.nativasAgregadas.append("potenNativeFunc")
        self.nativas += "func potenNativeFunc(){" + f"""
    {e[1]}=P+1; 
    {e[0]}=stack[int({e[1]})];
    {e[2]}=P+3; 
    stack[int({e[2]})]={e[0]};
    {l[1]}:
    {e[4]}=P+2; 
    {e[3]}=stack[int({e[4]})];
    if {e[3]}>1.0 """ + "{goto " + f"""{l[2]}""" + "}" + f""";
    goto """ + f"""{l[3]};
    {l[2]}:
    {e[6]}=P+3; 
    {e[5]}=stack[int({e[6]})];
    {e[8]}=P+1; 
    {e[7]}=stack[int({e[8]})];
    {e[9]}={e[5]}*{e[7]}; 
    {e[10]}=P+3; 
    stack[int({e[10]})]={e[9]};
    {e[12]}=P+2; 
    {e[11]}=stack[int({e[12]})];
    {e[13]}={e[11]}-1.0; 
    {e[14]}=P+2; 
    stack[int({e[14]})]={e[13]};
    goto """ + f"""{l[1]};
    {l[3]}:
    {e[16]}=P+3; 
    {e[15]}=stack[int({e[16]})];
    stack[int(P)]={e[15]};
    goto """ + f"""{l[0]};
    {l[0]}:
    return;
""" + "}\n"

    def addConcat(self):
        if "concatNative" in self.nativasAgregadas:
            return
        self.nativasAgregadas.append("concatNative")
        self.in_native = True
        function = False
        if self.in_function:
            function = True
        self.addFunc("concatNative", 0)
        t3 = f"T{self.getPointer()}" # resultado
        self.place_operation(t3, "H")

        self.comment("PARAMETRO 1")
        t1 = f"T{self.getPointer()}"    # pos 1
        self.place_operation(t1, "P", 1, "+")
        t1s = f"T{self.getPointer()}"    
        self.get_stack(t1s, t1)
        
        l1 = f"L{self.getLabel()}"
        lf1 = f"L{self.getLabel()}"

        tempPos = f"T{self.getPointer()}"
        tempCad = f"T{self.getPointer()}"
        self.place_operation(tempPos, t1s)

        self.place_label(l1) # LABEL 1
        self.get_heap(tempCad, tempPos)
        self.place_if(tempCad, "-1", "==", lf1)
        self.insert_heap("H", tempCad)
        self.place_operation(tempPos, tempPos, "1", "+")
        self.next_heap()
        self.place_goto(l1)
        
        self.place_label(lf1) # LABEL 2
        l2 = f"L{self.getLabel()}"
        lf2 = f"L{self.getLabel()}"

        self.comment("PARAMETRO 2")
        t2 = f"T{self.getPointer()}"    # pos 2
        self.place_operation(t2, "P", 2, "+")
        t2s = f"T{self.getPointer()}"    
        self.get_stack(t2s, t2)
        
        tempPos = f"T{self.getPointer()}"
        tempCad = f"T{self.getPointer()}"
        self.place_operation(tempPos, t2s)

        self.place_label(l2) # LABEL 2
        self.get_heap(tempCad, tempPos)
        self.place_if(tempCad, "-1", "==", lf2)
        self.insert_heap("H", tempCad)
        self.place_operation(tempPos, tempPos, "1", "+")
        self.next_heap()
        self.place_goto(l2)

        self.place_label(lf2) # SALIDA
        self.insert_heap("H", -1)
        self.next_heap()
        self.insert_stack("P", t3)
        self.endFunc()
        self.in_native = False
        if function:
            self.in_function = True

    def addRepeat(self):
        if "repeatNative" in self.nativasAgregadas:
            return
        self.nativasAgregadas.append("repeatNative")
        self.in_native = True
        function = False
        if self.in_function:
            function = True
        self.addFunc("repeatNative", 0)

        t3 = f"T{self.getPointer()}" # resultado
        self.place_operation(t3, "H")

        self.comment("PARAMETRO 1")
        t1 = f"T{self.getPointer()}"    # pos 1
        self.place_operation(t1, "P", 1, "+")
        t1s = f"T{self.getPointer()}"    
        self.get_stack(t1s, t1)

        self.comment("PARAMETRO 2")
        t2 = f"T{self.getPointer()}"    # pos 2
        self.place_operation(t2, "P", 2, "+")
        t2s = f"T{self.getPointer()}"    
        self.get_stack(t2s, t2)
        
        
        l1 = f"L{self.getLabel()}"
        lf1 = f"L{self.getLabel()}"

        tempPos = f"T{self.getPointer()}"
        tempCad = f"T{self.getPointer()}"
        tempCount = f"T{self.getPointer()}"
        self.place_operation(tempPos, t1s)
        self.place_operation(tempCount, t2s)

        self.place_label(l1) # LABEL 1
        self.get_heap(tempCad, tempPos)
        self.place_if(tempCad, "-1", "==", lf1)
        self.insert_heap("H", tempCad)
        self.place_operation(tempPos, tempPos, "1", "+")
        self.next_heap()
        self.place_goto(l1)
        
        lf2 = f"L{self.getLabel()}"
        self.place_label(lf1) # LABEL 2
        self.place_operation(tempCount, tempCount, "1", "-")
        self.place_operation(tempPos, t1s)
        self.place_if(tempCount, "1", "<", lf2)
        self.place_goto(l1)

        self.place_label(lf2) # SALIDA
        self.insert_heap("H", -1)
        self.next_heap()
        self.insert_stack("P", t3)
        self.endFunc()
        self.in_native = False
        if function:
            self.in_function = True

    def addLower(self):
        if "lowerNative" in self.nativasAgregadas:
            return
        self.nativasAgregadas.append("lowerNative")
        self.in_native = True
        function = False
        if self.in_function:
            function = True
        self.addFunc("lowerNative", 0)

        t3 = f"T{self.getPointer()}" # resultado
        self.place_operation(t3, "H")

        self.comment("PARAMETRO 1")
        t1 = f"T{self.getPointer()}"    # pos 1
        self.place_operation(t1, "P", 1, "+")
        t1s = f"T{self.getPointer()}"    
        self.get_stack(t1s, t1)

        l1 = f"L{self.getLabel()}"
        l2 = f"L{self.getLabel()}"
        l3 = f"L{self.getLabel()}"
        lf = f"L{self.getLabel()}"
        lf1 = f"L{self.getLabel()}"

        tempPos = f"T{self.getPointer()}"
        tempCad = f"T{self.getPointer()}"
        self.place_operation(tempPos, t1s)

        self.place_label(l1) # LABEL 1
        self.get_heap(tempCad, tempPos)
        self.place_if(tempCad, "-1", "==", lf1)
        self.place_if(tempCad, 65, ">=", l2)
        self.place_goto(lf)
        self.place_label(l2)
        self.place_if(tempCad, 90, "<=", l3)
        self.place_goto(lf)

        self.place_label(l3)
        temp = f"T{self.getPointer()}"
        self.place_operation(temp, tempCad, 32, "+")
        self.insert_heap("H", temp)
        self.place_operation(tempPos, tempPos, "1", "+")
        self.next_heap()
        self.place_goto(l1)

        self.place_label(lf)
        self.insert_heap("H", tempCad)
        self.place_operation(tempPos, tempPos, "1", "+")
        self.next_heap()
        self.place_goto(l1)

        self.place_label(lf1) # SALIDA
        self.insert_heap("H", -1)
        self.next_heap()
        self.insert_stack("P", t3)
        self.endFunc()
        self.in_native = False
        if function:
            self.in_function = True

    def addUpper(self):
        if "upperNative" in self.nativasAgregadas:
            return
        self.nativasAgregadas.append("upperNative")
        self.in_native = True
        function = False
        if self.in_function:
            function = True
        self.addFunc("upperNative", 0)

        t3 = f"T{self.getPointer()}" # resultado
        self.place_operation(t3, "H")

        self.comment("PARAMETRO 1")
        t1 = f"T{self.getPointer()}"    # pos 1
        self.place_operation(t1, "P", 1, "+")
        t1s = f"T{self.getPointer()}"    
        self.get_stack(t1s, t1)

        l1 = f"L{self.getLabel()}"
        l2 = f"L{self.getLabel()}"
        l3 = f"L{self.getLabel()}"
        lf = f"L{self.getLabel()}"
        lf1 = f"L{self.getLabel()}"

        tempPos = f"T{self.getPointer()}"
        tempCad = f"T{self.getPointer()}"
        self.place_operation(tempPos, t1s)

        self.place_label(l1) # LABEL 1
        self.get_heap(tempCad, tempPos)
        self.place_if(tempCad, "-1", "==", lf1)
        self.place_if(tempCad, 97, ">=", l2)
        self.place_goto(lf)
        self.place_label(l2)
        self.place_if(tempCad, 122, "<=", l3)
        self.place_goto(lf)

        self.place_label(l3)
        temp = f"T{self.getPointer()}"
        self.place_operation(temp, tempCad, 32, "-")
        self.insert_heap("H", temp)
        self.place_operation(tempPos, tempPos, "1", "+")
        self.next_heap()
        self.place_goto(l1)

        self.place_label(lf)
        self.insert_heap("H", tempCad)
        self.place_operation(tempPos, tempPos, "1", "+")
        self.next_heap()
        self.place_goto(l1)

        self.place_label(lf1) # SALIDA
        self.insert_heap("H", -1)
        self.next_heap()
        self.insert_stack("P", t3)
        self.endFunc()
        self.in_native = False
        if function:
            self.in_function = True

    def addPrintArray(self):
        if "printArrNative" in self.nativasAgregadas:
            return
        self.nativasAgregadas.append("printArrNative")
        self.in_native = True
        function = False
        if self.in_function:
            function = True
        self.addFunc("printArrNative", 0)

        self.comment("PARAMETRO 1")
        t1 = f"T{self.getPointer()}"    # pos 1
        self.place_operation(t1, "P", 1, "+")
        t1s = f"T{self.getPointer()}"    
        self.get_stack(t1s, t1)
        self.place_operation(t1s, t1s, 1, "+") # TAMANO

        self.comment("PARAMETRO 2")
        t2s = f"T{self.getPointer()}"
        tipo = f"T{self.getPointer()}"
        self.place_operation(t2s, t1s, 1, "+") # TIPO
        self.get_heap(tipo, t2s)

        self.comment("PRINT")
        tamano = f"T{self.getPointer()}"
        self.get_heap(tamano, t1s)

        
        l1 = f"L{self.getLabel()}"
        l2 = f"L{self.getLabel()}"
        l3 = f"L{self.getLabel()}"
        lfinal = f"L{self.getLabel()}"
        lf1 = f"L{self.getLabel()}"

        self.insert_code("fmt.Printf(\"%c\", int(91));\n")

        pos = f"T{self.getPointer()}"
        self.place_operation(pos, t2s, 1, "+")
        temp = f"T{self.getPointer()}"

        self.place_label(l1) # LABEL 1
        self.place_if(tamano, "0", "<=", lf1)
        self.get_heap(temp, pos)
        temp1 = f"T{self.getPointer()}"
        self.get_heap(temp1, temp)
        self.place_if(temp1, "-2", "==", l2)
        self.place_goto(l3)
        
        self.place_label(l2) # LABEL 2
        tempN = f"T{self.getPointer()}"
        self.place_operation(tempN, "P", 2, "+")
        self.insert_stack(tempN, tamano)
        self.place_operation(tempN, "P", 3, "+")
        self.insert_stack(tempN, pos)
        self.place_operation(tempN, "P", 4, "+")
        self.insert_stack(tempN, temp)
        self.new_env(3)
        self.call_function("printArrNative")
        self.insert_code(f"fmt.Printf(\",\");\n") # COMA
        self.return_evn(3)
        self.place_goto(lfinal)

        self.place_label(l3) # LABEL 3
        lprint1 = f"L{self.getLabel()}"
        lprint2 = f"L{self.getLabel()}"
        lprint3 = f"L{self.getLabel()}"
        lprintSalida = f"L{self.getLabel()}"
        self.place_if(tipo, "0", "==", lprint1) # STRING
        self.place_if(tipo, "1", "==", lprint2) # INT
        self.place_if(tipo, "2", "==", lprint3) # FLOAT
        self.place_label(lprint1)
        self.insert_code(f"fmt.Printf(\"%f,\", ({temp1}));\n") # FALTA
        self.place_goto(lprintSalida)
        self.place_label(lprint2)
        self.insert_code(f"fmt.Printf(\"%d,\", int({temp1}));\n")
        self.place_goto(lprintSalida)
        self.place_label(lprint3)
        self.insert_code(f"fmt.Printf(\"%f,\", ({temp1}));\n")
        self.place_label(lprintSalida)

        self.place_label(lfinal)
        self.place_operation(tamano, tamano, 1, "-")
        self.place_operation(pos, pos, 1, "+")
        self.place_goto(l1)

        self.place_label(lf1)
        self.insert_code("fmt.Printf(\"%c\", int(8));\n")
        self.insert_code("fmt.Printf(\"%c\", int(93));\n")

        self.comment("PARAMETRO 3")
        t1 = f"T{self.getPointer()}"    # pos 1
        self.place_operation(t1, "P", 1, "-")
        t1s = f"T{self.getPointer()}"    
        self.get_stack(t1s, t1)
        self.place_operation(tamano, t1s) # TAMANO

        self.comment("PARAMETRO 4")
        t1 = f"T{self.getPointer()}"    # pos 1
        self.place_operation(t1, "P", 0, "-")
        t1s = f"T{self.getPointer()}"    
        self.get_stack(t1s, t1)
        self.place_operation(pos, t1s) # POS

        self.endFunc()
        self.in_native = False
        if function:
            self.in_function = True

    def addCompareString(self):
            if "compareStringNative" in self.nativasAgregadas:
                return
            self.nativasAgregadas.append("compareString")
            self.in_native = True
            function = False
            if self.in_function:
                function = True
            self.addFunc("compareString", 0)

            t3 = f"T{self.getPointer()}" # resultado
            self.place_operation(t3, "H")

            self.comment("PARAMETRO 1")
            t1 = f"T{self.getPointer()}"    # pos 1
            self.place_operation(t1, "P", 1, "+")
            t1s = f"T{self.getPointer()}"    
            self.get_stack(t1s, t1)
            
            self.comment("PARAMETRO 2")
            t2 = f"T{self.getPointer()}"    # pos 2
            self.place_operation(t2, "P", 2, "+")
            t2s = f"T{self.getPointer()}"    
            self.get_stack(t2s, t2)

            l1 = f"L{self.getLabel()}"
            lf1 = f"L{self.getLabel()}"
            lf2 = f"L{self.getLabel()}"
            fin = f"L{self.getLabel()}"


            tempPos = f"T{self.getPointer()}"
            tempCad = f"T{self.getPointer()}"
            tempCad1 = f"T{self.getPointer()}"

            self.place_operation(tempPos, t1s)
            
            self.place_label(l1) # LABEL 1
            self.get_heap(tempCad, tempPos)
            self.get_heap(tempCad1, tempPos)
            self.place_if(tempCad, tempCad1, "!=", lf1)
            self.place_if(tempCad, "-1", "==", lf2)
            self.place_operation(tempPos, tempPos, "1", "+")
            self.place_goto(l1)
            
            self.place_label(lf1) # LABEL 2
            self.insert_stack("P", 0)
            self.place_goto(fin)

            self.place_label(lf2) # SALIDA
            self.insert_stack("P", 1)

            self.place_label(fin)
            self.endFunc()
            self.in_native = False
            if function:
                self.in_function = True

    def addTrunc(self):
        if "truncNative" in self.nativasAgregadas:
            return
        self.nativasAgregadas.append("truncNative")
        self.in_native = True
        function = False
        if self.in_function:
            function = True
        self.addFunc("truncNative", 0)

        t3 = f"T{self.getPointer()}" # resultado
        self.place_operation(t3, "H")

        self.comment("PARAMETRO 1")
        t1 = f"T{self.getPointer()}"    # pos 1
        self.place_operation(t1, "P", 1, "+")
        t1s = f"T{self.getPointer()}"    
        self.get_stack(t1s, t1)
        

        temp = f"T{self.getPointer()}"
        self.place_mod_op(temp, t1s, 1)

        self.place_operation(t3, t1s)
        self.place_operation(t3, t3, temp, "-")

        self.insert_stack("P", t3)
        self.endFunc()
        self.in_native = False
        if function:
            self.in_function = True



