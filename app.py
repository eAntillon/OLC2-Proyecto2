from flask import Flask, render_template, request, redirect, Markup
import sys
sys.path.append('./analizador')
from analizador.ejecutar import *
from flask import Markup

app = Flask(__name__)

text_input = ""
text_output = ""
tabla_simbolos = []
errores =[]

@app.route("/", methods=["GET", "POST"])
def index():
    img = open("./analizador/arbol.svg", "w")
    img.write("")
    img.close()
    return render_template("index.html", active_page="home")


@app.route("/editor", methods=["GET"])
def editor():
    return render_template("editor.html", data=[text_input, text_output, tabla_simbolos, errores], active_page="editor")

@app.route("/reportes", methods=["GET"])
def reportes():
    try:
        svg = open('./analizador/arbol.svg').read()
    except: 
        svg = "ERROR AQUI"
    return render_template("reportes.html",svg=Markup(svg), active_page="reportes")

@app.route("/submitCode", methods=["POST"])
def submitCode():
    global text_input, text_output, tabla_simbolos, errores
    text_input = request.form["code_editor"]
    if(text_input.strip() == ""):
        text_output = ""
    else:
        try:
            res = interpretar(text_input)
            text_output, tabla_simbolos, errores = res
        except Exception as e:
            print("excepcion", e)
    return redirect("/editor")


if __name__ == "__main__":
    app.run(debug= True)
