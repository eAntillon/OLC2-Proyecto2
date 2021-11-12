import gramatica as g
from tabla_simbolos import tabla_simbolos
from write import write
import traceback

def interpretar(texto):
    f = open('./analizador/salida.go', 'r+')
    f.truncate(0) # need '0' when using r+
    f.close()
    # f = open('./analizador/entrada.jl', 'r')
    # entrada  = f.read()
    # f.close()
    entrada = texto
    try:
        wr = write()
        ts = tabla_simbolos()
        instrucciones = g.parse(entrada)
        for inst in instrucciones:
            inst.interpretar(ts,wr)
        wr.print()
        f = open('./salida.go', 'r')
        res = f.read()
        f.close()
        return [res, [], []]
    except Exception as e:
        print(traceback.format_exc())
        output = str(e)
        print("ERROR DE EJECUCION", e)
        return [output, [], []]
