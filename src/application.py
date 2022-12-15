#!flask/bin/python
import json
from flask import Flask, Response, render_template
import optparse
import boto3
from boto3.dynamodb.conditions import Key

application = Flask(__name__)

# class Item(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(length=30), nullable=False, unique=True)
#     price = db.Column(db.Integer(), nullable=False)
#     barcode = db.Column(db.String(length=12), nullable=False, unique=True)
#     description = db.Column(db.String(length=1024), nullable=False, unique=True)

#     def __repr__(self):
#         return f'Item {self.name}'

def get_products_from_dynamodb():
    dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
    table = dynamodb.Table('w10group1products-test')
    data = table.scan()
    items = data['Items']
    return items

def subtract_products_from_dynamodb(ProdCat,ProdName):
    dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
    table = dynamodb.Table('w10group1products-test')
    product_info = table.query(KeyConditionExpression=Key('ProdCat').eq(ProdCat) & Key('ProdName').eq(ProdName))
    data = product_info['Items']
    newstock = int(data[0]['ProdStock'])-1
    table.update_item(
        Key={'ProdCat': ProdCat,'ProdName': ProdName},
        UpdateExpression="SET ProdStock= :s",
        ExpressionAttributeValues={':s':newstock},
    )
    return str(newstock)


@application.route('/')
@application.route('/home')
def home_page():
    return render_template('home.html')

@application.route('/market')
def market_page():
    items = get_products_from_dynamodb()
    return render_template('market.html', items=items)

@application.route('/market/purchase/<ProdCat>/<ProdName>')
def purchase_page(ProdCat,ProdName):
    data = subtract_products_from_dynamodb(ProdCat,ProdName)
    return f"Thank you for your purchase of {ProdName}, items remaining in stock = {data}"


if __name__ == '__main__':
    default_port = "80"
    default_host = "0.0.0.0"
    parser = optparse.OptionParser()
    parser.add_option("-H", "--host",
                      help=f"Hostname of Flask app {default_host}.",
                      default=default_host)

    parser.add_option("-P", "--port",
                      help=f"Port for Flask app {default_port}.",
                      default=default_port)

    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug",
                      help=optparse.SUPPRESS_HELP)

    options, _ = parser.parse_args()

    application.run(
        debug=options.debug,
        host=options.host,
        port=int(options.port)
    )
