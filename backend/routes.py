"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from backend.models import db, User, Photo, Favorite, People, Planet

api = Blueprint('api', __name__, url_prefix="/api")

# Allow CORS requests to this API
CORS(api)

@api.route("/users", methods=["POST"])
def create_user():
    """
    Create a new user.
    Body:
    {
        "username": "sombra",
        "password": "littleblueparrot"
    }
    """
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify(message="Username and password are required"), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify(message="Username already exists"), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(message="User created successfully", user=new_user.serialize()), 201

@api.route("/users", methods=["GET"])
def get_users():
    """
    Get all users.
    """
    users = User.query.all()
    return jsonify(users=[user.serialize() for user in users])

@api.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """
    Get a single user by user_id.
    """
    user = User.query.get(user_id)
    if user:
        return jsonify(user.serialize())
    return jsonify(message="User not found"), 404

@api.route("/users/<string:username>", methods=["GET"])
def get_user_by_username(username):
    """
    Get a single user by username.
    """
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify(user.serialize())
    return jsonify(message="User not found"), 404

@api.route("/photos", methods=["POST"])
def create_photo():
    """
    Create a new photo.
    Body:
    {
        "url": "https://wob.site/photo.jpg",
        "user_id": 1
    }
    """
    data = request.json
    url = data.get("url")
    user_id = data.get("user_id")

    if not url or not user_id:
        return jsonify(message="URL and user_id are required"), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify(message="User not found"), 404

    new_photo = Photo(url=url, user_id=user_id)
    db.session.add(new_photo)
    db.session.commit()

    return jsonify(message="Photo created successfully", photo=new_photo.serialize()), 201

@api.route("/photos", methods=["GET"])
def get_photos():
    """
    Get all photos.
    """
    photos = Photo.query.all()
    return jsonify(photos=[photo.serialize(include_user=True) for photo in photos])

@api.route("/photos/<int:photo_id>", methods=["GET"])
def get_photo(photo_id):
    """
    Get a single photo by photo_id.
    """
    photo = Photo.query.get(photo_id)
    if photo:
        return jsonify(photo.serialize(include_user=True))
    return jsonify(message="Photo not found"), 404

@api.route("/photos/<int:photo_id>", methods=["PUT"])
def update_photo(photo_id):
    """
    Update a photo by photo_id.
    Body:
    {
        "url": "https://wob.site/photo.jpg"
    }
    """
    data = request.json
    new_url = data.get("url")

    photo = Photo.query.get(photo_id)
    if not photo:
        return jsonify(message="Photo not found"), 404

    if new_url:
        photo.url = new_url

    db.session.commit()

    return jsonify(message="Photo updated successfully", photo=photo.serialize())

@api.route("/photos/<int:photo_id>", methods=["DELETE"])
def delete_photo(photo_id):
    """
    Delete a photo by photo_id.
    """
    photo = Photo.query.get(photo_id)
    if not photo:
        return jsonify(message="Photo not found"), 404

    db.session.delete(photo)
    db.session.commit()

    return jsonify(message="Photo deleted successfully"), 204

@api.route("/users/favorites", methods=["GET"])
def get_user_favorites():
    """
    Get all favorites for the current user.
    """
    # For now, assume a single user scenario, replace with authentication logic
    user_id = 1  # Replace with authenticated user's ID
    user = User.query.get(user_id)
    if not user:
        return jsonify(message="User not found"), 404

    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify(favorites=[fav.serialize() for fav in favorites])

@api.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_favorite_people(people_id):
    """
    Add a new favorite people to the current user with people_id.
    """
    # For now, assume a single user scenario, replace with authentication logic
    user_id = 1  # Replace with authenticated user's ID
    user = User.query.get(user_id)
    if not user:
        return jsonify(message="User not found"), 404

    # Check if the people exists
    people = People.query.get(people_id)
    if not people:
        return jsonify(message="People not found"), 404

    # Check if already favorite
    existing_favorite = Favorite.query.filter_by(
        user_id=user_id, favorite_type='people', favorite_id=people_id
    ).first()
    if existing_favorite:
        return jsonify(message="People already favorited"), 400

    favorite = Favorite(user_id=user_id, favorite_type='people', favorite_id=people_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify(message="People added to favorites successfully", favorite=favorite.serialize()), 201

@api.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_favorite_people(people_id):
    """
    Delete a favorite people with people_id.
    """
    # For now, assume a single user scenario, replace with authentication logic
    user_id = 1  # Replace with authenticated user's ID
    user = User.query.get(user_id)
    if not user:
        return jsonify(message="User not found"), 404

    # Check if the favorite exists
    favorite = Favorite.query.filter_by(
        user_id=user_id, favorite_type='people', favorite_id=people_id
    ).first()
    if not favorite:
        return jsonify(message="Favorite people not found"), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify(message="Favorite people deleted successfully"), 204

@api.route("/favorite/planets/<int:planet_id>", methods=["POST"])
def add_favorite_planet(planet_id):
    """
    Add a new favorite planet to the current user with planet_id.
    """
    # For now, assume a single user scenario, replace with authentication logic
    user_id = 1  # Replace with authenticated user's ID
    user = User.query.get(user_id)
    if not user:
        return jsonify(message="User not found"), 404

    # Check if the planet exists
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify(message="Planet not found"), 404

    # Check if already favorite
    existing_favorite = Favorite.query.filter_by(
        user_id=user_id, favorite_type='planet', favorite_id=planet_id
    ).first()
    if existing_favorite:
        return jsonify(message="Planet already favorited"), 400

    favorite = Favorite(user_id=user_id, favorite_type='planet', favorite_id=planet_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify(message="Planet added to favorites successfully", favorite=favorite.serialize()), 201

@api.route("/favorite/planets/<int:planet_id>", methods=["DELETE"])
def delete_favorite_planet(planet_id):
    """
    Delete a favorite planet with planet_id.
    """
    # For now, assume a single user scenario, replace with authentication logic
    user_id = 1  # Replace with authenticated user's ID
    user = User.query.get(user_id)
    if not user:
        return jsonify(message="User not found"), 404

    # Check if the favorite exists
    favorite = Favorite.query.filter_by(
        user_id=user_id, favorite_type='planet', favorite_id=planet_id
    ).first()
    if not favorite:
        return jsonify(message="Favorite planet not found"), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify(message="Favorite planet deleted successfully"), 204

@api.route("/people", methods=["GET"])
def get_people():
    """
    Get a list of all people.
    """
    people = People.query.all()
    return jsonify(people=[person.serialize() for person in people])

@api.route("/people/<int:people_id>", methods=["GET"])
def get_person(people_id):
    """
    Get information about a single person by people_id.
    """
    person = People.query.get(people_id)
    if person:
        return jsonify(person.serialize())
    return jsonify(message="Person not found"), 404

@api.route("/planets", methods=["GET"])
def get_planets():
    """
    Get a list of all planets.
    """
    planets = Planet.query.all()
    return jsonify(planets=[planet.serialize() for planet in planets])

@api.route("/planets/<int:planet_id>", methods=["GET"])
def get_planet(planet_id):
    """
    Get information about a single planet by planet_id.
    """
    planet = Planet.query.get(planet_id)
    if planet:
        return jsonify(planet.serialize())
    return jsonify(message="Planet not found"), 404

# Add routes for managing planets
@api.route("/planets", methods=["POST"])
def create_planet():
    """
    Create a new planet.
    Body:
    {
        "name": "Tatooine",
        "diameter": "10465",
        "climate": "Arid",
        "gravity": "1 standard",
        "terrain": "Desert",
        "population": "200000"
    }
    """
    data = request.json
    name = data.get("name")
    diameter = data.get("diameter")
    climate = data.get("climate")
    gravity = data.get("gravity")
    terrain = data.get("terrain")
    population = data.get("population")

    if not name or not diameter or not climate or not gravity or not terrain or not population:
        return jsonify(message="All fields (name, diameter, climate, gravity, terrain, population) are required"), 400

    new_planet = Planet(name=name, diameter=diameter, climate=climate, gravity=gravity, terrain=terrain, population=population)
    db.session.add(new_planet)
    db.session.commit()

    return jsonify(message="Planet created successfully", planet=new_planet.serialize()), 201

@api.route("/planets/<int:planet_id>", methods=["PUT"])
def update_planet(planet_id):
    """
    Update a planet by planet_id.
    Body:
    {
        "name": "Tatooine",
        "diameter": "10465",
        "climate": "Arid",
        "gravity": "1 standard",
        "terrain": "Desert",
        "population": "200000"
    }
    """
    data = request.json

    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify(message="Planet not found"), 404

    planet.name = data.get("name", planet.name)
    planet.diameter = data.get("diameter", planet.diameter)
    planet.climate = data.get("climate", planet.climate)
    planet.gravity = data.get("gravity", planet.gravity)
    planet.terrain = data.get("terrain", planet.terrain)
    planet.population = data.get("population", planet.population)

    db.session.commit()

    return jsonify(message="Planet updated successfully", planet=planet.serialize())

@api.route("/planets/<int:planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    """
    Delete a planet by planet_id.
    """
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify(message="Planet not found"), 404

    db.session.delete(planet)
    db.session.commit()

    return jsonify(message="Planet deleted successfully"), 204

# Add routes for managing people
@api.route("/people", methods=["POST"])
def create_person():
    """
    Create a new person.
    Body:
    {
        "name": "Luke Skywalker",
        "height": "172",
        "mass": "77",
        "hair_color": "blond",
        "skin_color": "fair",
        "eye_color": "blue",
        "birth_year": "19BBY",
        "gender": "male"
    }
    """
    data = request.json
    name = data.get("name")
    height = data.get("height")
    mass = data.get("mass")
    hair_color = data.get("hair_color")
    skin_color = data.get("skin_color")
    eye_color = data.get("eye_color")
    birth_year = data.get("birth_year")
    gender = data.get("gender")

    if not name or not height or not mass or not hair_color or not skin_color or not eye_color or not birth_year or not gender:
        return jsonify(message="All fields (name, height, mass, hair_color, skin_color, eye_color, birth_year, gender) are required"), 400

    new_person = People(name=name, height=height, mass=mass, hair_color=hair_color, skin_color=skin_color, eye_color=eye_color, birth_year=birth_year, gender=gender)
    db.session.add(new_person)
    db.session.commit()

    return jsonify(message="Person created successfully", person=new_person.serialize()), 201

@api.route("/people/<int:people_id>", methods=["PUT"])
def update_person(people_id):
    """
    Update a person by people_id.
    Body:
    {
        "name": "Luke Skywalker",
        "height": "172",
        "mass": "77",
        "hair_color": "blond",
        "skin_color": "fair",
        "eye_color": "blue",
        "birth_year": "19BBY",
        "gender": "male"
    }
    """
    data = request.json

    person = People.query.get(people_id)
    if not person:
        return jsonify(message="Person not found"), 404

    person.name = data.get("name", person.name)
    person.height = data.get("height", person.height)
    person.mass = data.get("mass", person.mass)
    person.hair_color = data.get("hair_color", person.hair_color)
    person.skin_color = data.get("skin_color", person.skin_color)
    person.eye_color = data.get("eye_color", person.eye_color)
    person.birth_year = data.get("birth_year", person.birth_year)
    person.gender = data.get("gender", person.gender)

    db.session.commit()

    return jsonify(message="Person updated successfully", person=person.serialize())

@api.route("/people/<int:people_id>", methods=["DELETE"])
def delete_person(people_id):
    """
    Delete a person by people_id.
    """
    person = People.query.get(people_id)
    if not person:
        return jsonify(message="Person not found"), 404

    db.session.delete(person)
    db.session.commit()

    return jsonify(message="Person deleted successfully"), 204