from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from os import environ
import datetime

IMAGES_PATH = 'https://burgersandytchu.pythonanywhere.com/static/images/'
db_user = environ['DB_USER']
db_password = environ['DB_PASSWORD']

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@tai.db.elephantsql.com/cucyerdx'
db = SQLAlchemy(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    text = db.Column(db.String())
    image = db.Column(db.String())
    price = db.Column(db.Integer())
    baseprice = db.Column(db.Integer())
    grams = db.Column(db.Integer())
    extra = db.Column(db.String())

    def __init__(self, title, text, image, price, baseprice, grams, extra=''):
        self.title = title
        self.text = text
        self.image = image
        self.price = price
        self.baseprice = baseprice
        self.grams = grams
        self.extra = extra

    def __repr__(self):
        return f"<Product {self.title}>"


class Burgers:
    @staticmethod
    def get_burgers_list(extra=''):
        burgers_list = list()
        try:
            if extra != '':
                products = Product.query.filter(Product.extra.like(extra))
            else:
                products = Product.query.filter(Product.extra.is_(None))
            burgers_list.extend([
                {
                    'image': IMAGES_PATH + p.image,
                    'title': p.title,
                    'text': p.text,
                    'price': p.price,
                    'baseprice': p.baseprice,
                    'grams': p.grams,
                    'extra': p.extra
                } for p in products])
        except Exception as e:
            print(f"Query error ({datetime.datetime.now()}): {e}")
        return burgers_list


@app.route('/burgers-order', methods=['POST'])
@cross_origin()
def burgers_order():
    try:
        order = request.json["order"]
        name = request.json["name"]
        phone = request.json["phone"]
    except:
        return {"success": 0, "message": "Заполните все поля!!!"}
    else:
        return {"success": 1, "message": "Спасибо за заказ! Мы скоро свяжемся с вами!"}


@app.route('/burgers-data')
@cross_origin()
def burger_data():
    response = list()
    response.extend(Burgers.get_burgers_list())
    extra = request.args.get('extra', '')
    if extra != '':
        response.extend(Burgers.get_burgers_list(extra))
    return jsonify(response)


if __name__ == '__main__':
    app.run()
