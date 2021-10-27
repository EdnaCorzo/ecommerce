from flask import Flask, render_template, request, jsonify, redirect, session
from flask_login import LoginManager,login_user,logout_user,login_required,current_user
from flask_wtf import form
from formas import FormComent, FormEditarUsuario, FormEliminarProduct, FormEliminarUsuario, FormLista, FormProduct, FormUser, Formlogin, FormEditarProduct
import os
import db
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
from PIL import Image

app = Flask(__name__)
app.secret_key=os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

#rutas principales:
@app.route('/', methods=['GET'])
def index():
    return render_template('inicio.html')

@app.route('/catalogoproductos/', methods=['GET', 'POST'])
def catalogo():
    output= db.listaProductos()
    return render_template('catalogo.html', productos= output)

@app.route('/detalleproducto/<nomprodu>', methods=['GET', 'POST'])
def produdetail(nomprodu):
    formulario= FormComent()
    output= db.listaProductos()
    idproducto =  db.get_producto_nombre_db(nomprodu)
    comentarios =  db.listaComentariosPorProducto(idproducto)
    return render_template('detalleproducto.html', productos= output, nomprodu=nomprodu, form= formulario, comentarios= comentarios)

@app.route('/nuevocomentario/', methods=['GET', 'POST'])
def addcomentario():
    formulario= FormComent()
    if formulario.validate_on_submit():
        pro= formulario.producto.data
        usu= formulario.usuario.data
        men= formulario.mensaje.data
        estado= db.addComent(pro, usu, men)
        if estado:
            return render_template('comentarioexito.html')
        else:
            return "<h1>Fallo en la creacion del comentario</h1>"
    else:
        return "<h1>Usuario debe iniciar sesión para dejar comentarios</h1>"

@app.route('/comentariocreado/', methods=['GET'])
def comencreado():
    return render_template('comentarioexito.html')

@app.route('/nuevoenlista/', methods=['GET', 'POST'])
def addlista():
    if request.method=='POST':
        usu= request.form['usuario']
        pro= request.form['producto']
        estado= db.addLista(usu, pro)
        if estado:
            return render_template('listaexito.html')
        else:
            return "<h1>Fallo al añadir</h1>"
    else:
        return "<h1>Usuario debe iniciar sesión para añadir productos a su lista de deseos</h1>"

@app.route('/listaanadido/', methods=['GET'])
def comenlista():
    return render_template('listaexito.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    formulario= Formlogin()
    return render_template('login.html', form=formulario)

@app.route('/register/', methods=['GET', 'POST'])
def registro():
    formulario= FormUser()
    return render_template('register.html', form=formulario)

#Rutas despues del login:
@app.route('/bienvenido/', methods=['GET', 'POST'])
def bienvenido():
    formulario= Formlogin()
    if request.method=='POST':
        user= request.form['usuario']
        clave= request.form['contrasena']
        tipoa= 'admin'
        tipou= 'user'
        resultSet= db.get_user_db(user)
        if resultSet!=None:
            if user==resultSet[2] and check_password_hash(resultSet[5], clave) and tipoa==resultSet[6]:
                id=resultSet[0]
                session["logedin"]= True
                session["usuario"]= user
                session["id"]=id
                session["tipo"] = tipoa
                return redirect(f'/dashboard/{user}')
            elif user==resultSet[2] and check_password_hash(resultSet[5], clave) and tipou==resultSet[6]:
                id=resultSet[0]
                session["logedin"]= True
                session["usuario"]= user
                session["id"]=id
                return redirect('/inicio-sesion/')
            else:
                return "<h1>Contraseña invalida</h1>"
        else:
            return render_template('inicio-fallido.html')
    else:
        return render_template('login.html', form=formulario)

@login_manager.user_loader
def load_user(user):
	return user

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/login/')

@app.route('/dashboard/')
@app.route('/dashboard')
def dashboard():
    return redirect ('/')

@app.route('/dashboard/<user>', methods=['GET'])
def dash(user):
    if session and user == session['usuario'] and session['tipo']== 'admin':
    	 return render_template('dashboard.html')
    else:
        return redirect ('/')

@app.route('/inicio-sesion/', methods=['GET'])
def inisesion():
    return render_template('inicio-sesion.html')

@app.route('/listadeseos/', methods=['GET'])
def listadeseos():
    if session:
        idusu = session["id"]
        listaDeseo = db.getListaDeseos(idusu)
        return render_template('lista-deseos.html', listaDeseo=listaDeseo)
    else:
        return "<h1>Por favor inicie sesion para ver su lista de deseos</h1>"

#Aqui inicia la gestion de usuarios: 
#Creacion
@app.route('/UsuarioNuevo/', methods=['GET', 'POST'])
def guardarUsuario():
    formulario= FormUser()
    if request.method=='POST':
        nom= formulario.nombre.data
        usu= formulario.usuario.data
        cor= formulario.correo.data
        idu= formulario.idusuario.data
        hashPwd = generate_password_hash(formulario.contrasena.data)
        tip= "user"
        estado= db.addUsuario(nom, usu, cor, idu, hashPwd, tip)
        if estado:
            return render_template('login-exitoso.html')
        else:
            return "<h1>Fallo en la creacion del usuario</h1>"
    else:
        return render_template("register.html", form= formulario)

#Edicion
@app.route('/editar-usuario/', methods=['GET', 'POST'])
def ediusu():
    formulario= FormEditarUsuario()
    return render_template('editar-usuario.html', form=formulario)

@app.route('/listUser/', methods=['GET'])
def listuser():
    formulario= FormEditarUsuario()
    idp = request.args.get('idusuario')
    output= db.get_user_db(idp)
    if output!=None:
        nom=output[1]
        usu=output[2]
        cor=output[3]
        idu=output[4]
        con=output[5]
        tip=output[6]
        return render_template('editar-usuario.html', nom1=nom, usu1=usu, cor1=cor, idu1=idu, con1=con, tip1=tip, form=formulario)

@app.route('/UsuarioActualizado/', methods=['GET', 'POST'])
def actualizarUsuario():
    formulario= FormEditarUsuario()
    if request.method=='POST':
        nom= formulario.nombre.data
        usu= formulario.usuario.data
        cor= formulario.correo.data
        idu= formulario.idusuario.data
        hashPwd = generate_password_hash(formulario.contrasena.data)
        tip= formulario.tipo.data
        estado= db.editUser(nom, usu, cor, idu, hashPwd, tip)
        if estado:
            return "<h1>Usuario actualizado exitosamente</h1>"
        else:
            return "<h1>Fallo en la actualizacion del usuario</h1>"
    else:
        return render_template('editar-usuario.html', form= formulario)

#Eliminacion
@app.route('/eliminar-usuario/', methods=['GET', 'POST'])
def eliusu():
    formulario= FormEliminarUsuario()
    return render_template('eliminar-usuario.html', form=formulario)

@app.route('/listUsuarios/', methods=['GET'])
def listusu():
    formulario= FormEliminarUsuario()
    idp = request.args.get('idusuario')
    output= db.get_user_db(idp)
    if output!=None:
        nom=output[1]
        usu=output[2]
        cor=output[3]
        idu=output[4]
        con=output[5]
        tip=output[6]
        return render_template('eliminar-usuario.html', nom1=nom, usu1=usu, cor1=cor, idu1=idu, con1=con, tip1=tip, form=formulario)

@app.route('/UsuarioEliminado/', methods=['GET', 'POST'])
def eliminarUsuario():
    formulario= FormEliminarUsuario()
    if request.method=='POST':
        usu= formulario.usuario.data
        estado= db.deleteUser(usu)
        if estado:
            return "<h1>Usuario eliminado exitosamente</h1>"
        else:
            return "<h1>Fallo en la eliminacion del usuario</h1>"
    else:
        return render_template('eliminar-usuario.html', form= formulario)

#Aqui inicia la gestion de productos:
#Creacion
@app.route('/crearproducto/', methods=['GET', 'POST'])
def creaproducto():
    formulario= FormProduct()
    return render_template('creacion-producto.html', form=formulario)

@app.route('/creado/', methods=['GET'])
def creado():
    return render_template('crear-exito.html')

def save_picture(form_picture,folder):
    #Creamos un nombre aleatorio al fichero
    random_hex = secrets.token_hex(8)
    #Sacamos la extensión de la imagen que vamos a guardar
    _, f_ext = os.path.splitext(form_picture.filename)
    #Armamos el nombre del fichero con la extensión
    picture_fname = random_hex+f_ext
    #Creamos el path donde vamos a guardar
    picture_path = os.path.join(app.root_path,'static/'+folder,picture_fname)
    #Redimensionar la imagen
    output_size = (450,233)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    #Guardamos la imagen
    i.save(picture_path)
    #Devolvemos el nuevo path
    return picture_fname

@app.route('/ProductoNuevo/', methods=['GET', 'POST'])
def guardarProducto():
    formulario= FormProduct()
    if formulario.validate_on_submit():
        cod= formulario.codigo.data
        nom= formulario.nombre.data
        pre= formulario.precio.data
        qty= formulario.existencia.data
        cor= formulario.descorta.data
        lar= formulario.deslarga.data
        ima= save_picture(formulario.imagen.data,'images')
        estado= db.addProduct(cod, nom, pre, qty, cor, lar, ima)
        if estado:
            return render_template('crear-exito.html')
        else:
            return "<h1>Fallo en la creacion del producto</h1>"
    else:
        return render_template('creacion-producto.html', form= formulario)

#Edicion y eliminacion
@app.route('/editar-producto/', methods=['GET', 'POST'])
def ediprodu():
    formulario= FormEditarProduct()
    return render_template('editar-producto.html', form=formulario)

@app.route('/listProductById/', methods=['GET'])
def listProductById():
    formulario= FormEditarProduct()
    idp = request.args.get('idproducto')
    output= db.get_produ_db(idp)
    if output!=None:
        cod=output[1]
        nom=output[2]
        pre=output[3]
        qty=output[4]
        cor=output[5]
        lar=output[6]
        return render_template('editar-producto.html', cod1=cod, nom1=nom, pre1=pre, qty1=qty, cor1=cor, lar1=lar, form=formulario)

@app.route('/editado/', methods=['GET'])
def editado():
    return render_template('editar-exito.html')

@app.route('/ProductoActualizado/', methods=['GET', 'POST'])
def actualizarProducto():
    formulario= FormEditarProduct()
    if request.method=='POST':
        cod= formulario.codigo.data
        nom= formulario.nombre.data
        pre= formulario.precio.data
        qty= formulario.existencia.data
        cor= formulario.descorta.data
        lar= formulario.deslarga.data
        estado= db.editProduct(cod, nom, pre, qty, cor, lar)
        if estado:
            return render_template('editar-exito.html')
        else:
            return "<h1>Fallo en la actualizacion del producto</h1>"
    else:
        return render_template('editar-producto.html', form= formulario)

#Eliminacion
@app.route('/eliminar-producto/', methods=['GET', 'POST'])
def eliprodu():
    formulario= FormEliminarProduct()
    return render_template('eliminar-producto.html', form=formulario)

@app.route('/listProduct/', methods=['GET'])
def listProduct():
    formulario= FormEliminarProduct()
    idp = request.args.get('idproducto')
    output= db.get_produ_db(idp)
    if output!=None:
        cod=output[1]
        nom=output[2]
        pre=output[3]
        qty=output[4]
        cor=output[5]
        lar=output[6]
        return render_template('eliminar-producto.html', cod1=cod, nom1=nom, pre1=pre, qty1=qty, cor1=cor, lar1=lar, form=formulario)

@app.route('/eliminado/', methods=['GET'])
def eliminado():
    return render_template('eliminar-exito.html')

@app.route('/ProductoEliminado/', methods=['GET', 'POST'])
def eliminarProducto():
    formulario= FormEliminarProduct()
    if request.method=='POST':
        cod= formulario.codigo.data
        estado= db.deleteProduct(cod)
        if estado:
            return render_template('eliminar-exito.html')
        else:
            return "<h1>Fallo en la eliminacion del producto</h1>"
    else:
        return render_template('eliminar-producto.html', form= formulario)

#Aqui inicia la gestion de comentarios:
@app.route('/gestioncomentarios/', methods=['GET'])
def comentario():
    return render_template('gestion-comentarios.html')

if __name__=='__main__':
    app.run(port=5001, debug=True)