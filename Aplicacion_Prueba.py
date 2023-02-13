#Importación de librerias
from flask import Flask, render_template, request
import pandas as pd
import json
import os
import firebase_admin
from firebase_admin import credentials, db

#Inicializa proyecto en flask
AppWeb = Flask(__name__, template_folder="Plantillas", static_folder="Archivos")
BASE_PATH= os.getcwd()
UPLOAD_PATH= os.path.join(BASE_PATH, "Subidas")

#Conexión a base de datos en firebase
cred = credentials.Certificate("pruebatecnicait-firebase-adminsdk-mhm5y-6a0c8ab35a.json")
firebase_admin.initialize_app(cred, {'databaseURL':'https://pruebatecnicait-default-rtdb.firebaseio.com/'})

@AppWeb.route("/", methods=["GET", "POST"])
def inicio():
    ref = db.reference("Datos")
    datos = ref.get() 
    print(datos)
    if request.method == "POST":
        archivo_csv = request.files["csv_file"]
        nombre_archivo = archivo_csv.filename
        extensionFile = nombre_archivo.split(".")[-1]
        if extensionFile.lower() in ["csv"]:
            path_save= os.path.join(UPLOAD_PATH, nombre_archivo)
            archivo_csv.save(path_save)
            df = pd.read_csv(path_save)
            nombre_columnas = df.columns
            print(nombre_columnas)
            for item in nombre_columnas:
                datosColumna = df[item].tolist()
                json_data = json.dumps(datosColumna)
                ref.child(nombre_archivo.split(".")[0]).child(item).set(datosColumna)
        else:
            mensaje = "Extensión incorrecta, solo se permiten archivos csv"
            return render_template("index.html", mensaje = mensaje)        
    return render_template("index.html", array=datos)

@AppWeb.route("/mi-ruta/", methods=["POST"])
def funcionVer():
    global datosRecuperados
    ref = db.reference("Datos")
    selectedOption = request.get_json()["selectedOption"]
    print(selectedOption)
    datosRecuperados = ref.child(selectedOption).get()
    if datosRecuperados == None:
        print(datosRecuperados)
        return render_template("index.html", mensaje = "Sin datos")
    else:
        return render_template("index.html")

@AppWeb.route("/mi-ruta2/", methods=["GET"])
def funcionVer2():
    print("Entro aqui", datosRecuperados)
    datos2 = datosRecuperados
    return render_template("index2.html", datos2=datos2)

if __name__ == "__main__":
    AppWeb.run(debug=True)
