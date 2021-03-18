import json
from flask import Flask, request, render_template
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.exc import IntegrityError
from datetime import timedelta 
from models import db, User, Pokemon, MyPokemon
''' Begin boilerplate code '''
def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SECRET_KEY'] = "MYSECRET"
  app.config['JWT_EXPIRATION_DELTA'] = timedelta(days = 7) 
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()

''' End Boilerplate Code '''

''' Set up JWT here '''
def authenticate(uname, pw):
  user = User.query.filter_by(username=uname).first()
  if user and user.check_password(pw):
    return user

def identity(payload):
  return User.query.get(payload["identity"])

jwt = JWT(app, authenticate, identity)
''' End JWT Setup '''

# edit to query 50 pokemon objects and send to template
@app.route('/')
def index():
  pokemon_objects = Pokemon.query.limit(50).all()
  return render_template('index.html', pokemon_objects = pokemon_objects)

@app.route('/app')
def client_app():
  return app.send_static_file('app.html')

@app.route("/signup", methods=["POST"])
def signup():
  userdata = request.get_json()
  print(userdata)
  new_u = User(username = userdata["username"], email=userdata["email"])
  new_u.set_password(userdata["password"])
  try:
    db.session.add(new_u)
    db.session.commit()
  except IntegrityError:
    db.session.rollback()
    return "username or email already exists"
  return "user created"

@app.route("/pokemon", methods=["GET"])
def get_pokemons():
  pokemons = Pokemon.query.all()
  pokemons_dict = [poke.toDict() for poke in pokemons]
  return json.dumps(pokemons_dict)

@app.route('/mypokemon', methods=['POST'])
@jwt_required()
def create_pokemon():
  pokemon_data = request.get_json()
  pokemon = MyPokemon(pid=pokemon_data["pid"], name=pokemon_data["name"], id=current_identity.id)
  db.session.add(pokemon)
  db.session.commit()
  return "Pokemon created", 201

@app.route('/mypokemon/<id>', methods=['GET'])
@jwt_required()
def get_my_pokemon(id):
  id = int(id)
  pokemons = MyPokemon.query.filter_by(id=current_identity.id).all()
  if pokemons == None:
    return 'Invalid id or unauthorized'
  if len(pokemons) == 0:
    return 'No Pokemon captured!'
  pokemon_dict = pokemons[id-1].toDict()
  return json.dumps(pokemon_dict)

@app.route('/mypokemon', methods=['GET'])
@jwt_required()
def list_my_pokemons():
  pokemons = MyPokemon.query.filter_by(id=current_identity.id).all()
  if pokemons == None:
    return 'Invalid id or unauthorized'
  if len(pokemons) == 0:
    return 'No Pokemon captured!'
  pokemons_dict = [poke.toDict() for poke in pokemons]
  return json.dumps(pokemons_dict)

@app.route('/mypokemon/<id>', methods=['PUT'])
@jwt_required()
def update_pokemon(id):
  id = int(id)
  pokemon_data = request.get_json()
  pokemons = MyPokemon.query.filter_by(id = current_identity.id).all()
  if pokemons == None:
    return 'Invalid id or unauthorized'
  if len(pokemons) == 0:
    return 'No Pokemon captured!'
  pokemon = pokemons[id-1]
  if "name" in pokemon_data:
    pokemon.name = pokemon_data["name"]
    db.session.add(pokemon)
    db.session.commit()
    return "Updated", 201

@app.route('/mypokemon/<id>', methods=["DELETE"])
@jwt_required()
def delete_pokemon(id):
  id = int(id)
  pokemons = MyPokemon.query.filter_by(id=current_identity.id).all()
  if pokemons == None:
    return 'Invalid id or unauthorized'
  if len(pokemons) == 0:
    return 'No Pokemon captured!'
  pokemon = pokemons[id-1]
  if pokemon:
    db.session.delete(pokemon)
    db.session.commit()
    return "Pokemon deleted", 204
  return "Pokemon not found", 404 


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)