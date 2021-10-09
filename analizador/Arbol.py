

class Nodo:
    def __init__(self, nombre, hijos = []):
        self.id = None
        self.nombre = nombre
        self.hijos = hijos

    def imprimir(self):
        print(self.nombre)
        for i in self.hijos:
            print(self.nombre, "->", i.nombre)
            i.imprimir()

    def imprimirInfoNodo(self, texto, contador):
        self.id = "nodo"+ str(contador)
        texto += self.id + f"[label=\"{self.nombre}\"];"
        contador += 1
        for i in self.hijos:
            texto, contador = i.imprimirInfoNodo(texto, contador)
        return [texto, contador]

    def imprimirEnlace(self, texto, padre):
        if padre is not None:
            texto+= f"{padre}->{self.id};"
            for i in self.hijos:
                texto = i.imprimirEnlace(texto, self.id)
        else:
            for i in self.hijos:
                texto = i.imprimirEnlace(texto, self.id)

        return texto

    def insertar(self, nodo):
        self.hijos.append(nodo)

class Arbol:
    def __init__(self, raiz, filepath):
        self.raiz = raiz
        self.filepath = filepath
    
    def imprimir(self):
        texto, contador = self.raiz.imprimirInfoNodo("",0)
        texto_enlace = self.raiz.imprimirEnlace("", None)
        f = open(self.filepath, "w")
        f.write("digraph{")
        f.write(texto)
        f.write(texto_enlace)
        f.write("}")

