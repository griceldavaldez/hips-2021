from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import crud
from .forms import MD5SumForm,LimiteProcesoForm,GeneralForm,AppPeligrosaForm
from BaseDatos.modelos import Md5sum, General, AlarmaPrevencion, AplicacionPeligrosa, LimiteProceso
from BaseDatos import dao


#---- MD5 --------------------------------------------------------------
@crud.route('/md5', methods=['GET', 'POST'])
@login_required
def list_md5():

    modulo = 'md5'
    label = 'Md5 Sum'
    lista_valores = dao.obtenerMd5sum()

    return render_template('crud/'+modulo+'/list_'+modulo+'.html',
                           lista_valores=lista_valores, title=label, label=label)


@crud.route('/md5/add', methods=['GET', 'POST'])
@login_required
def add_md5():
    modulo = 'md5'
    add_registro = True
    form = MD5SumForm()
    label = 'Md5 Sum'

    if form.validate_on_submit():
        md5 = Md5sum(None, form.directorio.data, None)

        try:
            dao.insertarMd5sum(md5)
            flash('Se agregó correctamente '+label+'.', 'info')
        except:
            flash('Error: No se pudo agregar '+label+'.', 'error')

        return redirect(url_for('crud.list_'+modulo))

    return render_template('crud/'+modulo+'/'+modulo+'.html', action="Add",
                           add_registro=add_registro, form=form,
                           title="Agregar " + label, label=label)


@crud.route('/md5/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_md5(id):

    modulo = 'md5'
    add_registro = False
    form = MD5SumForm()
    label = 'Md5 Sum'

    objeto = dao.obtenerMd5sumPorId(id)
    form = MD5SumForm(obj=objeto)
    if form.validate_on_submit():

        objeto.directorio = form.directorio.data
        
        try:
            dao.actualizarMd5sum(objeto)
            flash('Se actualizó correctamente.', 'info')
        except:
            flash('Error: No se pudo actualizar '+label+'.', 'error')
        return redirect(url_for('crud.list_' + modulo))

    form.directorio.data = objeto.directorio
    return render_template('crud/'+modulo+'/'+modulo+'.html', action="Edit",
                           add_registro=add_registro, form=form,
                           title="Editar " + label, label=label)


@crud.route('/md5/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_md5(id):

    modulo = 'md5'
    label = 'Md5 Sum'

    try:
        dao.eliminarMd5sumPorId(id)
        flash('Se eliminó correctamente.', 'info')
    except:
        flash('Error: No se pudo eliminar '+label+'.', 'error')

    return redirect(url_for('crud.list_' + modulo))

#---- Aplicaciones peligrosas --------------------------------------------------------------
@crud.route('/apel', methods=['GET', 'POST'])
@login_required
def list_apel():
    #Modif-----------------<
    modulo = 'apel'
    label = 'Aplicaciones Peligrosas'
    lista_valores = dao.obtenerAplicacionPeligrosa()
    #Modif----------------->

    return render_template('crud/'+modulo+'/list_'+modulo+'.html',
                           lista_valores=lista_valores, title=label, label=label)


@crud.route('/apel/add', methods=['GET', 'POST'])
@login_required
def add_apel():

    #Modif-----------------<
    modulo = 'apel'
    form = AppPeligrosaForm()
    label = 'Aplicaciones Peligrosas'
    #Modif----------------->

    add_registro = True
    if form.validate_on_submit():

        #Modif-----------------<
        apel =AplicacionPeligrosa(None,form.nombre_sniffer.data)
        #Modif----------------->

        try:
            #Modif-----------------<
            dao.insertarAplicacionPeligrosa(apel)
            #Modif----------------->

            flash('Se agregó correctamente '+label+'.', 'info')
        except:
            flash('Error: No se pudo agregar '+label+'.', 'error')

        return redirect(url_for('crud.list_'+modulo))

    return render_template('crud/'+modulo+'/'+modulo+'.html', action="Add",
                           add_registro=add_registro, form=form,
                           title="Agregar " + label, label=label)


@crud.route('/apel/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_apel(id):

    #Modif-----------------<
    modulo = 'apel'
    form = AppPeligrosaForm()
    label = 'Aplicaciones Peligrosas'
    objeto = dao.obtenerAplicacionPeligrosaPorId(id)
    form = AppPeligrosaForm(obj=objeto)
    #Modif----------------->

    add_registro = False

    if form.validate_on_submit():
        #Modif-----------------<
        objeto.nombre_sniffer = form.nombre_sniffer.data
        #Modif----------------->

        try:
            #Modif-----------------<
            dao.actualizarAplicacionPeligrosa(objeto)
            #Modif----------------->

            flash('Se actualizó correctamente.','info')
        except:
            flash('Error: No se pudo actualizar '+label+'.','error')
        return redirect(url_for('crud.list_' + modulo))

    #Modif-----------------<
    form.nombre_sniffer.data = objeto.nombre_sniffer
    #Modif----------------->

    return render_template('crud/'+modulo+'/'+modulo+'.html', action="Edit",
                           add_registro=add_registro, form=form,
                           title="Editar " + label, label=label)


@crud.route('/apel/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_apel(id):
    #Modif-----------------<
    modulo = 'apel'
    label = 'Aplicación Peligrosa'
    #Modif----------------->

    try:
        #Modif-----------------<
        dao.eliminarAplicacionPeligrosaPorId(id)
        #Modif----------------->

        flash('Se eliminó correctamente.','info')
    except:
        flash('Error: No se pudo eliminar '+label+'.','error')

    return redirect(url_for('crud.list_' + modulo))


    #---- Datos generales --------------------------------------------------------------
@crud.route('/general', methods=['GET', 'POST'])
@login_required
def list_general():
    #Modif-----------------<
    modulo = 'general'
    label = 'Datos Globales'

    datos = dao.obtenerGeneral()

    datos_lista = []
    datos_lista.append(datos)  

    lista_valores = datos_lista
    #Modif----------------->

    return render_template('crud/'+modulo+'/list_'+modulo+'.html',
                           lista_valores=lista_valores, title=label, label=label)


'''@crud.route('/general/add', methods=['GET', 'POST'])
@login_required
def add_general():

    #Modif-----------------<
    modulo = 'general'
    form = GeneralForm()
    label = 'Datos Globales'
    #Modif----------------->

    add_registro = True
    if form.validate_on_submit():

        #Modif-----------------<
        gen =General(None, form.ip.data, form.correo.data, form.contrasenha_correo.data, form.uso_cpu_por_defecto.data, form.uso_memoria_por_defecto.data, form.intento_maximo_ssh.data,form.correo_maximo_por_usuario.data,form.cola_maxima_correo.data)
        #Modif----------------->

        try:
            #Modif-----------------<
            
            #Modif----------------->

            flash('Se agregó correctamente '+label+'.', 'info')
        except:
            flash('Error: No se pudo agregar '+label+'.', 'error')

        return redirect(url_for('crud.list_'+modulo))

    return render_template('crud/'+modulo+'/'+modulo+'.html', action="Add",
                           add_registro=add_registro, form=form,
                           title="Agregar " + label, label=label)
'''

@crud.route('/general/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_general(id):

    #Modif-----------------<
    modulo = 'general'
    form = GeneralForm()
    label = 'Datos Globales'
    objeto = dao.obtenerGeneral()

    form = GeneralForm(obj=objeto)
    #Modif----------------->

    add_registro = False

    if form.validate_on_submit():
        #Modif-----------------<
        objeto.setIP(form.ip.data)
        objeto.setCorreo(form.correo.data)
        objeto.setContrasenhaCorreo(form.contrasenha_correo.data)
        objeto.setUsoCpuPorDefecto(form.uso_cpu_por_defecto.data)
        objeto.setUsoMemoriaPorDefecto(form.uso_memoria_por_defecto.data)
        objeto.setIntentoMaximoSSH(form.intento_maximo_ssh.data)
        objeto.setCorreoMaximoPorUsuario(form.correo_maximo_por_usuario.data)
        objeto.setColaMaximaCorreo(form.cola_maxima_correo.data)

        #Modif----------------->

        try:
            #Modif-----------------<
            dao.actualizarGeneral(objeto)
            #Modif----------------->

            flash('Se actualizó correctamente.','info')
        except:
            flash('Error: No se pudo actualizar '+label+'.','error')
        return redirect(url_for('crud.list_' + modulo))

    #Modif-----------------<
    form.ip.data = objeto.getIP()
    form.correo.data = objeto.getCorreo()
    form.contrasenha_correo.data = objeto.getContrasenhaCorreo()
    form.uso_cpu_por_defecto.data = objeto.getUsoCpuPorDefecto()
    form.uso_memoria_por_defecto.data = objeto.getUsoMemoriaPorDefecto()
    form.intento_maximo_ssh.data = objeto.getIntentoMaximoSSH()
    form.correo_maximo_por_usuario.data = objeto.getCorreoMaximoPorUsuario()
    form.cola_maxima_correo.data = objeto.getColaMaximaCorreo()
    #Modif----------------->

    return render_template('crud/'+modulo+'/'+modulo+'.html', action="Edit",
                           add_registro=add_registro, form=form,
                           title="Editar " + label, label=label)

#---- Límite procesos --------------------------------------------------------------
@crud.route('/limproc', methods=['GET', 'POST'])
@login_required
def list_limproc():
    #Modif-----------------<
    modulo = 'limproc'
    label = 'Límite Procesos'
    lista_valores = dao.obtenerLimiteProceso()
    #Modif----------------->

    return render_template('crud/'+modulo+'/list_'+modulo+'.html',
                           lista_valores=lista_valores, title=label, label=label)


@crud.route('/limproc/add', methods=['GET', 'POST'])
@login_required
def add_limproc():

    #Modif-----------------<
    modulo = 'limproc'
    form = LimiteProcesoForm()
    label = 'Límite Procesos'
    #Modif----------------->

    add_registro = True
    if form.validate_on_submit():

        #Modif-----------------<
        limproc =LimiteProceso(None,form.nombre_proceso.data,form.uso_cpu.data,form.uso_memoria.data,form.tiempo_maximo_ejecucion.data)
        #Modif----------------->

        try:
            #Modif-----------------<
            dao.insertarLimiteProceso(limproc)
            #Modif----------------->

            flash('Se agregó correctamente '+label+'.', 'info')
        except:
            flash('Error: No se pudo agregar '+label+'.', 'error')

        return redirect(url_for('crud.list_'+modulo))

    return render_template('crud/'+modulo+'/'+modulo+'.html', action="Add",
                           add_registro=add_registro, form=form,
                           title="Agregar " + label, label=label)


@crud.route('/limproc/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_limproc(id):

    #Modif-----------------<
    modulo = 'limproc'
    form = LimiteProcesoForm()
    label = 'Límite Procesos'
    objeto = dao.obtenerLimiteProcesoPorId(id)
    form = LimiteProcesoForm(obj=objeto)
    #Modif----------------->

    add_registro = False

    if form.validate_on_submit():
        #Modif-----------------<
        objeto.setNombreProceso(form.nombre_proceso.data)
        objeto.setUsoCpu(form.uso_cpu.data)
        objeto.setUsoMemoria(form.uso_memoria.data)
        objeto.setTiempoMaximoEjecucion(form.tiempo_maximo_ejecucion.data)
        #Modif----------------->

        try:
            #Modif-----------------<
            dao.actualizarLimiteProcesoPorId(objeto)
            #Modif----------------->

            flash('Se actualizó correctamente.','info')
        except:
            flash('Error: No se pudo actualizar '+label+'.','error')
        return redirect(url_for('crud.list_' + modulo))

    #Modif-----------------<
    form.nombre_proceso.data = objeto.getNombreProceso()
    form.uso_cpu.data = objeto.getUsoCpu()
    form.uso_memoria.data = objeto.getUsoMemoria()
    form.tiempo_maximo_ejecucion.data = objeto.getTiempoMaximoEjecucion()
    #Modif----------------->

    return render_template('crud/'+modulo+'/'+modulo+'.html', action="Edit",
                           add_registro=add_registro, form=form,
                           title="Editar " + label, label=label)


@crud.route('/limproc/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_limproc(id):
    #Modif-----------------<
    modulo = 'limproc'
    label = 'Límite Proceso'
    #Modif----------------->

    try:
        #Modif-----------------<
        dao.eliminarLimiteProcesoPorId(id)
        #Modif----------------->

        flash('Se eliminó correctamente.','info')
    except:
        flash('Error: No se pudo eliminar '+label+'.','error')

    return redirect(url_for('crud.list_' + modulo))

#---- Listar alertas --------------------------------------------------------------
@crud.route('/veralert', methods=['GET', 'POST'])
@login_required
def list_veralert():
    #Modif-----------------<
    modulo = 'veralert'
    label = 'Ver alarmas y alertas'
    lista_valores = dao.obtenerAlarmaPrevencion()
    #Modif----------------->

    return render_template('crud/'+modulo+'/list_'+modulo+'.html',
                           lista_valores=lista_valores, title=label, label=label)