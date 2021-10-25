import gramatica as g
from tabla_simbolos import tabla_simbolos
from write import write, pointer
import traceback

def interpretar():
    f = open('./salida.go', 'r+')
    f.truncate(0) # need '0' when using r+
    f.close()
    f = open('./entrada.jl', 'r')
    entrada  = f.read()
    f.close()
    try:
        wr = write()
        ts = tabla_simbolos()
        instrucciones = g.parse(entrada)
        for inst in instrucciones:
            inst.interpretar(ts,wr)
        wr.print()
        ts.print()
    except Exception as e:
        print(traceback.format_exc())
        output = str(e)
        print("ERROR DE EJECUCION", e)
        return [output, [], []]

interpretar()