from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import Config
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database and marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))

# Schemas
class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

class ItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        load_instance = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token)
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/items', methods=['GET'])
@jwt_required()
def get_items():
    items = Item.query.all()
    return items_schema.jsonify(items)

@app.route('/items', methods=['POST'])
@jwt_required()
def create_item():
    data = request.get_json()
    new_item = Item(name=data['name'], description=data['description'])
    db.session.add(new_item)
    db.session.commit()
    return item_schema.jsonify(new_item), 201

@app.route('/items/<int:item_id>', methods=['GET'])
@jwt_required()
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return item_schema.jsonify(item)

@app.route('/items/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.get_json()
    item.name = data['name']
    item.description = data['description']
    db.session.commit()
    return item_schema.jsonify(item)

@app.route('/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted"})

# Run server
if __name__ == '__main__':
    app.run(debug=True)
