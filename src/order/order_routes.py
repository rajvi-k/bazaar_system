from flask import Flask, render_template, jsonify, request, Blueprint
import json
import configparse
import sqlite3 as sql
import requests
import argparse
import logging
import os
import random

# Create blueprint for routes
order_router = Blueprint('order_router', __name__, template_folder='templates')


# Home page for the order server
@order_router.route("/", methods=['GET', 'POST', 'PUT'])
def home():
    return render_template('index.html')


# End point to buy item with item_number using GET request with item number in URL
@order_router.route('/buy/<item_number>', methods=['GET'])
def buy(item_number):
    rep = random.randint(1, 2)
    log = 'buy method: buy request received for item' + str(item_number)
    logging.debug(log)
    print("Received buy request for item ", item_number)

    # Querying the catalog server for getting the quantity of item
    quantity = requests.get('http://' + catalog_ip + ':' + catalog_port + '/get_quantity/' + str(item_number)).content
    quantity = quantity.decode("utf-8")
    quantity = json.loads(quantity)
    print("Received buy request for item ", item_number, " has quantity ", quantity)

    # Decrement the quantity
    quantity = int(quantity['quantity']) - 1
    log = 'buy method: quantity for item' + str(item_number) + ' is ' + str(quantity)
    logging.debug(log)

    err_response = "Item is unavailable."

    # IF item is not present then return unavailable message
    if int(quantity) < 0:
        log = 'buy method: ' + str(item_number) + ' ' + str(err_response)
        logging.debug(log)
        print(log)
        return json.dumps(err_response)
    else:
        print("quantity is", quantity, i)

        # for ip,port in zip(replica_ip,replica_port):
        # Buying the item and updating the quantity
        try:
            ip = replica_ip[0]
            port = replica_port[0]
            message = json.loads(requests.get(
                'http://' + str(ip) + ':' + str(port) + '/update_q/' + str(item_number) + '/' + str(-1)).content.decode(
                "utf-8"))
        except:
            print("catalog server 1 is down")

        try:
            ip = replica_ip[1]
            port = replica_port[1]
            message = json.loads(requests.get(
                'http://' + str(ip) + ':' + str(port) + '/update_q/' + str(item_number) + '/' + str(-1)).content.decode(
                "utf-8"))
        except:
            print("catalog server 2 is down")

        msg = "Record successfully bought"

        # Getting the name of the item
        item_name = json.loads(
            requests.get('http://' + replica_ip[int(i) - 1] + ':' + replica_port[int(i) - 1] + '/get_name/' + str(
                item_number)).content.decode(
                "utf-8"))
        log = 'buy method: Bought item ' + str(item_number) + str(item_name) + 'and the quantity becomes ' + str(
            quantity)
        print("Bought book ", str(item_name))
        logging.debug(log)
        return json.dumps(msg)


# End point for buy to take POST request with item_number in json
@order_router.route('/buy/', methods=['POST'])
def buy_with_json_request():
    req_data = request.get_json()
    item_number = req_data['item_number']
    return buy(item_number)


# read config file
order_ip1, order_port1, order_ip2, order_port2, catalog_ip1, catalog_port1, catalog_ip2, catalog_port2, frontend_ip, frontend_port, i = configparse.parse()
replica_ip = [catalog_ip1, catalog_ip2]

replica_port = [catalog_port1, catalog_port2]
print(replica_ip, replica_port, "rep______________________", i)
catalog_port = catalog_port1
catalog_ip = catalog_ip1
