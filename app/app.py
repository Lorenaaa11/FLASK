from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import bcrypt


# Crear instancia
app = Flask(__name__)

# Configurar la conexión
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="agenda2024"
)

cursor = db.cursor()

def encriptarcontra(contraencrip):

    encriptar = bcrypt.hashpw(contraencrip.encode('utf-8'), bcrypt.gensalt())

    return encriptar
@app.route('/login' , methods=['GET','POST'])
def login():
    if request.methos == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')

        cursor = db.cursor()


        cursor.execute('SELECT usup,passp FROM personas WHERE usup = %s', (usuario,))                   
        usuario = cursor.fetchone()

        if usuario and bcrypt.checkpw_password_hash(usuario[7],password):
            session['usuario'] = usuario
            return redirect(url_for('lista')) 
        else:
            error = 'Credenciales ivalidas, por favor intente de nuevo'
            return redirect(url_for('login',error=error))

@app.route('/')  # Crear ruta
def lista():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM personas')
    usuario = cursor.fetchall()
    return render_template('index.html',usuario=usuario)

@app.route('/Registrar', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == 'POST':
       Nombres = request.form.get('nombre')
       Apellidos = request.form.get('apellido')
       email = request.form.get('email')
       Direccion = request.form.get('direccion')
       Telefono = request.form.get('telefono')
       Usuario = request.form.get('usuario')
       Password = request.form.get('password')

       contrasenaencriptada = encriptarcontra(Password)

        # Insertar datos a la tabla de mysql
       cursor.execute("INSERT INTO personas(nombrep,apellidop,emailp,dirp,telp,usup,passp) VALUES (%s,%s,%s,%s,%s,%s,%s)",(Nombres,Apellidos,email,Direccion,Telefono,Usuario,contrasenaencriptada))
       db.commit()

            
       return redirect(url_for('registrar_usuario'))  # Redirigir a la página principal
    return render_template("Registrar.html")

@app.route('/editar/<int:id>',methods=['GET', 'POST'])
def editar_usuario(id):
    cursor = db.cursor()
    if request.method == 'POST':
        nombrep = request.form.get('nombrep')
        apellidop = request.form.get('apellidop')
        emailp = request.form.get('emailp')
        dirp = request.form.get('dirp')
        telp = request.form.get('telp')
        usup = request.form.get('usup')
        passp = request.form.get('passp')

        sql = "UPDATE personas set nombrep=%s,apellidop=%s,emailp=%s,dirp=%s,telp=%s,usup=%s,passp=%s where polper=%s"
        cursor.execute(sql,(nombrep,apellidop,emailp,dirp,telp,usup,passp,id))
        db.commit()
        
        return redirect(url_for('lista'))
    
    else: 
        cursor = db.cursor()
        cursor.execute('SELECT * FROM personas WHERE polper=%s' ,(id,))
        data = cursor.fetchall()

        return render_template('editar.html', personas=data[0])

@app.route("/eliminar/<int:id>", methods=['GET'])
def eliminar_usuario(id):

    cursor = db.cursor()
    cursor.execute('DELETE FROM personas WHERE polper = %s', (id,))
    db.commit()
    return redirect(url_for('lista'))

# Ejecutar app
if __name__ == '__main__':
    app.add_url_rule('/',view_func=lista)
    app.run(debug=True, port=5005)  # Debug para que salgan los errores en consola
