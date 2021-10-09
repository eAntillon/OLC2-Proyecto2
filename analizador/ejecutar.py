import gramatica as g
from tabla_simbolos import tabla_simbolos
import traceback
from Arbol import Arbol
import requests
import shutil

def interpretar(input):
    f = open('./analizador/salida.txt', 'r+')
    f.truncate(0) # need '0' when using r+
    f.close()
    try:
        instrucciones = g.parse(input)
        g.parser.restart()
    except Exception as e:
        print(traceback.format_exc())
        output = str(e)
        print("ERROR DE EJECUCION", e)
        f = open("./analizador/salida.txt", "a")
        strs = "ups! " + str(e)
        f.write(strs)
        f.close()
        return [output, [], []]


    ts_global = tabla_simbolos()
    ts_global.clean()

    # LISTA DE ERRORES
    errores = []
    for instruccion in instrucciones[0]:
        try:
            instruccion.interpretar(ts_global)
        except Exception as e:
            e.valor["no"] = len(errores)+1
            errores.append(e.valor)            

    ts_global.print()
    lista_print = ts_global.get_table()
    ts_global.clean()
    f = open("./analizador/salida.txt", "r")
    output = f.read()
    f.close()

    # GENERAR ARBOL
    arbol = Arbol(instrucciones[1], "./analizador/graph.txt")
    arbol.imprimir()
    # LEER TEXTO DOR
    f = open("./analizador/graph.txt", "r")
    graph = f.read()
    f.close()
    # HTTP POST
    URL = "https://quickchart.io/graphviz"
    data = {'graph':graph, "layout": "dot","format": "svg"}
    r = requests.post(url = URL, json = data, timeout=1110)
    # with open('./static/img/arbol-graph.png', 'wb') as f:
    #     f.write(r.content)
    # del r
    img = open("./analizador/arbol.svg", "w")
    img.write(r.text)
    img.close()
    return [output, lista_print, errores]