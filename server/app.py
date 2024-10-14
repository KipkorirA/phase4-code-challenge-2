#!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
import os
import logging

# Initialize the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code Challenge API</h1>'

# Retrieve all pizzas
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([pizza.to_dict() for pizza in pizzas])

# Retrieve all restaurants
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    try:
        restaurants = Restaurant.query.all()
        response = jsonify([restaurant.to_dict() for restaurant in restaurants])
        print(response)  
        return response
    except Exception as e:
        print(f"Error: {str(e)}")  
        return make_response(jsonify({'error': str(e)}), 500)
    


# Retrieve a specific restaurant by ID
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant is None:
        return make_response(jsonify({'error': 'Restaurant not found'}), 404)
    return jsonify(restaurant.to_dict())

# Delete a restaurant by ID
@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant is None:
        return make_response(jsonify({'error': 'Restaurant not found'}), 404)
    db.session.delete(restaurant)
    db.session.commit()
    return make_response(jsonify({'message': 'Restaurant deleted'}), 204)

# Create a new RestaurantPizza entry
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()

    # Validate incoming data
    if not data or 'price' not in data or 'pizza_id' not in data or 'restaurant_id' not in data:
        return jsonify({'errors': ['Missing fields in request.']}), 400

    # Check if the pizza and restaurant exist
    pizza = Pizza.query.get(data['pizza_id'])
    restaurant = Restaurant.query.get(data['restaurant_id'])

    if pizza is None:
        return jsonify({'errors': ['Pizza not found.']}), 404
    if restaurant is None:
        return jsonify({'errors': ['Restaurant not found.']}), 404

    try:
        new_restaurant_pizza = RestaurantPizza(
            price=data['price'],
            pizza_id=data['pizza_id'],
            restaurant_id=data['restaurant_id']
        )
        db.session.add(new_restaurant_pizza)
        db.session.commit()
        return jsonify(new_restaurant_pizza.to_dict()), 201 

    except ValueError as e:
        db.session.rollback() 
        logger.error(f"ValueError: {str(e)}")
        return jsonify({'errors': [str(e)]}), 400
    except Exception as e:
        db.session.rollback() 
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'errors': ['An unexpected error occurred.']}), 500

if __name__ == '__main__':
    app.run(port=5555, debug=True)
