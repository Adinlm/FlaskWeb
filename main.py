from flask import Flask, flash, redirect, url_for, render_template, request
from datetime import datetime
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'clave_secreta_flask'

# Conexión DB

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'proyectoflask'

mysql = MySQL(app)


# Context Processors

@app.context_processor
def date_now():
    return {
        'now': datetime.utcnow()
    }

# Endpoints


@app.route('/')
def index():

    edad = 101
    personas = ['Cooper', 'Vader', 'Sony', 'Kin']

    return render_template('index.html', edad=edad, dato1="Valor", dato2="Valor2", lista=["uno", "dos", "tres"], personas=personas)


@app.route('/informacion/')
@app.route('/informacion/<string:nombre>')
@app.route('/informacion/<string:nombre>/<apellidos>')
def informacion(nombre=None, apellidos=None):

    texto = ""
    if nombre is not None and apellidos is not None:
        texto = f"Bienvenido, {nombre} {apellidos}"

    return render_template('informacion.html', texto=texto)


@app.route('/contacto')
@app.route('/contacto/<redireccion>')
def contacto(redireccion=None):

    if redireccion is not None:
        return redirect(url_for('lenguajes'))

    return render_template('contacto.html')


@app.route('/lenguajes-de-programacion')
def lenguajes():
    return render_template('lenguajes.html')

@app.route('/crear-auto', methods=['GET','POST'])
def crear_auto():
    if request.method == 'POST':

        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']
        ciudad = request.form['ciudad']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO autos VALUES(NULL, %s, %s, %s, %s)", (marca, modelo, precio, ciudad))
        cursor.connection.commit()
        flash('Has creado el auto correctamente')

        return redirect(url_for('index'))

    return render_template('crear_auto.html')


@app.route('/autos')
def autos():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM autos ORDER BY id DESC")
    autos = cursor.fetchall()
    cursor.close()

    return render_template('autos.html', autos=autos)

@app.route('/auto/<auto_id>')
def auto(auto_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM autos WHERE id = %s", (auto_id))
    auto = cursor.fetchall()
    cursor.close()

    return render_template('auto.html', auto=auto[0])

@app.route('/borrar-auto/<auto_id>')
def borrar_auto(auto_id):
    cursor = mysql.connection.cursor()
    cursor.execute(f"DELETE FROM autos WHERE id = {auto_id}")
    mysql.connection.commit()

    flash('El auto ha sido eliminado!!')

    return redirect(url_for('autos'))

    return render_template('auto.html', auto=auto[0])

@app.route('/editar-auto/<auto_id>', methods=['GET', 'POST'])
def editar_auto(auto_id):
    if request.method == 'POST':

        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']
        ciudad = request.form['ciudad']

        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE autos
            SET marca = %s,
                modelo = %s,
                precio = %s,
                ciudad = %s
            WHERE id=%s
        """, (marca, modelo, precio, ciudad, auto_id))
        cursor.connection.commit()
        flash('Has editado el auto correctamente')

        return redirect(url_for('autos'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM autos WHERE id = %s", (auto_id))
    auto = cursor.fetchall()
    cursor.close()

    return render_template('crear_auto.html', auto=auto[0])

if __name__ == '__main__':
    app.run(debug=True)
