from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import sentry_sdk
import metodos
import json

#configuracion del mongo no tocar 
app=Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://proyectoml:8voyOIN8aam7j94e@cluster0.qd2uc.mongodb.net/ProyectoML?retryWrites=true&w=majority"
mongo = PyMongo(app)
 #comprobacion de que funciona 

todos = mongo.db.todos



@app.route('/')
def index():
    saved_todos = todos.find()
    return render_template('index.html', todos=saved_todos)
@app.route('/add', methods=['POST'])
#carga
def add_todo():
    
    new_todo = request.form.get('new-todo')
    new_todo2 = request.form.get('new-todo2')
    todos.insert_one({'text' : new_todo, 'complete' : False})
    todos.insert_one({'text' : new_todo2, 'complete' : False})
    #textolnp= metodos.nlp ('new-todo')
    return redirect(url_for('index'))
#@app.route('/complete/<oid>')
#def complete(oid):
 #   todo_item = todos.find_one({'_id': ObjectId(oid)})
  #  todo_item['complete'] = True
   # todos.save(todo_item)
    #return redirect(url_for('index'))
#
@app.route('/delete_completed')
def delete_completed():
    todos.delete_many({'complete' : True})
    return redirect(url_for('index'))

@app.route('/delete_all')
def delete_all():
    todos.delete_many({})
    return redirect(url_for('index'))


##################

@app.route('/ajax-data',methods=["POST"])
def ajdata():
    texto1 = request.form.get('texto1')
    texto2 = request.form.get('texto2')
    #trasformar texto
    code1=open('./env/archivos/code1.py','w')
    code1.write(texto1)
    code1.close()
    #trasformar texto
    code2=open('./env/archivos/code2.py','w')
    code2.write(texto2)
    code2.close()
    #llama metodos
    rep=metodos.code_sim(r'./env/archivos/code1.py', r'./env/archivos/code2.py', 'jaccard')
    re=metodos.code_sim(r'./env/archivos/code1.py', r'./env/archivos/code2.py', 'tree_edit')
    r=metodos.code_sim(r'./env/archivos/code1.py', r'./env/archivos/code2.py', 'fake_anti_uni')
    tw={'texto1':texto2,'texto2':texto1,"valor Jaccard":rep,"valor tree_edit":re,"valor fake_anti_uni":r}
  
    return json.dumps(tw)

