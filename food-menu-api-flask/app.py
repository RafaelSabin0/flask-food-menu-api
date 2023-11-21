from flask import Flask, jsonify
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    app = Flask(__name__)


app.config['MONGO_URI'] = os.environ.get('MONGO_ADDRESS')
app.config['MONGO_DBNAME'] = os.environ.get('DB_NAME')

mongo = PyMongo(app)
db = mongo.cx[os.environ.get('DB_NAME')]

@app.route('/')
def lesgo():
   return "<h1>LesGOO</h1>"

@app.route('/food', methods=['GET'])
def get_food():
   try:
    foods = db.foods.find()
    print(db.list_collection_names())
    
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
      print("Error:", str(e))
      return jsonify({'error': '🚨 Internal Server Error 🚨'}), 500

app.run(port=5000, host='localhost', debug=True)