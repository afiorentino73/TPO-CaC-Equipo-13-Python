from __future__ import print_function
from __future__ import unicode_literals
from flask import Flask
from flask import render_template, request, redirect

import musicbrainzngs
import sys

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

#Api Musica validacion
musicbrainzngs.set_useragent(
    "python-musicbrainzngs-example",
    "0.1",
    "https://github.com/alastair/python-musicbrainzngs/",
)

#App Musica
def show_release_details(artist,album):
    
    simage = []
    result = musicbrainzngs.search_releases(artist=artist, release=album, type=['album'], status='official',limit=5)
    
    if "release-list" in result:
        for rel in result['release-list']:
            if  int(rel['ext:score'])>=80:
                #rel['status']=='Official' and
                disk = rel['title']
                artista = rel["artist-credit-phrase"]
                #print(rel['id'],disco,artista)
                try:
                    data = musicbrainzngs.get_image_list(rel['id'])
                    #if data.status_code!=404:
                    if "images" in data:
                        for image in data["images"]:
                            if "Front" in image["types"] and image["approved"]:
                                foto = image["thumbnails"]["small"]
                    else:
                        foto = ''
                        #print("No foto")
                    sdisco = (disk,artista,foto)
                    simage.append(sdisco)
                    #print(simage)
                
                except Exception as e:
                    #Print("Error")
                    sdisco=''
                    #return
            else:
                foto=''
                #print("No score")
        return(simage)
    
    #if not result['release-list']:
    #    simage = ["Sin resultados"]
    #for rel in result['release-list']:
    #    disk = rel['title']
    #    artista = rel["artist-credit-phrase"]
    #    data = musicbrainzngs.get_image_list(rel['id'])
    #    if not data['images']:
    #        foto=''
    #    for image in data["images"]:
    #        foto = image["thumbnails"]["small"]
    #        break
    #    sdisco = (disk,artista,foto)
    #    simage.append(sdisco)
    #return(simage)
    
    
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
    #print(db_discos)
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
    
    datos = (_nombre, _grupo, nuevoNombreFoto)
    
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
    
    return render_template('/discos/edit.html', udiscos=upd_disco)

@app.route('/addext/',methods=['GET'])
def addext():
    
    sdisco_nombre = request.args.get('sdisco_nombre')
    sdisco_grupo = request.args.get('sdisco_grupo')
    sdisco_foto = request.args.get('sdisco_foto')

    datosext = (sdisco_nombre, sdisco_grupo, sdisco_foto)

    sql = "INSERT INTO `discos` (`Id`, `nombre`, `grupo`, `foto`)\
        VALUES (NULL, %s, %s, %s);"
    
    #datos =  ('Clicks Modernos3', 'Charly Garcia', 'clicks_foto3.jpg')
    
    conn = mysql.connection
    
    cur = conn.cursor()
    
    cur.execute(sql,datosext)
    
    conn.commit()
    
    return redirect('/discos')

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

@app.route('/search', methods=['POST'])
def search():
   
    album = request.form['stxtNombre']
    artist = request.form['stxtGrupo']
    rs_discos = show_release_details(album,artist)
    
    return render_template('/discos/search.html', sdiscos=rs_discos)
 
#Lineas req by python

if __name__=='__main__':
    app.run(debug=True)
