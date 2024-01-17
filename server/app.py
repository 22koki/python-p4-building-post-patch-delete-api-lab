#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(jsonify(bakeries), 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()

    if bakery is None:
        return make_response(jsonify({'message': 'Bakery not found'}), 404)

    bakery_serialized = bakery.to_dict()
    return make_response(jsonify(bakery_serialized), 200)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response(jsonify(baked_goods_by_price_serialized), 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()

    if most_expensive is None:
        return make_response(jsonify({'message': 'No baked goods found'}), 404)

    most_expensive_serialized = most_expensive.to_dict()
    return make_response(jsonify(most_expensive_serialized), 200)

# Placeholder for POST route to create a new baked good
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form

    # Extract data from the form
    name = data.get('name')
    price = data.get('price')
    bakery_id = data.get('bakery_id')

    # Validate the data (add your validation logic)

    # Create a new baked good
    baked_good = BakedGood(name=name, price=price, bakery_id=bakery_id)

    # Add to the database and commit the changes
    db.session.add(baked_good)
    db.session.commit()

    return make_response(jsonify({'message': 'Baked good created successfully'}), 201)

# Placeholder for PATCH route to update bakery name
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get(id)

    if bakery:
        data = request.form

        # Update bakery attributes based on the form data
        bakery.name = data.get('name', bakery.name)

        # Validate the data if needed

        # Commit the changes to the database
        db.session.commit()

        return make_response(jsonify(bakery.to_dict()), 200)
    else:
        return make_response(jsonify({'message': 'Bakery not found'}), 404)

# Placeholder for DELETE route to delete a baked good
# ...

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)

    if baked_good:
        db.session.delete(baked_good)
        db.session.commit()

        return make_response(jsonify({'message': 'Baked good deleted successfully'}), 200)
    else:
        return make_response(jsonify({'message': 'Baked good not found'}), 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
