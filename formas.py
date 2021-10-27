from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired

class FormUser(FlaskForm):
    nombre = StringField('Nombre y Apellido', validators=[DataRequired(message='No dejar vacío, completar')])

    usuario = StringField('Usuario', validators=[DataRequired(message='No dejar vacío, completar')])

    correo = StringField('Correo Electronico', validators=[DataRequired(message='No dejar vacío, completar')])

    idusuario = StringField('No. de Identificacion', validators=[DataRequired(message='No dejar vacío, completar')])

    contrasena = PasswordField('Contraseña', validators=[DataRequired(message='No dejar vacío, completar')])

    botonGuardar = SubmitField('Crear Usuario')

class Formlogin(FlaskForm):
    usuario = StringField('Usuario', validators=[DataRequired(message='No dejar vacío, completar')])

    contrasena = PasswordField('Contraseña', validators=[DataRequired(message='No dejar vacío, completar')])

    recordar = BooleanField('Recordar Usuario')
    enviar = SubmitField('Iniciar Sesión')

class FormProduct(FlaskForm):
    codigo = StringField('Codigo del Producto', validators=[DataRequired(message='No dejar vacío, completar')])

    nombre = StringField('Nombre del Producto', validators=[DataRequired(message='No dejar vacío, completar')])

    precio = StringField('Precio del Producto', validators=[DataRequired(message='No dejar vacío, completar')])

    existencia = StringField('Cantidad en Existencia', validators=[DataRequired(message='No dejar vacío, completar')])

    descorta = StringField('Descripcion Corta', validators=[DataRequired(message='No dejar vacío, completar')])

    deslarga = StringField('Descripcion Larga', validators=[DataRequired(message='No dejar vacío, completar')])

    imagen = FileField('Inserte una imagen (jpg o png)',validators=[FileAllowed(['jpg','png'])])

    botonGuardar = SubmitField('Crear Producto')

class FormEditarProduct(FlaskForm):
    codigo = StringField('Codigo del Producto', validators=[DataRequired(message='No dejar vacío, completar')])

    nombre = StringField('Nombre del Producto', validators=[DataRequired(message='No dejar vacío, completar')])

    precio = StringField('Precio del Producto', validators=[DataRequired(message='No dejar vacío, completar')])

    existencia = StringField('Cantidad en Existencia', validators=[DataRequired(message='No dejar vacío, completar')])

    descorta = StringField('Descripcion Corta', validators=[DataRequired(message='No dejar vacío, completar')])

    deslarga = StringField('Descripcion Larga', validators=[DataRequired(message='No dejar vacío, completar')])

    botonEditar = SubmitField('Editar Producto')

class FormEliminarProduct(FlaskForm):
    codigo = StringField('Codigo del Producto', validators=[DataRequired(message='No dejar vacío, completar')])

    nombre = StringField('Nombre del Producto', validators=[DataRequired(message='No dejar vacío, completar')])

    precio = StringField('Precio del Producto', validators=[DataRequired(message='No dejar vacío, completar')])

    existencia = StringField('Cantidad en Existencia', validators=[DataRequired(message='No dejar vacío, completar')])

    descorta = StringField('Descripcion Corta', validators=[DataRequired(message='No dejar vacío, completar')])

    deslarga = StringField('Descripcion Larga', validators=[DataRequired(message='No dejar vacío, completar')])

    botonEliminar = SubmitField('Eliminar Producto')

class FormEditarUsuario(FlaskForm):
    nombre = StringField('Nombre y Apellido', validators=[DataRequired(message='No dejar vacío, completar')])

    usuario = StringField('Usuario', validators=[DataRequired(message='No dejar vacío, completar')])

    correo = StringField('Correo Electronico', validators=[DataRequired(message='No dejar vacío, completar')])

    idusuario = StringField('No. de Identificacion', validators=[DataRequired(message='No dejar vacío, completar')])

    contrasena = PasswordField('Contraseña', validators=[DataRequired(message='No dejar vacío, completar')])

    tipo = StringField('Rol del usuario (user o admin)', validators=[DataRequired(message='No dejar vacío, completar')])

    botonEditar = SubmitField('Editar Usuario')

class FormEliminarUsuario(FlaskForm):
    nombre = StringField('Nombre y Apellido', validators=[DataRequired(message='No dejar vacío, completar')])

    usuario = StringField('Usuario', validators=[DataRequired(message='No dejar vacío, completar')])

    correo = StringField('Correo Electronico', validators=[DataRequired(message='No dejar vacío, completar')])

    idusuario = StringField('No. de Identificacion', validators=[DataRequired(message='No dejar vacío, completar')])

    contrasena = PasswordField('Contraseña', validators=[DataRequired(message='No dejar vacío, completar')])

    tipo = StringField('Rol del usuario (user o admin)', validators=[DataRequired(message='No dejar vacío, completar')])

    botonEliminar = SubmitField('Eliminar Usuario')

class FormComent(FlaskForm):
    producto = StringField('producto', validators=[DataRequired(message='No dejar vacío, completar')])

    usuario = StringField('Usuario', validators=[DataRequired(message='No dejar vacío, completar')])

    mensaje = StringField('Añada su comentario del producto', validators=[DataRequired(message='No dejar vacío, completar')])

    enviar = SubmitField('Enviar Comentario')

class FormLista(FlaskForm):
    producto = StringField('producto', validators=[DataRequired(message='No dejar vacío, completar')])

    usuario = StringField('Usuario', validators=[DataRequired(message='No dejar vacío, completar')])

    anadir = SubmitField('Añadir a Lista de deseos')