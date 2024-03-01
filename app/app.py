from flask import Flask,render_template,request,redirect,url_for
import mysql.connector

app = Flask (__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Agenda2024"
)
curso = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Registrar', methods=['GET','POST'])
def registrar_usuario():
    if request.method == 'POST':
        Nombre = request.form.get('nombre')
        Apellido = request.form.get('apellido')
        Email = request.form.get('email')
        Direccion = request.form.get('direccion')
        Telefono = request.form.get('telefono')
        Usuario = request.form.get('usuario')
        Contraseña = request.form.get('Contrasena')


        curso.execute("INSERT INTO personas(Nombreper,Apellidoper,Emailper,direccionper,Telefono,Usuarioper,Contraseñaper)VALUES(%s,%s,%s,%s,%s,%s,%s)",(Nombre,Apellido,Email,Direccion,Telefono,Usuario,Contraseña))
        db.commit()


        return redirect(url_for('registrar_usuario'))
    return render_template('Registrar.html')


if __name__ == '__main__':
    app.add_url_rule('/',view_func=index)
    app.run(debug=True,port=5005)

  