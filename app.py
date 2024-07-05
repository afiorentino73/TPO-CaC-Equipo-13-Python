from flask import Flask
from flask import render_template, request, redirect
from flask_mysqldb import MySQL

#Importamos datetime
from datetime import datetime

#Declaracion App
app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='test1'

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
    cursor = conn.cursor()
    cursor.execute(sql)
   
    db_discos = cursor.fetchall()
    
    #Print
    # print("-"*60)
    # for disco in db_discos:
    #    print(disco)
    #    print("-"*60)
    
    
    cursor.close()
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
    
    cursor = conn.cursor()
    
    cursor.execute(sql,datos)
    
    conn.commit()
    
    return redirect('/discos')
    
    
#Lineas req by python

if __name__=='__main__':
    app.run(debug=True)
