from flask import Flask, render_template, jsonify, request, Blueprint, send_from_directory
import json
import configparse
import sqlite3 as sql
import requests
import argparse
import logging
import os
import time
import db_logger
import pandas as pd
from threading import Lock

# Create blueprint for routes
catalog_router = Blueprint('catalog_router', __name__, template_folder='templates')
lock = Lock()


# Make db connection

def db(database_name='database.db'):
    return sql.connect(database=database_name)


# Function to get records according to the arguments
# IF one is True then returns a single record
def query_db(query, args=(), one=False):
    cur = db(db_path).cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
              for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r


# Home Page for catalog server
@catalog_router.route("/", methods=['GET', 'POST', 'PUT'])
def home():
    return render_template('index.html')


# End point for getting the entire list of books present
@catalog_router.route('/list', methods=['GET'])
def list():
    print("Received list request")
    my_query = query_db("select * from books_1")
    log = 'list method: The list of items currently present is has ' + str(my_query) + ' items'
    logging.info(log)
    return json.dumps(my_query)


# End point for getting the books with the given topic, takes get request and topic in URL
@catalog_router.route('/search/<topic>', methods=['GET'])
def search(topic):
    print("Received search request for topic:", topic)
    log = 'search method: called for topic ' + str(topic)
    logging.info(log)
    my_query = query_db('select item_number, title from books_1 where topic = ?', [topic])
    log = 'search method: has items ' + str(my_query)
    logging.info(log)
    return json.dumps(my_query)


# End point for getting the books with the given topic, takes post request and topic in json
@catalog_router.route('/search/', methods=['POST'])
def search_with_json_request():
    req_data = request.get_json()
    topic = req_data['topic']
    return search(topic)


# End point for getting the name of book with the id, takes get request and item_number in URL
@catalog_router.route('/get_name/<item_number>', methods=['GET'])
def get_name(item_number):
    log = 'get name method: called for item_number ' + str(item_number)
    logging.debug(log)
    my_query = query_db('select title from books_1 where item_number = ?', [item_number], one=True)
    log = 'get_name method: returns ' + str(my_query)
    logging.debug(log)
    return json.dumps(my_query)


# End point for getting the details of book with item_number, takes get request and item_number in URL
@catalog_router.route('/lookup/<item_number>', methods=['GET'])
def lookup(item_number):
    print("Received lookup request for item :", item_number)
    log = 'lookup method: called for item_number ' + str(item_number)
    logging.debug(log)
    my_query = query_db('select title, cost, quantity from books_1 where item_number = ?', [item_number], one=True)
    log = 'lookup method: returns ' + str(my_query)
    logging.debug(log)
    return json.dumps(my_query)


# End point for getting the details of book with item_number, takes post request and item_number in json
@catalog_router.route('/lookup/', methods=['POST'])
def lookup_with_json_request():
    req_data = request.get_json()
    item_number = req_data['item_number']
    return lookup(item_number)


# End point for getting the quantity of book with item_number, takes get request and item_number in URL
@catalog_router.route('/get_quantity/<item_number>', methods=['GET'])
def get_quantity(item_number):
    print("Received get quantity for item :", item_number)
    log = 'get_quantity method: called for item ' + str(item_number)
    logging.debug(log)
    my_query = query_db('select quantity from books_1 where item_number = ?', [item_number], one=True)
    log = 'get_quantity method: result ' + str(my_query)
    logging.debug(log)
    return json.dumps(my_query)


# End point for getting the quantity of book with item_number, takes post request and item_number in json
@catalog_router.route('/get_quantity/', methods=['POST'])
def get_quantity_with_json_request():
    req_data = request.get_json()
    item_number = req_data['item_number']
    return get_quantity(item_number)


# End point for updating the quantity of book with item_number, takes get request and item_number and quantity in URL
@catalog_router.route('/update_q/<item_number>/<quantity>')
def update_q(quantity, item_number):
    log = 'update method: called for item ' + str(item_number) + ' update by ' + str(quantity)
    logging.debug(log)
    print(log)
    quant = json.loads(get_quantity(item_number))
    # print(quantity[0])
    quant = int(quant['quantity']) + int(quantity)
    try:
        lock.acquire()
        with sql.connect(db_path) as con:
            res = requests.get('http://' + frontend_ip + ':' + frontend_port + '/invalidate/' + item_number).content
            query = "UPDATE books_1 SET quantity = ? WHERE item_number = ?"
            cur = con.cursor()
            cur.execute(query, (quant, item_number))
            con.commit()

            # Log the updates in the dblogger file for consistency and fault tolerance
            db_logger.db_log(query, "quantity", item_number, quant, i)

            msg = "Quantity of record " + str(item_number) + " successfully changed by " + str(quantity)
    #
    except:
        con.rollback()
        msg = "error in update operation"

    finally:
        log = 'update_q method: ' + msg
        logging.debug(log)
        con.close()
        lock.release()
    return json.dumps(msg)


# End point for updating the quantity of book with item_number, takes post request and item number and quantity in json
@catalog_router.route('/update_q/', methods=['POST'])
def update_q_with_json_request():
    req_data = request.get_json()
    item_number = req_data['item_number']
    quantity = req_data['quantity']
    return update_q(quantity, item_number)


# End point for updating the cost of book with item_number, takes get request and item number and cost in URL
@catalog_router.route('/update_c/<item_number>/<cost>')
def update_c(cost, item_number):
    log = 'update_c method: item ' + str(item_number) + ' cost to be updated ' + str(cost)

    logging.debug(log)
    msg = ''
    try:
        lock.acquire()
        with sql.connect(db_path) as con:
            res = requests.get('http://' + frontend_ip + ':' + frontend_port + '/invalidate/' + item_number).content
            query = "UPDATE books_1 SET cost = ? WHERE item_number = ?"
            cur = con.cursor()
            cur.execute(query, (cost, item_number))
            con.commit()
            # Log the updates in the dblogger file for consistency and fault tolerance

            db_logger.db_log(query, "cost", item_number, cost, i)
            msg = "Cost of item :" + str(item_number) + " successfully updated to:" + str(cost)

    except:
        con.rollback()
        msg = "error in update operation"

    finally:
        log = 'update_c method: ' + msg
        logging.debug(log)
        con.close()
        lock.release()
    return json.dumps(msg)


# End point for updating the cost of book with item_number, takes post request and item_number and cost in json
@catalog_router.route('/update_c/')
def update_c_with_json_request():
    req_data = request.get_json()
    item_number = req_data['item_number']
    cost = req_data['cost']
    return update_c(cost, item_number)


# End point for getting the database updates log file
@catalog_router.route("/files/")
def get_file():
    """Download a file."""
    return send_from_directory(BASE_DIR, filename, as_attachment=True)


# read config file
order_ip1, order_port1, order_ip2, order_port2, catalog_ip1, catalog_port1, catalog_ip2, catalog_port2, frontend_ip, frontend_port, i, restart = configparse.parse()
# db name
database_name = 'database' + str(i) + '.db'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, database_name)
# db update logger file
filename = 'db_logcatalog' + str(i) + '.csv'
