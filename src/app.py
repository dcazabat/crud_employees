from os import abort
import pymysql
from flask import Flask, flash, render_template, request, redirect, session, send_from_directory
# from cryptography.fernet import Fernet
from flaskext.mysql import MySQL
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "daniel"
# encrypted_key = Fernet(app.secret_key)
mysql = MySQL()

# MySQL configurations
# En remote host
# app.config['MYSQL_DATABASE_HOST'] = 'remotemysql.com'
# app.config['MYSQL_DATABASE_USER'] = 'rB3cUolUmD'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'vXlnbLUILD'
# app.config['MYSQL_DATABASE_DB'] = 'rB3cUolUmD'

# En localhost
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'empleados'

mysql.init_app(app)


# Diccionario de que Contiene parametros Globales de la App
data={
    'title':'App de Flask - Empleados',
    'message': '',
    'messagealternative':'',
    'errbd': False
}

def test_connection():
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select version();")
        cursor = cursor.fetchall()
        data['errbd'] = False
    except pymysql.err.OperationalError:
        data['errbd'] = True
    except Exception as e:
        print(e)


def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/')
@app.route('/home')
def index():
    test_connection()
    data['message'] = 'Bienvenidos al Sitio'
    if data['errbd']:
        data['messagealternative'] = 'Sin Conexión a la Base de Datos'
    else:
        data['messagealternative'] = 'Ingreso al sistema'
    return render_template('/index.html',data=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    _user = request.form['txtUser']
    # _pass = encrypted_key.encrypt(request.form['txtPassword'])
    _pass = request.form['txtPassword']
    print(_user, _pass)
    try:
        if request.method == 'POST':
            sql = f'SELECT * FROM tbl_user WHERE user_email="{_user}";'
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql)
            cursor = cursor.fetchall()
            if cursor[0]['user_password'] == _pass:
                session['username'] = cursor[0]['user_name']
                session['email'] = cursor[0]['user_email']
                session['admin'] = cursor[0]['user_isadmin'] == 1
        return redirect('/')
    except pymysql.err.OperationalError:
        data['errbd'] = True
        return redirect('/')
    except Exception as e:
        return e


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('email', None)
    session.pop('admin', None)
    return redirect('/')

# TODO Emplaados

@app.route('/employees')
def employees():
    cursor = None
    try:
        #sql = 'insert into empleados (nombre, correo, foto) values ("Daniela Leon", "mdel2002@hotmail.com", "fotodedaniela.png");'
        sql = 'SELECT * FROM empleados'
        conn = mysql.connect()
        # conn.commit() # se usa cuando se hace un insert, update o delete

        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        cursor = cursor.fetchall()
        cabecera = ['#', 'Foto', 'Nombre', 'Correo', 'Acciones']
        data['message'] = 'Lista de Empleados'

        return render_template('empleados/employees.html', cursor=cursor, cabecera=cabecera, data=data)
    except pymysql.err.OperationalError:
        data['errbd'] = True
        return render_template('empleados/employees.html', data=data)
    except Exception as e:
        return e

@app.route('/fotodeusuario/<path:nombreFoto>')
def uploads(nombreFoto):
    print('**************',send_from_directory(os.path.join('uploads'), nombreFoto))
    return send_from_directory(os.path.join('uploads'), nombreFoto)

@app.route('/newemployee')
def add_employee_view():
    data['message'] = 'Alta de Empleados'
    return render_template('empleados/add.html',data=data)

@app.route('/addemployee',  methods=['GET', 'POST'])
def add_employee():
    cursor = None
    try: 
        if session['username']:
            _name = request.form['inputName']
            _email = request.form['inputEmail']
            _foto = request.files['inputFoto']
            # validate the received values
            if _name and _email and _foto and request.method == 'POST':
                now = datetime.now()
                tiempo = now.strftime("%Y%H%M%S")
                if _foto.filename != '':
                    nuevoNombreFoto = tiempo + '_' + _foto.filename
                    _foto.save("src/static/assets/images/uploads/" + nuevoNombreFoto)

                sql = "INSERT INTO empleados (nombre, correo, foto) values (%s, %s, %s);"
                datos = (_name, _email, nuevoNombreFoto)                # save edits
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, datos)
                conn.commit()
            return redirect('/employees')
        else:
            return render_template('404.html'), 404
    except Exception as e:
        return e


@app.route('/editemployee/<int:id>',  methods=['GET', 'POST'])
def edit_employee(id):
    cursor = None
    data['message'] = 'Editar de Empleado'
    try:
        if session['username']:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            datos = [id]
            cursor.execute("SELECT * FROM empleados WHERE id=%s", datos)
            row = cursor.fetchone()
            return render_template('empleados/edit.html', row=row, data=data)
        else:
            return render_template('404.html'), 404
    except Exception as e:
        return e


@app.route('/updateemployee', methods=['GET', 'POST'])
def update_employee():
    cursor = None
    try:
        if session['username']:
            _name = request.form['inputName']
            _email = request.form['inputEmail']
            _foto = request.files['inputFoto']
            _id = request.form['inputId']
            # validate the received values
            if _name and _email and _id and request.method == 'POST':
                # save edits
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                if _foto.filename != '':
                    now = datetime.now()
                    tiempo = now.strftime("%Y%H%M%S")
                    nuevoNombreFoto = tiempo + '_' + _foto.filename
                    print(nuevoNombreFoto)
                    _foto.save("static/assets/images/uploads/" + nuevoNombreFoto)

                    sql = f'SELECT foto FROM empleados WHERE id={_id}'
                    cursor.execute(sql)
                    row = cursor.fetchone()
                    try:
                        os.remove(os.path.join(app.config['UPLOADS'], row['foto']))
                    except:
                        pass

                    sql = f'UPDATE empleados SET foto="{nuevoNombreFoto}" WHERE id={_id};'
                    cursor.execute(sql)
                    conn.commit()

                sql = f'UPDATE empleados SET nombre="{_name}", correo="{_email}" WHERE id={_id}'
                cursor.execute(sql)
                conn.commit()
                return redirect('/employees')
        else:
            return render_template('404.html'), 404
    except Exception as e:
        return e

@app.route('/deleteemployee/<int:id>')
def delete_employee(id):
    cursor = None
    try:
        if session['username']:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sql = "SELECT foto FROM empleados WHERE id = (%s)"
            datos = [id]
            cursor.execute(sql, datos)
            row = cursor.fetchone()

            try:
                os.remove(os.path.join(app.config['UPLOADS'], row['foto']))
            except:
                pass

            sql = "DELETE FROM empleados WHERE id = (%s)"
            cursor.execute(sql, datos)
            conn.commit()
            return redirect('/employees')
        else:
            return render_template('404.html'), 404
    except Exception as e:
        return e


# TODO Users

@app.route('/users', methods=['GET', 'POST'])   
def users():
    cursor = None    
    try:
        if session['admin']:
            sql = 'SELECT * FROM tbl_user'
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(sql)
            cursor = cursor.fetchall()
            print(cursor)
            cabecera = ['Nombre', 'E-mail', 'Acciones']
            data['message'] = 'Usuarios del Sistema'

            return render_template('login/users.html', cursor=cursor, cabecera=cabecera, data=data)
        else:
           return render_template('404.html'), 404
    except pymysql.err.OperationalError:
        data['errbd'] = True
        return render_template('login/users.html', data=data)
    except Exception as e:
        return e


@app.route('/newuser')
def add_user_view():
    data['message'] = 'Alta de Usuarios'
    return render_template('login/add.html',data=data)

@app.route('/adduser',  methods=['GET', 'POST'])
def add_user():
    cursor = None
    try: 
        if session['admin']:
            _name = request.form['inputName']
            _email = request.form['inputEmail']
            _password = request.form['inputPassword']
            # validate the received values
            if _name and _email and _password and request.method == 'POST':
            #do not save password as a plain text
                _hashed_password = _password
                # _hashed_password = encrypted_key.encrypt(_password)
                # save edits
                sql = "INSERT INTO tbl_user(user_name, user_email, user_password) VALUES(%s, %s, %s)"
                datos = (_name, _email, _hashed_password)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, datos)
                conn.commit()
            return redirect('/users')
        else:
            return render_template('404.html'), 404
    except Exception as e:
        return e


@app.route('/edituser/<int:id>')
def edit_user(id):
    cursor = None
    data['message'] = 'Editar de Usuario'
    try:
        if session['admin']:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM tbl_user WHERE user_id=%s", id)
            row = cursor.fetchone()
            return render_template('login/edit.html', row=row, data=data)
        else:
            return render_template('404.html'), 404
    except Exception as e:
        return e


@app.route('/updateuser', methods=['GET', 'POST'])
def update_user():
    cursor = None
    try:
        if session['admin']:
            _name = request.form['inputName']
            _password = request.form['inputPassword']
            _id = request.form['inputId']
            # validate the received values
            if _name and _password and _id and request.method == 'POST':
                #do not save password as a plain text
                # _hashed_password = encrypted_key.encrypt(_password)
                _hashed_password = _password
                # save edits
                sql = "UPDATE tbl_user SET user_name=%s, user_password=%s WHERE user_id=%s"
                datos = (_name, _hashed_password, _id,)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, datos)
                conn.commit()
                return redirect('/users')
        else:
            return render_template('404.html'), 404
    except Exception as e:
        return e

@app.route('/deleteuser/<int:id>')
def delete_user(id):
    cursor = None
    try:
        if session['admin']:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tbl_user WHERE user_id=%s", (id,))
            conn.commit()
            return redirect('/users')
        else:
            return render_template('404.html'), 404
    except Exception as e:
        return e


if __name__ == '__main__':
    # Captura del Error 404, se puede hacer con los otros Errores
    app.register_error_handler(404,page_not_found)
    # Modo Debugg
    app.run(debug=True)
