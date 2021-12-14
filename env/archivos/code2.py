def delete_all():
    todos.delete_many({})
    return redirect(url_for('index'))                        