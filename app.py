from flask import Flask
from flask import render_template, request, redirect
from flask_mysqldb import MySQL

#Importamos datetime
from datetime import datetime

#Declaracion App
app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_HOST']='afiorentino.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER']='afiorentino'
app.config['MYSQL_PASSWORD']='tester13'
app.config['MYSQL_DB']='afiorentino$test1'

mysql.init_app(app)

#Rutas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nosotros')
def nosotros():
    return render_template('acercade.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')


@app.route('/discos')
def discos():
    sql = "SELECT * FROM discos"

    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(sql)

    db_discos = cur.fetchall()

    #Print
    # print("-"*60)
    # for disco in db_discos:
    #    print(disco)
    #    print("-"*60)

    cur.close()

    return render_template('discos/discos.html', discos=db_discos)

@app.route('/create')
def create():
    return render_template('discos/create.html')

@app.route('/store', methods=['POST'])
def store():

    _nombre = request.form['txtNombre']
    _grupo = request.form['txtGrupo']
    _foto = request.form['txtFoto']

    now = datetime.now()
    tiempo = now.strftime("%H%M%S")

    if _foto !='':
        nuevoNombreFoto = tiempo+_foto
        #_foto.save("uploads/"+nuevoNombreFoto)

    datos = (_nombre, _grupo,nuevoNombreFoto)

    sql = "INSERT INTO `discos` (`Id`, `nombre`, `grupo`, `foto`)\
        VALUES (NULL, %s, %s, %s);"

    #datos =  ('Clicks Modernos3', 'Charly Garcia', 'clicks_foto3.jpg')

    conn = mysql.connection

    cur = conn.cursor()

    cur.execute(sql,datos)

    conn.commit()

    return redirect('/discos')

@app.route('/destroy/<int:del_id>')
def destroy(del_id):

    sql = "DELETE FROM `discos` WHERE Id = %s"

    conn = mysql.connection

    cur = conn.cursor()

    #cur.execute(sql,id)

    cur.execute(sql,{del_id})

    conn.commit()

    return redirect('/discos')

@app.route('/edit/<int:upd_id>')
def edit(upd_id):

    sql = "SELECT * FROM `discos` WHERE Id = %s"

    conn = mysql.connection

    cur = conn.cursor()

    cur.execute(sql,{upd_id})

    upd_disco = cur.fetchall()

    cur.close()

    return render_template('/discos/edit.html', discos=upd_disco)

@app.route('/update', methods=['POST'])
def update():

    _nombre = request.form['txtNombre']
    _grupo = request.form['txtGrupo']
    _foto = request.form['txtFoto']
    _Id = request.form['txtId']

    now = datetime.now()
    tiempo = now.strftime("%H%M%S")

    if _foto !='':
        nuevoNombreFoto = _foto
        #_foto.save("uploads/"+nuevoNombreFoto)

    datos = (_nombre, _grupo, nuevoNombreFoto, _Id)

    sql = "UPDATE `discos` SET `nombre`=%s,`grupo`=%s,`foto`=%s WHERE `Id`=%s;"

    #datos =  ('Clicks Modernos3', 'Charly Garcia', 'clicks_foto3.jpg')

    conn = mysql.connection

    cur = conn.cursor()

    cur.execute(sql,datos)

    conn.commit()

    cur.close()

    return redirect('/discos')

#Lineas req by python

if __name__=='__main__':
    app.run(debug=True)
