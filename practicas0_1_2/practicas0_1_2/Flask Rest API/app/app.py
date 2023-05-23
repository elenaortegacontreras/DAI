#./app/app.py
from flask import Flask, jsonify, request, Response
from bson.json_util import dumps
from pymongo import MongoClient
from flask_restful import Resource, Api
from bson import ObjectId

#--------------------------------------------------------------------------------------------
''' Flask Rest API usando librería flask-restfull'''
#--------------------------------------------------------------------------------------------

# Conectar al servicio (docker) "mongo" en su puerto estandar
client = MongoClient("mongo", 27017)

# http://localhost:5000

app = Flask(__name__)
api = Api(app)

# Base de datos
db = client.cockteles

# para devolver una lista (GET), o añadir (POST)
class Recipes(Resource):
    def get(self):
        lista = []
        arg = request.args.get('con')
        if arg == None:
            buscados = db.recipes.find().sort('name')
        else:
            arg = arg.capitalize()
            buscados = db.recipes.find({ "ingredients": { "$elemMatch": { "name":arg } } }).sort('name')
            if not buscados:
                return jsonify({'error':'Not found'}), 404
        for recipe in buscados:
            recipe['_id'] = str(recipe['_id']) # casting a string (es un ObjectId)
            lista.append(recipe)
        return jsonify(lista)
    
    def post(self):
        resultado = db.recipes.insert_one(
            {   
                "name":request.json['name'],
                "ingredients":request.json['ingredients'],
                "instructions":request.json['instructions'],
                "slug":request.json['slug']
            }
        )
        id = resultado.inserted_id
        recipe = db.recipes.find_one({"_id":ObjectId(id)})
        recipe = str(recipe) # casting a string (es un ObjectId)
        return jsonify("Nuevo registro creado: :  " + recipe)

api.add_resource(Recipes, '/f_restfull/api/recipes')

# para devolver una, modificar o borrar
class Recipes2(Resource):
    def get(self, id):
        buscado = db.recipes.find_one({'_id':ObjectId(id)})
        if buscado:
            buscado['_id'] = str(buscado['_id']) # casting a string (es un ObjectId)
            return jsonify(buscado)
        else:
            return jsonify({'error':'Not found'}), 404
        
    def put(self, id):
        buscado = db.recipes.find_one({'_id':ObjectId(id)})
        if buscado:
            db.recipes.update_one({'_id':ObjectId(id)}, {"$set": 
            {
                "name":request.json['name'],
                "ingredients":request.json['ingredients'],
                "instructions":request.json['instructions'],
                "slug":request.json['slug']
            } }
        )
            buscado = db.recipes.find_one({'_id':ObjectId(id)})
            buscado['_id'] = "Registro modificado :  " +  str(buscado['_id']) # casting a string (es un ObjectId)
            return jsonify(buscado)
        else:
            return jsonify({'error':'Not found'}), 404
    
    def delete(self, id):
        buscado = db.recipes.find_one({'_id':ObjectId(id)})
        if buscado:
            buscado['_id'] = str(buscado['_id']) # casting a string (es un ObjectId)
            db.recipes.delete_one({'_id':ObjectId(id)})
            return jsonify("ID registro borrado :  " + str(buscado['_id']))
        else:
            return jsonify({'error':'Not found'}), 404
        
api.add_resource(Recipes2, '/f_restfull/api/recipes/<id>')

if __name__ == '__main__':
    app.run(debug=True)