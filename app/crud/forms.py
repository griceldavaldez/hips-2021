from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Length


class MD5SumForm(FlaskForm):
    directorio = StringField('Directorio', validators=[DataRequired(), Length(255)])
    submit = SubmitField('Confirmar')

class AppPeligrosaForm(FlaskForm):
    nombre_sniffer = StringField('Nombre Sniffer', validators=[DataRequired(), Length(32)])

class LimiteProcesoForm(FlaskForm):
    nombre_proceso = StringField('Nombre Proceso', validators=[DataRequired(), Length(32)])
    uso_cpu = IntegerField('Uso CPU', [DataRequired()])
    uso_memoria = IntegerField('Uso CPU', [DataRequired()])
    tiempo_maximo_ejecucion = IntegerField('Uso CPU', [DataRequired()])

class GeneralForm(FlaskForm):
    ip = StringField('IP', validators=[DataRequired(), Length(32)])
    correo = StringField('Correo E.', validators=[DataRequired(), Length(100)])
    contrasenha_correo = PasswordField('Password Correo', validators=[DataRequired(), Length(100)])
    uso_cpu_por_defecto = IntegerField('Uso CPU Default', [DataRequired()])
    uso_memoria_por_defecto = IntegerField('Uso Memoria Default', [DataRequired()])
    intento_maximo_ssh = IntegerField('Intento Máximo SSH', [DataRequired()])
    correo_maximo_por_usuario = IntegerField('Correo Máx. por usuario', [DataRequired()])
    cola_maxima_correo = IntegerField('Cola Máx. por correo', [DataRequired()])