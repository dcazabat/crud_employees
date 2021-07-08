from flask import Flask
from flask import render_template
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

# En remote host
app.config['MYSQL_DATABASE_HOST'] = 'remotemysql.com'
app.config['MYSQL_DATABASE_USER'] = 'rB3cUolUmD'
app.config['MYSQL_DATABASE_PASSWORD'] = 'vXlnbLUILD'
app.config['MYSQL_DATABASE_DB'] = 'rB3cUolUmD'

# En localhost
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = ''
# app.config['MYSQL_DATABASE_DB'] = 'empleados'


mysql.init_app(app)

@app.route('/')
def index():
    #sql = 'insert into empleados (nombre, correo, foto) values ("Daniela Leon", "mdel2002@hotmail.com", "fotodedaniela.png");'
    sql = 'SELECT * FROM empleados'
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    rv = cursor.fetchall()
    conn.commit()

    

    return render_template('empleados/index.html', cursor=rv)


if __name__ == '__main__':
    app.run(debug=True)
