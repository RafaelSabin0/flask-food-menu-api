from flask import Flask, jsonify
from flask_pymongo import PyMongo
from routes.food_routes import food_routes
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    app = Flask(__name__)


app.config['MONGO_URI'] = os.environ.get('MONGO_ADDRESS')
app.config['MONGO_DBNAME'] = os.environ.get('DB_NAME')

mongo = PyMongo(app)

app.register_blueprint(food_routes)

@app.route('/')
def lesgo():
   return "<h1>Food Menu API in Flask </h1>"


app.run(port=5000, host='localhost', debug=True)