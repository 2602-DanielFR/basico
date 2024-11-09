from flask import Flask, render_template, request,redirect
import pymysql

app = Flask(__name__)

@app.route("/")
def hola_mundo():
    mensaje = "Hola mundo 2"
    return mensaje


@app.route("/usuario/registrar")
def usuario_registrar():
    return render_template("registroUsuario.html")

@app.route("/usuario/guardar", methods=["POST"])
def usuario_guardar():
    username = request.form["username "]
    password = request.form["password"]
    nombres = request.form["nombres"]
    apellidos = request.form["apellidos"]
    tipo = request.form["tipo"]

    conn = conexion()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO usuario(username, password, nombres, apellidos, tipo, id_escuela, email) VALUES(%s, %s, %s, %s, %s %s,%s)", (username, password, nombres, apellidos, tipo, 1, "generico@gmail.com"))
    conn.commit()
    conn.close()
    return redirect("/usuario/mostrar")

@app.route("/usuario/mostrar")
def usuario_mostrar():
    conn = conexion()
    usuarios = []
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM usuario")
        usuarios = cursor.fetchall()
    conn.close()
    return render_template("mostrarUsuario.html", usuarios=usuarios)

@app.route("/usuario/modificar/<int:id>")
def usuario_modificar(id):
    conn = conexion()
    usuarios = []
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM usuario WHERE id = %s", (id))
        usuarios = cursor.fetchall()
    conn.close()
    return render_template("actualizarUsuario.html", usuarios=usuarios)

@app.route("/usuario/actualizar", methods=["POST"])
def usuario_actualizar():
    username = request.form["username"]
    nombres = request.form["nombres"]
    apellidos = request.form["apellidos"]
    tipo = request.form["tipo"]
    id = request.form["id"]

    conn = conexion()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE usuario SET username = %s, password = %s, nombres = %s, apellidos = %s, tipo = %s WHERE id = %s", (username, nombres, apellidos, tipo, id))
    conn.commit()
    conn.close()
    return "usuario actualizado"

@app.route("/usuario/eliminar/<int:id>")
def usuario_eliminar(id):
    conn = conexion()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM usuario WHERE id = %s", (id))
    conn.commit()
    conn.close()
    return "Usuario Eliminado"

def conexion():
    return pymysql.connect(host="localhost", 
                           user="root", 
                           password="", 
                           database="udh")