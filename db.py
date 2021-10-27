import sqlite3
from sqlite3.dbapi2 import Error

def conectar():
    dbname= 'ecommerce.db'
    conn= sqlite3.connect(dbname)
    return conn

def listaUsuarios():
    conn= conectar()
    cursor= conn.execute("select * from Usuarios;")
    resultusu= list(cursor.fetchall())
    conn.close()
    return resultusu

def get_user_db(userid):
    conn= conectar()
    cursor= conn.execute("select * from Usuarios where usuario='"+userid+"';")
    resultSet= cursor.fetchone()
    conn.close()
    return resultSet

def addUsuario(nombre, usuario, correo, iduser, pas, tipo):
    try:
        conn= conectar()
        conn.execute("insert into Usuarios (nombre, usuario, correo, identificacion, contrasena, tipo) values (?,?,?,?,?,?);", (nombre, usuario, correo, iduser, pas, tipo))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        return False

def editUser(nombre, usuario, correo, iduser, pas, tipo):
    try:
        conn= conectar()
        conn.execute("UPDATE Usuarios SET nombre= '" + nombre + "', usuario= '" + usuario + "', correo= '" + correo + "', identificacion= '" + iduser + "', contrasena= '" + pas + "', tipo= '" + tipo + "' WHERE usuario = '" + usuario + "';")
        conn.commit()
        conn.close()
        return True
    except Error as error:
        return False

def deleteUser(usuario):
    try:
        conn= conectar()
        conn.execute("DELETE from Usuarios WHERE usuario= '" + usuario + "';")
        conn.commit()
        conn.close()
        return True
    except Error as error:
        return False

def listaProductos():
    conn= conectar()
    cursor= conn.execute("select * from Producto;")
    resultprodu= list(cursor.fetchall())
    conn.close()
    return resultprodu

def get_produ_db(producod):
    conn= conectar()
    cursor= conn.execute("select * from Producto where codigo='"+producod+"';")
    resultpro= cursor.fetchone()
    conn.close()
    return resultpro

def get_producto_nombre_db(nombre):
    conn= conectar()
    cursor = conn.execute("select id from Producto where nombre='"+nombre+"';")
    resultpro= cursor.fetchone()
    conn.close()
    return resultpro

def addProduct(codigo, nombre, precio, existencia, cordes, londes, imagen):
    try:
        conn= conectar()
        conn.execute("insert into Producto (codigo, nombre, precio, existencia, shortdes, longdes, img) values (?,?,?,?,?,?,?);", (codigo, nombre, precio, existencia, cordes, londes, imagen))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        return False

def editProduct(codigo, nombre, precio, existencia, cordes, londes):
    try:
        conn= conectar()
        conn.execute("UPDATE Producto SET codigo= '" + codigo + "', nombre= '" + nombre + "', precio= '" + precio + "', existencia= '" + existencia + "', shortdes= '" + cordes + "', longdes= '" + londes + "' WHERE codigo = '" + codigo + "';")
        conn.commit()
        conn.close()
        return True
    except Error as error:
        return False

def deleteProduct(codigo):
    try:
        conn= conectar()
        conn.execute("DELETE from Producto WHERE codigo= '" + codigo + "';")
        conn.commit()
        conn.close()
        return True
    except Error as error:
        return False

def addComent(idpro, iduser, mensaje):
    try:
        conn= conectar()
        conn.execute("insert into Comentarios (idproducto, idusuario, mensaje) values (?,?,?);", (idpro, iduser, mensaje))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        return False

def addLista(iduser, idpro):
    try:
        conn= conectar()
        conn.execute("insert into ListaDeseos (idusuario, idproducto) values (?,?);", (iduser, idpro))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        return False

def listaComentarios():
    conn= conectar()
    cursor= conn.execute("select * from Comentarios;")
    resultdeseos= list(cursor.fetchall())
    conn.close()
    return resultdeseos
    
def listaComentariosPorProducto(idProd):
    conn= conectar()
    try:
        cursor= conn.execute('SELECT nombre, mensaje FROM Usuarios INNER JOIN Comentarios on Usuarios.id = Comentarios.idusuario and  Comentarios.idproducto = ?', (idProd))
        resultdeseos= list(cursor.fetchall())
        conn.close()
        return resultdeseos
    except Error as e:
        print(f"error en listacomkentariosporproducto {e}")
        return False

def getListaDeseos(idusu):
    conn= conectar()
    try:
        cursor= conn.execute('SELECT * FROM Producto INNER JOIN ListaDeseos on Producto.id = ListaDeseos.idproducto and  ListaDeseos.idusuario = ?', (idusu, ))
        resultdeseos= list(cursor.fetchall())
        conn.close()
        return resultdeseos
    except Error as e:
        print(f"error en listacomkentariosporproducto {e}")
        return False