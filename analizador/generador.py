from .table import Tabla

class Generador(object):
    generador = None
    def __init__(self) -> None:
        self.temp_counter = 0
        self.label_counter = 0
        self.code = ''
        self.functions = ''
        self.natives = ''
        self.in_function = False
        self.in_native = False
        self.temps = []
        self.native_true = []


    def limpiar(self):
        self.temp_counter = 0
        self.label_counter = 0
        self.code = ''
        self.functions = ''
        self.natives = ''
        self.in_function = False
        self.in_native = False
        self.temps = []
        self.native_true = []
        Generador.generador = Generador()

    
    '''
    CODIGO
    '''
    def generate_header(self) -> str:
        c = 'package main;\n\nimport (\n\t"fmt"\n)\n\n'
        if len(self.temps) > 0:
            c += 'var '
            for temp in range(len(self.temps)):
                c += self.temps[temp]
                if temp != (len(self.temps) - 1):
                    c += ", "
            c += " float64\n"
        c += "var P, H float64;\nvar stack [30101999]float64;\nvar heap [30101999]float64;\n\n"
        return c


    def get_code(self):
        return f'{self.generar_encabezado()}{self.natives}\n{self.functions}\nfunc main(){{\n\tP = 1;\n{self.code}\n}}'


    def insert_code(self, codigo, tab='\t'):
        if self.in_native:
            if self.natives == '':
                self.natives += '/*----native functions----*/\n'
            self.natives = self.natives + tab + codigo
        elif self.functions:
            if self.functions == '':
                self.functions += '/*----functions----*/\n'
            self.functions += tab + codigo 
        else:
            self.code += '\t' + codigo


    def comment(self, comment):
        self.insert_code(f'/* {comment} */\n')


    def get_instance(self):
        if Generador.generador == None:
            Generador.generador = Generador()
        return Generador.generador


    def jump(self):
        self.insert_code('\n')


    '''
    TEMPORALES
    '''
    def new_temporal(self) -> str:
        temporal = f't{self.temp_counter}'
        self.temp_counter += 1
        self.temps.append(temporal)
        return temporal


    '''
    ETIQUETAS
    '''
    def new_label(self) -> str:
        etiqueta = f'L{self.label_counter}'
        self.label_counter += 1
        return etiqueta


    def place_label(self, etiqueta):
        self.insert_code(f'{etiqueta}:\n')



    def place_goto(self, etiqueta):
        self.insert_code(f'goto {etiqueta};\n')



    def place_if(self, izq, der, operador, etiqueta):
        self.insert_code(f'if {izq}{operador}{der} {{goto {etiqueta};}}\n')


    '''
    OPERACION BINARIA
    '''
    def place_operation(self, resultado, izq, der, operador):
        self.insert_code(f'{resultado}={izq}{operador}{der}; \n')


    '''
    functions
    '''
    def new_function(self, id):
        if not self.in_native:
            self.in_function = True
        self.insert_code(f'func {id}(){{\n', '')


    def end_function(self):
        self.insert_code('return;\n}\n')
        if not self.in_native:
            self.in_function = False


    '''
    STACK
    '''
    def insert_stack(self, posicion, valor):
        self.insert_code(f'stack[int({posicion})]={valor};\n')


    def get_stack(self, variable, posicion):
        self.insert_code(f'{variable}=stack[int({posicion})];\n')


    '''
    HEAP
    '''
    def insert_heap(self, posicion, valor):
        self.insert_code(f'heap[int({posicion})]={valor};\n')


    def get_heap(self, variable, posicion):
        self.insert_code(f'{variable}=heap[int({posicion})];\n')


    def next_heap(self):
        self.insert_code('H = H + 1;\n')

    
    '''
    ENTORNO
    '''
    def new_env(self, tamano):
        self.insert_code(f'P=P+{tamano};\n')

    
    def call_function(self, id):
        self.insert_code(f'{id}();\n')


    def return_evn(self, tamano):
        self.insert_code(f'P=P-{tamano};\n')


    # Añadir print de go 
    def place_print(self, tipo, valor):
        if tipo != 'f':
            self.insert_code(f'fmt.Printf("%{tipo}", int({valor}));\n')
        else:
            self.insert_code(f'fmt.Printf("%{tipo}", {valor});\n')

    '''
        prints
    '''
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


    '''
    natives
    '''

    def print_mathError(self):
        if "math_error" in self.native_true:
            return
        self.native_true.append("math_error")
        self.in_native = True

        self.new_function('math_error')
        self.place_print('c', 77)   #M
        self.place_print('c', 97)   #a
        self.place_print('c', 116)  #t
        self.place_print('c', 104)  #h
        self.place_print('c', 32)   # 
        self.place_print('c', 69)   #E
        self.place_print('c', 114)  #r
        self.place_print('c', 114)  #r
        self.place_print('c', 111)  #o
        self.place_print('c', 114)  #r
        self.place_print('c', 10)   #Salto de linea
        self.end_function()
        self.in_native = False


  
