from flask import Flask, jsonify, Blueprint, request
from flask_pymongo import PyMongo
from bson import ObjectId
from dotenv import load_dotenv
from bson import ObjectId
import os

load_dotenv()

food_routes = Blueprint('food_routes', __name__)
food_conn = Flask(__name__)

#set connection
food_conn.config['MONGO_URI'] = os.environ.get('MONGO_ADDRESS')
food_conn.config['MONGO_DBNAME'] = os.environ.get('DB_NAME')
mongo = PyMongo(food_conn)
db = mongo.cx[os.environ.get('DB_NAME')]


#Routes:
@food_routes.route('/food', methods=['GET'])
def get_food():
   try:
    foods = db.foods.find()
    
    result = []
    for food in foods:
        result.append({
            '_id': str(food['_id']),
            'name': food['name'],
            'price': food['price'],
            'details': food['details'],
            'category': food['category'],
            'rate': food['rate'],
            'shortDescription': food['shortDescription'],
            'imgUrl': food['imgUrl'],
        })
    return jsonify(result)

   except Exception as e:
      print("🚨 Error 🚨:", str(e))
      return jsonify({'🚨 Error 🚨': ' Internal Server Error'}), 500
   


@food_routes.route('/food/<string:id>', methods=['GET'])
def get_food_by_id(id):
    try:
      object_id = ObjectId(id)
      food = db.foods.find_one({'_id': object_id})

      result = []
      if food:
        result.append({
         '_id': str(food['_id']),
         'name': food['name'],
         'price': food['price'],
         'details': food['details'],
         'category': food['category'],
         'rate': food['rate'],
         'shortDescription': food['shortDescription'],
         'imgUrl': food['imgUrl'],
         })
        return jsonify(result)
    
    except Exception as e:
       print("🚨 Error 🚨: ", str(e))
       return jsonify({'🚨 Error 🚨': 'Internal Server Error'}, 500)


@food_routes.route('/food/by_category', methods=['GET'])
def get_food_by_category():
   try:
    food_category = request.args.get('category')
    foods = db.foods.find({'category': food_category})
    
    result = []
    for food in foods:
        result.append({
            '_id': str(food['_id']),
            'name': food['name'],
            'price': food['price'],
            'details': food['details'],
            'category': food['category'],
            'rate': food['rate'],
            'shortDescription': food['shortDescription'],
            'imgUrl': food['imgUrl'],
        })
    return jsonify(result)

   except Exception as e:
      print("🚨 Error 🚨:", str(e))
      return jsonify({'🚨 Error 🚨': 'Internal Server Error'}), 500
   
@food_routes.route('/food/create', methods=['POST'])
def add_food():
   request_data = request.json

   if not request_data:
      return jsonify({"🚨 Oops 🚨": "Check if the request body is valid and try again"}), 400
   
   name = request_data.get('name')
   rate = request_data.get('rate')
   price = request_data.get('price')
   imgUrl = request_data.get('imgUrl')
   details = request_data.get('details')
   category = request_data.get('category')
   shortDescription = request_data.get('shortDescription')

   if not name: 
      return jsonify({"🚨 Oops 🚨": " Name is a required field"}), 403
   
   if db.foods.find_one({'name': name}):
      return jsonify({"🚨 Oops 🚨": "This food is already registered!!!"}), 403
   
   new_food =  {
      'name': name,
      'rate': rate,
      'price': price,
      'imgUrl': imgUrl,
      'details': details,
      'category': category,
      'shortDescription': shortDescription
   }

   db.foods.insert_one(new_food)
   response_info = {
      "info": {
         'name': new_food['name'],
         'rate': new_food['rate'],
         'price': new_food['price'],
         'imgUrl': new_food['imgUrl'],
         'details': new_food['details'],
         'category': new_food['category'],
         'shortDescription': new_food['shortDescription']
      },
      "✅Sucess!!!✅": " New food added to API 😃"
   }

   return jsonify(response_info)

@food_routes.route('/food/delete', methods=['DELETE'])
def delete_food_by_id():
   request_data = request.json
   food_id = request_data.get('id')

   try:        
      if not request_data or len(food_id) == 0 :
         return jsonify({"🚨 Error 🚨": " The ID sent is not valid, check the information entered and try again"}), 400
      
      if not db.foods.find_one({'_id': ObjectId(food_id)}):
         return jsonify({'🚨 Oops 🚨': "Food item not found "}), 404
      
      db.foods.delete_one({'_id': ObjectId(food_id)})
      return jsonify({"✅ Success! ✅": "Food deleted successfully"})

   except ValueError:
      print("🚨 Error 🚨:", str(ValueError))
      return jsonify({'🚨 Error 🚨': ' Invalid ID or format'}), 400
   
