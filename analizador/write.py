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
        
    def get_header(self):
        header = "package main; \nimport ( \"fmt\" );\n"
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
        texto_print += f"T{self.getPointer()} = P+0;\nT{self.getPointer()} = stack[int(T{self.getLastPointer()-1})];\n"
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
            if self.natives == '':
                # comentario
                self.natives += '/* funciones nativas */\n'
            self.natives = self.natives + tab + codigo
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

    def addFunc(self, id, tipoFunc):
        if(not self.in_native):
            self.in_function = True
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