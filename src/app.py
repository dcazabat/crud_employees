import pymysql
from tables import Results
from flask import Flask, flash, render_template, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flaskext.mysql import MySQL


app = Flask(__name__)
app.secret_key = "daniel"
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

data={
    'title':'App de Flask - Empleados',
    'message':'Bienvenidos al Sitio'
}

def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    try:
        #sql = 'insert into empleados (nombre, correo, foto) values ("Daniela Leon", "mdel2002@hotmail.com", "fotodedaniela.png");'
        sql = 'SELECT * FROM empleados'
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        rv = cursor.fetchall()
        conn.commit()

        return render_template('empleados/index.html', cursor=rv, data=data)
    except:
        return 'Error en busqueda de archivo Index'

@app.route('/users')
def users():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM tbl_user")
        rows = cursor.fetchall()
        table = Results(rows)
        table.border = True
        return render_template('login/users.html', table=table)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/new_user')
def add_user_view():
    return render_template('login/add.html')

@app.route('/add', methods=['POST'])
def add_user():
    conn = None
    cursor = None
    try: 
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        # validate the received values
        if _name and _email and _password and request.method == 'POST':
        #do not save password as a plain text
            _hashed_password = generate_password_hash(_password)
            # save edits
            sql = "INSERT INTO tbl_user(user_name, user_email, user_password) VALUES(%s, %s, %s)"
            data = (_name, _email, _hashed_password,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            flash('User added successfully!')
            return redirect('/')
        else:
            return 'Error while adding user'
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/edit/<int:id>')
def edit_view(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM tbl_user WHERE user_id=%s", id)
        row = cursor.fetchone()
        if row:
            return render_template('login/edit.html', row=row)
        else:
            return 'Error loading #{id}'.format(id=id)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/update', methods=['POST'])
def update_user():
    conn = None
    cursor = None
    try: 
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        _id = request.form['id']
        # validate the received values
        if _name and _email and _password and _id and request.method == 'POST':
            #do not save password as a plain text
            _hashed_password = generate_password_hash(_password)
            print(_hashed_password)
            # save edits
            sql = "UPDATE tbl_user SET user_name=%s, user_email=%s, user_password=%s WHERE user_id=%s"
            data = (_name, _email, _hashed_password, _id,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            flash('User updated successfully!')
            return redirect('/')
        else:
            return 'Error while updating user'
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/delete/<int:id>')
def delete_user(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbl_user WHERE user_id=%s", (id,))
        conn.commit()
        flash('User deleted successfully!')
        return redirect('/')
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

if __name__ == '__main__':
    app.register_error_handler(404,page_not_found)
    app.run(debug=True)