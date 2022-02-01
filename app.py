from ast import dump
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import pyodbc
import urllib

#Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
#Database

#SQLite DB
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'db.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#SQL DB
params = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER=VASUSHARMA\SQLEXPRESS;DATABASE=Vasu_Db;Trusted_Connection=yes;')
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#Init db
db= SQLAlchemy(app)

#init MArshmallow
ma = Marshmallow(app)

#Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self,name,description,price,qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

#Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name','description','price','qty')

#Init Schema
product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(many=True, strict=True)
#product_schema = ProductSchema()

#Create a Product
@app.route('/product',methods = ['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name,description,price,qty)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)

#Get All products
@app.route('/product',methods =['GET'])
def get_products():
    all_products = Product.query.all()
    result = product_schema.dump(all_products)
    return jsonify(result.data)

#Get Single products
@app.route('/product/<id>',methods =['GET'])
def get_product(id):
    product = Product.query.get(id)
    result = product_schema.dump(product)
    return product_schema.jsonify(result)

#update a Product
@app.route('/product/<id>',methods = ['PUT'])
def update_product(id):
    product = Product.query.get(id)
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    product.name = name
    product.description = description
    product.price = price
    product.qty = qty
    db.session.commit()
    return product_schema.jsonify(product)

#Delete products
@app.route('/product/<id>',methods =['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    #result = product_schema.dump(all_products)
    return product_schema.jsonify(product)

#Run server
if __name__=='__main__':
    app.run(debug=True)
