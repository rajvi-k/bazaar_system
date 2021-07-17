from flask import Flask, render_template, jsonify, request, Blueprint
import json
import configparse
import functools
import sqlite3 as sql
import requests
import argparse
import logging
import cache
import os
import pickle
import time
from threading import Lock
import socket

# Active status of the servers
is_catalog_server_active = [False, False]
is_order_server_active = [False, False]

# locks to update shared variables
lock_catalog = Lock()
lock_order = Lock()
cache_lock = Lock()
delay = 1


# heartbeat connection with the catalog server
def heartbeat_catalog(ipPortList):
    global is_catalog_server_active
    while True:
        # print("heartbeat with catalog: ", ipPortList)
        for i, address in enumerate(ipPortList):
            port = int(address[1])
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((address[0], port))
                message = "Are you up"
                bytes_sent = s.send(pickle.dumps(message))
                data = s.recv(1024).decode("ascii")
                if not data:
                    raise Exception('Did not receive response')
                lock_catalog.acquire()
                is_catalog_server_active[i] = True
                lock_catalog.release()
                s.close()
                # print("catalog servers active:", is_catalog_server_active)
            except socket.error:
                print("Error in connection with ", i," catalog server")
                lock_catalog.acquire()
                is_catalog_server_active[i] = False
                lock_catalog.release()
                print("catalog servers active: ", is_catalog_server_active)
            finally:
                s.close()
        time.sleep(10)


# heartbeat connection with the order server
def heartbeat_order(ipPortList):
    global is_order_server_active
    while True:
        # print("heartbeat with order servers", ipPortList)
        for i, address in enumerate(ipPortList):
            port = int(address[1])
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((address[0], port))
                message = "Are you up"
                bytes_sent = s.send(pickle.dumps(message))
                data = s.recv(1024).decode("ascii")

                if not data:
                    raise Exception('Did not receive response')

                lock_order.acquire()
                is_order_server_active[i] = True
                # print("order servers active:", is_order_server_active)
                lock_order.release()
                s.close()
            except socket.error:
                print("Error in connection with ", i, "order server")

                lock_order.acquire()
                is_order_server_active[i] = False
                print("order servers active:", is_order_server_active)

                lock_order.release()
            finally:
                s.close()
        time.sleep(10)


# Create blueprint for routes
# all the routes are cached have a decorator function around all these functions which caches requests
# decorater function mentioned in cache.py file
router = Blueprint('router', __name__, template_folder='templates')
import pickle


# keeps trying till it gets reply from atleast one up server in while
# handled in progress requests also  in try catch
# load balancing is done by sending alternate requests to different instances

# Home page for the front end server
@router.route("/", methods=['GET', 'POST', 'PUT'])
def home():
    return render_template('index.html')


############################################################

# invalidate cache
@router.route('/invalidate/<item_number>', methods=['GET'])
def inval(item_number):
    print("Invalidate cache called for item number :", item_number)
    cache_lock.acquire()
    for cachefile in cach_list:
        if os.path.exists(cachefile) and os.path.getsize(cachefile) > 0:
            with open(cachefile, 'rb') as cachehandle:
                c = pickle.load(cachehandle)
                if item_number in c:
                    del c[item_number]
                    pickle.dump(c, open(cachefile, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
    cache_lock.release()

    if os.path.exists("list_cache.pkl"):
        os.remove("list_cache.pkl")
    return "Invalidated entry for item " + item_number


# Forwards the lookup and get requests to the catalog server

# End point for getting the entire list of books present
@router.route('/list')
@cache.cached("list_cache.pkl")
def list():
    global lst

    print(lst, is_catalog_server_active, "is catalog server")


    while True:
        try:
            lst += 1
            log = "list"
            # print("entered list fun ")
            if lst % 2 == 0 and is_catalog_server_active[0]:
                logging.debug(log)
                print("entered list fun active")
                res = requests.get('http://' + catalog_ip1 + ':' + catalog_port1 + '/list').content
                break
            elif is_catalog_server_active[1]:
                print("entered list fun active odd")
                res = requests.get('http://' + catalog_ip2 + ':' + catalog_port2 + '/list').content
                break
        except:
            print("Failed to send request as server is down")

    return res


# End point for getting the books with the given topic, takes get request and topic in URL
@router.route('/search/<topic>', methods=['GET'])
@cache.cached("search_cache.pkl")
def search(topic):
    global tpc
    while True:
        try:
            tpc += 1

            if tpc % 2 == 0 and is_catalog_server_active[0]:
                res = requests.get('http://' + catalog_ip1 + ':' + catalog_port1 + '/search/' + topic).content
                break
            elif is_catalog_server_active[1]:
                res = requests.get('http://' + catalog_ip2 + ':' + catalog_port2 + '/search/' + topic).content
                break

        except:
            print("Failed to send request as server is down")

    return res


# End point for getting the books with the given topic, takes post request and topic in json
@router.route('/search/', methods=['POST'])
@cache.cached("search_cache.pkl")
def search_with_json_request():
    req_data = request.get_json()
    topic = req_data['topic']
    return search(topic)


# End point for getting the details of book with item_number, takes get request and item_number in URL
@router.route('/lookup/<item_number>', methods=['GET'])
@cache.cached("lookup_cache.pkl")
def lookup(item_number):
    print(lst, is_catalog_server_active, "is catalog server")
    global lookp
    while True:
        try:

            lookp += 1

            if lookp % 2 == 0 and is_catalog_server_active[0]:
                print("SENDING REQUEST LOOKUP TO CATALOG 1")
                res = requests.get('http://' + catalog_ip1 + ':' + catalog_port1 + '/lookup/' + item_number).content
                break
            elif is_catalog_server_active[1]:
                print("SENDING REQUEST LOOKUP TO CATALOG 2")
                res = requests.get('http://' + catalog_ip2 + ':' + catalog_port2 + '/lookup/' + item_number).content
                break
        except:
            print("Failed to send request as server is down")
    return res


# End point for getting the details of book with item_number, takes post request and item_number in json
@router.route('/lookup/', methods=['POST'])
def lookup_with_json_request():
    req_data = request.get_json()
    item_number = req_data['item_number']
    return lookup(item_number)


# End point for getting the quantity of book with item_number, takes get request and item_number in URL
@router.route('/get_quantity/<item_number>', methods=['GET'])
@cache.cached("get_q_cache.pkl")
def get_quantity(item_number):
    print(lst, is_catalog_server_active, "is catalog server")
    global get_q

    while True:
        try:
            get_q += 1

            if get_q % 2 == 0 and is_catalog_server_active[0]:
                print("SENDING REQUEST LOOKUP TO CATALOG 1")
                res = requests.get(
                    'http://' + catalog_ip1 + ':' + catalog_port1 + '/get_quantity/' + item_number).content
                break
            elif is_catalog_server_active[1]:
                print("SENDING REQUEST LOOKUP TO CATALOG 2")
                res = requests.get(
                    'http://' + catalog_ip2 + ':' + catalog_port2 + '/get_quantity/' + item_number).content
                break

        except:
            print("Failed to send request as server is down")
    return res


# End point for getting the quantity of book with item_number, takes post request and item_number in json
@router.route('/get_quantity/', methods=['POST'])
def get_quantity_with_json_request():
    req_data = request.get_json()
    item_number = req_data['item_number']
    return get_quantity(item_number)


# End point for updating the cost of book with item_number, takes get request and item number and cost in URL
@router.route('/update_c/<item_number>/<cost>', methods=['GET'])
def update_c(item_number, cost):
    res1 = ""
    res2 = ""

    try:
        if is_catalog_server_active[0]:
            print("SENDING REQUEST LOOKUP TO CATALOG 1")
            res1 = requests.get(
                'http://' + catalog_ip1 + ':' + catalog_port1 + '/update_c/' + item_number + '/' + cost).content
    except:
        print("Failed to send request as server is down")
    try:
        if is_catalog_server_active[1]:
            print("SENDING REQUEST LOOKUP TO CATALOG 2")
            res2 = requests.get(
                'http://' + catalog_ip2 + ':' + catalog_port2 + '/update_c/' + item_number + '/' + cost).content
    except:
        print("Failed to send request as server is down")
    return res1


# End point for updating the cost of book with item_number, takes post request and item_number and cost in json
@router.route('/update_c/', methods=['POST'])
def update_c_with_json_request():
    req_data = request.get_json()
    item_number = req_data['item_number']
    cost = req_data['cost']
    return update_c(item_number, cost)


# End point for updating the quantity of book with item_number, takes get request and item_number and quantity in URL
@router.route('/update_q/<item_number>/<quantity>', methods=['GET'])
def update_q(item_number, quantity):
    res1 = ""
    res2 = ""

    try:
        if is_catalog_server_active[0]:
            res1 = requests.get(
                'http://' + catalog_ip1 + ':' + catalog_port1 + '/update_q/' + item_number + '/' + quantity).content
    except:
        print("Failed to send request as server is down")
    try:
        if is_catalog_server_active[1]:
            res2 = requests.get(
                'http://' + catalog_ip2 + ':' + catalog_port2 + '/update_q/' + item_number + '/' + quantity).content
    except:
        print("Failed to send request as server is down")

    return res1


# End point for updating the quantity of book with item_number, takes post request and item number and quantity in json
@router.route('/update_q/', methods=['POST'])
def update_q_with_json_request():
    req_data = request.get_json()
    item_number = req_data['item_number']
    quantity = req_data['quantity']
    return update_q(item_number, quantity)


########################################################
# Forwards the buy requests to the order server

# End point to buy an item with item number get request
@router.route('/buy/<item_number>', methods=['GET'])
def buy(item_number):
    global bye

    # keep trying incase of in-progress requests fail to reach the server
    while True:
        try:
            bye += 1
            # print("entered list fun ")
            if bye % 2 == 0 and is_order_server_active[0]:
                res = requests.get('http://' + order_ip1 + ':' + order_port1 + '/buy/' + item_number).content
                break
            elif is_order_server_active[1]:
                res = requests.get('http://' + order_ip2 + ':' + order_port2 + '/buy/' + item_number).content
                break
        except:
            print("Failed to send request as server is down")

    return res


# End point to buy an item with item number post request
@router.route('/buy/', methods=['POST'])
def buy_with_json_request():
    req_data = request.get_json()
    item_number = req_data['item_number']
    return buy(item_number)


# Counter variables to indicate which servers turn it is
# Does load balancing by sending requests to alternate servers
get_q = 0
lst = 0
tpc = 0
lookp = 0
by = 0
get_q = 0
upd_q = 0
bye = 0
cach_list = ['get_q_cache.pkl', 'lookup_cache.pkl']
# parse config file
order_ip1, order_port1, order_ip2, order_port2, catalog_ip1, catalog_port1, catalog_ip2, catalog_port2, frontend_ip, frontend_port = configparse.parse()
print(catalog_ip1, catalog_port1)
