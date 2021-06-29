from flask import Flask, render_template, request, flash, redirect, url_for, session, g
import os
from conexion import Conexion
from werkzeug.security import generate_password_hash as genph  # Para encriptar la contraseña
from werkzeug.security import check_password_hash as checkph # para desencriptar la contraseña


app=Flask(__name__)
app.secret_key='mysecretkey'


@ app.route('/', methods=['GET', 'POST']) #Ruta para el index
def index():
    if request.method=='POST':
        session.pop('user', None) # Destruir sesiones abiertas antes de iniciar una nueva

        usuario= request.form['Username'] # Capturar el nombre de usuario del formulario
        conexion=Conexion.conectar() # Crear conexion a la base de datos
        # Enviar consulta para pedir la contraseña del usuario ingresado
        passwd=Conexion.leer_datos(conexion, f"select Password from Usuarios where Usuario = '{usuario}'") 
        if len(passwd)<1: # Si la longitud de la respuesta es <1 entonces no encontró el usuario en la DB
            print('El usuario no existe') 

        else: #Comprobar la ontraseña ingresada con la guardada en la base de datos
            password = str(passwd[0]['Password']) # Convertir la contraseña de la consulta a string
            contrasena=str(request.form['Password']) # Convertir la contraseña del formulario a string
            verificacion=checkph(password, contrasena) # Desencriptar y verificar igualdad de contraseñas devuelve (True o False)
            

            if verificacion==True: # En caso que sean iguales...
                session['user']= request.form['Username'] # Crea una sesion con el nombre de usuario ingresado
                return redirect(url_for('menu')) # REdirige a la pagina de menu

    return render_template('index.html')# En caso de que no sean iguales redirige nuevamente al index

@ app.route('/menu') # Ruta de la pagina menu
def menu():
    if g.user: # Verifica si hay una sesion con un usuario
        return render_template('menu.html', user=session['user'])# Renderiza la pagina y envia el nombre del usuario
    return redirect(url_for('index')) # Si no hay sesion redirige a index para que el usuario  haga login

@ app.before_request # Crear la variable global con el nombre del usuario
def before_request():
    g.user=None # Se inicializa la variable global

    if 'user' in session: # Verificar si hay algun usuario con sesion activa
        g.user=session['user'] # Asignar el nombre del usuario a la variable global


##====================CERRAR SESION =============================
@ app.route('/salir', methods=['POST']) # Ruta para hacer logout
def salir():

    if request.method=='POST': # Lee el formulario post del boton salir de las paginas
        session.pop('user', None) # Destruir la sesión         
        return redirect(url_for('index')) # Una vez destruida la sesión, Redireccionar al index
             
## ================== CREAR USUARIO EN LA APLICACION==================
@ app.route('/crear')
def crearuser():
    if g.user: # Verificar si hay alguna sesion abierta, de lo contrario no puede crear usuario
        return render_template('crearusuario.html', user=session['user'])# Redirige a la pagina crear usuario
    
    return redirect(url_for('index')) # Si no hay ususario redirige a index para abrir sesión


@ app.route('/add_user', methods=['POST']) # Funcion para crear usuario
def adduser():
    if request.method=='POST': # Verifica peticion del formulario
        usuario=request.form['Usuario'] # Capturar usuario
        password = request.form['Password'] # Capturar contraseña
        password=genph(password) # Encripta la contraseña

        conexion=Conexion.conectar() # Crear conexion con la base de datos
        # Guardar los datos de usuario y la contraseña encriptada en la base de datos
        Conexion.escribir_datos(conexion, f"insert into Usuarios values(null, '{usuario}', '{password}')")
        
    return redirect(url_for('index'))# una vez guardado redirige al index
    




if __name__=='__main__':
    app.run(port=3000, debug=True)