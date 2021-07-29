from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import crud
from .forms import MD5SumForm,LimiteProcesoForm,GeneralForm,AppPeligrosaForm
from BaseDatos.modelos import Md5sum, General, AlarmaPrevencion, AplicacionPeligrosa, LimiteProceso
from BaseDatos import dao



# Department Views


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
    form = MD5SumForm
    label = 'Md5 Sum'

    if form.validate_on_submit():
        md5 = Md5sum(directorio=form.directorio.data)

        try:
            dao.insertarMd5sum(md5)
        except:
            flash('Error: No se pudo agregar '+label+'.')

        return redirect(url_for('crud.list_'+modulo))

    return render_template('crud/'+modulo+'/'+modulo+'.html', action="Add",
                           add_registro=add_registro, form=form,
                           title="Agregar " + label, title=label, label=label)


@crud.route('/md5/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_md5(id):

    modulo = 'md5'
    add_registro = False
    form = MD5SumForm
    label = 'Md5 Sum'

    objeto = dao.obtenerMd5sumPorId(id)
    form = MD5SumForm(obj=objeto)
    if form.validate_on_submit():

        objeto.directorio = form.directorio.data
        
        try:
            dao.actualizarMd5sum(objeto)
            flash('Se actualizó correctamente.')
        except:
            flash('Error: No se pudo actualizar '+label+'.')
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
        flash('Se eliminó correctamente.')
    except:
        flash('Error: No se pudo eliminar '+label+'.')

    return redirect(url_for('crud.list_' + modulo))