"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from sqlalchemy import select
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Vehicle

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

def get_current_user() -> User:
    user = db.session.get(User, 1)
    if not user:
        raise APIException("No user with id=1. Please create one in the Flask Admin first", status_code=400)
    return user

def obj_or_404(model, obj_id: int):
    obj = db.session.get(model, obj_id)
    if not obj:
        raise APIException(f"{model.__name__} {obj_id} not found", status_code=404)
    return obj

# generate sitemap with all your endpoints
@app.route('/', methods=["GET"])
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# Endpoints for people and planets
@app.route("/people", methods=["GET"])
def list_people():
    chars = db.session.scalars(select(Character)).all()
    return jsonify([c.serialize() for c in chars]), 200

@app.route("/people/<int:people_id>", methods=["GET"])
def get_person(people_id: int):
    c = obj_or_404(Character, people_id)
    return jsonify(c.serialize()), 200

@app.route("/planets", methods=["GET"])
def list_planets():
    planets = db.session.scalars(select(Planet)).all()
    return jsonify([p.serialize()for p in planets]), 200

@app.route("/planets/<int:planet_id>", methods=["GET"])
def get_planet(planet_id: int):
    p = obj_or_404(Planet, planet_id)
    return jsonify(p.serialize()), 200

# Endpoints for Users and Favorites
@app.route("/users", methods=["GET"])
def list_users():
    users = db.session.scalars(select(User)).all()
    return jsonify([u.serialize() for u in users]), 200

@app.route("/users/favorites", methods=["GET"])
def get_my_favorites():
    user = get_current_user()
    data = {
        "user_id": user.id,
        "characters": [c.serialize() for c in user.favorite_characters],
        "planets": [p.serialize() for p in user.favorite_planets],
        "vehicles": [v.serialize() for v in user.favorite_vehicles],
    }
    return jsonify(data), 200


@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_fav_planet(planet_id: int):
    user = get_current_user()
    planet = obj_or_404(Planet, planet_id)
    if planet in user.favorite_planets:
        return jsonify({"msg": "Already in favorites"}), 200
    user.favorite_planets.append(planet)
    db.session.commit()
    return jsonify({"msg": "Planet added to favorites", "planet_id": planet.id}), 201

@app.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_fav_person(people_id: int):
    user = get_current_user()
    person = obj_or_404(Character, people_id)
    if person in user.favorite_characters:
        return jsonify({"msg": "Already in favorites"}), 200
    user.favorite_characters.append(person)
    db.session.commit()
    return jsonify({"msg": "Character added to favorites", "people_id": person.id}), 201

@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def del_fav_planet(planet_id: int):
    user = get_current_user()
    planet = obj_or_404(Planet, planet_id)
    if planet not in user.favorite_planets:
        raise APIException("Favorite not found for this user", status_code=404)
    user.favorite_planets.remove(planet)
    db.session.commit()
    return jsonify({"msg": "Planet removed from favorites", "planet_id": planet.id}), 200

@app.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def del_fav_person(people_id: int):
    user = get_current_user()
    person = obj_or_404(Character, people_id)
    if person not in user.favorite_characters:
        raise APIException("Favorite not found for this user", status_code=404)
    user.favorite_characters.remove(person)
    db.session.commit()
    return jsonify({"msg": "Character removed from favorites", "people_id": person.id}), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
