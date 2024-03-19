
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, Characters, Planets, FavoritePlanets, FavoriteCharacters      # aqui tambien agregaremos nuestros modelos 


# Instancia FLack
app = Flask(__name__)
app.url_map.strict_slashes = False
# configuracion de la base de datos
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


# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/hello', methods=['GET'])
def handle_hello():

    response_body = {"mesage": "Hello, this is your GET /hello response "}
    return jsonify(response_body), 200

@app.route('/users', methods=['GET', 'POST'])  # comenzamos con el endpoints
def handle_users():  #definimos nuestro enpoints
    response_body = results = {}
    #  comprehension esta implementacion
    if request.method == 'GET':
        try:
        # logica para consultar la base de dato y devolver todos los usuarios
            users = db.session.execute(db.select(Users)).scalars()  # de donde va a sacar el resultado
            response_body['results'] = [user.serialize() for user in users]  # el resultado que va a mostrar en forma de lista
            response_body['message'] = 'Success' 
            return jsonify(response_body), 200  # lo que exactamente nos mostrara
        except KeyError as e:
            response_body['message'] = f'Some Error {str(e)}'
            return jsonify(response_body), 400
    if request.method == 'POST':
        try:
            data = request.json # se pasan los datos del usuario desde la solicitud
            user = Users(email = data['email'], # los datos con los cual se crearan el usuario
                     password = data['password'],
                     is_active = True)
            db.session.add(user) # para añadir a la session
            db.session.commit() # para confirmar el añadir al usuario
            response_body['results'] = user.seralize() 
            response_body['message'] = 'User Created'
            return jsonify(response_body), 201 # 201 (creado)
        except KeyError as e:
            response_body['message'] = f'Some Error {str(e)}'
            return jsonify(response_body), 400


@app.route('/users/<int:user_id>/favorite', methods=['GET'])
def list_favorite(user_id):
    response_body = {}
    if request.method == 'GET':
        try:
            favorite_planets = db.session.query(FavoritePlanets).join(Users).filter(Users.id == user_id).all()
            favorite_characters = db.session.query(FavoriteCharacters).join(Users).filter(Users.id == user_id).all()
            response_body= {
                            "personajes": [favorite.serialize() for favorite in favorite_characters],
                            "planetas": [favorite.serialize() for favorite in favorite_planets]
                           }
            response_body['message'] = 'Success'
            return jsonify(response_body), 200
        except KeyError as e:
            response_body['message'] = f'Some Error {str(e)}'
            return jsonify(response_body), 400


@app.route('/characters', methods=['GET'])
def list_characters():
    response_body = results = {}
    if request.method == 'GET':
        try:
            characters = db.session.execute(db.select(Characters)).scalars()
            response_body['results'] = [character.serialize() for character in characters]
            response_body['message'] = 'Success'
            return jsonify(response_body), 200
        except KeyError as e:
            response_body['message'] = f'Some Error {str(e)}'
            return jsonify(response_body), 400

 
@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    if request.method == 'GET':
        try:
            # Buscar el personaje por su ID en la base de datos
            character = db.session.get(Characters, character_id)
            
            # Si el personaje no existe, retornar un mensaje de error con el código de estado 404
            if not character:
                return jsonify({"message": "Character not found"}), 404
            
            # Serializar el personaje a un formato JSON
            response_body = {
                "id": character.id,
                "name": character.name,}
                # Agregar más campos si es necesario
            # Retornar el personaje serializado en formato JSON
            return jsonify(response_body), 200
        except Exception as e:
            # En caso de cualquier error, retornar un mensaje de error con el código de estado 500
            return jsonify({"message": str(e)}), 500 # esta linea tuve que buscar si no, el codigo no me iba


@app.route('/planets', methods=['GET'])
def list_planets():
    response_body = results = {}
    if request.method == 'GET':
        try:
            planets = db.session.execute(db.select(Planets)).scalars()
            response_body['results'] = [planet.serialize() for planet in planets]
            response_body['message'] = 'Success'
            return jsonify(response_body), 200
        except KeyError as e:
            response_body['message'] = f'Some Error {str(e)}'
            return jsonify(response_body), 400


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    if request.method == 'GET':
        try:
            planet = db.session.get(Planets, planet_id)
            if not planet:
                return jsonify({"message": "Planet not found"}), 404
            response_body = {
                "id": planet.id,
                "name": planet.name,}
            return jsonify(response_body), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 500


@app.route('/favorite/<int:user_id>/planets', methods=['POST'])
def add_favorite_planets(user_id):
    response_body = {}
    data = request.json
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    planet_id = data.get("planet_id") # data, porque es el dato que enviamos
    planet = Planets.query.get(planet_id) # aqui lo buscaamos
    if not planet:
        return jsonify({"message": "Planet not found"}), 404
    # Crear una nueva instancia de FavoritePlanets
    favorite = FavoritePlanets(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    response_body['message'] = "success"
    response_body['favorite'] = favorite.serialize()
    return jsonify(response_body), 201


@app.route('/favorite/<int:user_id>/characters', methods=['POST'])
def add_favorite_characters(user_id):
    response_body = {}
    data = request.json
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    character_id = data.get("character_id") 
    character = Characters.query.get(character_id) 
    if not character:
        return jsonify({"message": "Character not found"}), 404
    favorite = FavoriteCharacters(user_id=user_id, character_id=character_id)
    db.session.add(favorite)
    db.session.commit()
    response_body['message'] = "success"
    response_body['favorite'] = favorite.serialize()
    return jsonify(response_body), 201


@app.route('/favorite/<int:user_id>/planets/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    response_body = {}
        # Verifica  si el usuario existe
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    favorite_planet = FavoritePlanets.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite_planet:
        return jsonify({"message": "Favorite planet not found"}), 404
    db.session.delete(favorite_planet)
    db.session.commit()
    response_body['message'] = 'deleted successfully'
    return jsonify(response_body), 200


@app.route('/favorite/<int:user_id>/characters/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(user_id, character_id):
    response_body = {}
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    favorite_character = FavoriteCharacters.query.filter_by(user_id=user_id, character_id=character_id).first()
    if not favorite_character:
        return jsonify({"message": "Favorite character not found"}), 404
    db.session.delete(favorite_character)
    db.session.commit()
    response_body['message'] = 'deleted successfully'
    return jsonify(response_body), 200   

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
