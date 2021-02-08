from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from todolist.db import get_db

bp = Blueprint('todos', __name__)

@bp.route('/')
def index():
    db = get_db()
    items = db.execute(
        'SELECT id, title, body, created '
        ' FROM todo'
        ' ORDER by created DESC'
    ).fetchall()
    return render_template('todos/index.html', items=items)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
               'INSERT INTO todo (title, body)'
               ' VALUES (?, ?)', (title, body) 
            )
            db.commit()
            return redirect(url_for('.index'))

    return render_template('todos/create.html')


def get_item(id):
    item = get_db().execute(
        'SELECT id, title, body, created'
        ' FROM todo'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if item is None:
        abort(404, "Item id {0} doesn't exist.".format(id))

    return item

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    item = get_item(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE todo SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('todos.index'))

    return render_template('todos/update.html', item=item)


@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_item(id)
    db = get_db()
    db.execute('DELETE FROM todo WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('todos.index'))