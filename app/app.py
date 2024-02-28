from flask import*  #flask,render_template
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

@app.route('/Registrar', methods=['POST'])
def registrar_usuario():
    Nombre = request.form['nombre'],
    Apellido = request.form['apellido'],
    Email = request.form['email'],
    Direccion = request.form['direccion'],
    Telefono = request.form['telefono'],
    Usuario = request.form['usuario'],
    Contraseña = request.form['contrasena']


    curso.execute("INSERT INTO personas(Nombreper,Apellidoper,Emailper,direccionper,Telefono,Usuarioper,Contraseñaper)VALUES(%s,%s,%s,%s,%s,%s,%s)",(Nombre,Apellido,Email,Direccion,Telefono,Usuario,Contraseña))
    db.commit()


    return redirect(url_for('Registrar'))

if __name__ == '__main__':
    app.add_url_rule('/',view_func=index)
    app.run(debug=True,port=5005)
     

  