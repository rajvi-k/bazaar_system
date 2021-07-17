from flask import Flask, render_template, jsonify, request
import json
import sqlite3 as sql
import requests
import argparse
import configparse
from order_routes import order_router

import os
import configparser
import logging
import argparse
import threading
import socket
import pickle

app = Flask(__name__)

# Register blueprint for routes
app.register_blueprint(order_router)


# function to maintain heartbeat connection with the frontend

def heartbeat_order(orderip, heartbeat_port):
    print(" order server heartbeat port listening at:", heartbeat_port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((orderip, int(heartbeat_port)))

    while True:

        s.listen(1)

        # print('waiting for connection')
        conn, addr = s.accept()

        # print('connected with  frontend - Connection address: ', addr)

        data = conn.recv(1024)

        if not data:
            break

        message = pickle.loads(data)
        conn.send("Yes I am up".encode('ascii'))
        conn.close()


# parse config file
order_ip1, order_port1, order_ip2, order_port2, catalog_ip1, catalog_port1, catalog_ip2, catalog_port2, frontend_ip, frontend_port, i = configparse.parse()
heartbeat_catalog_port1, heartbeat_catalog_port2, heartbeat_order_port1, heartbeat_order_port2 = configparse.get_heartbeat_ports()

# choose replica instance
if i == "1":
    order_ip = order_ip1
    order_port = order_port1
    heartbeat_port = heartbeat_order_port1
else:
    order_ip = order_ip2
    order_port = order_port2
    heartbeat_port = heartbeat_order_port2

filename = 'order_Server' + str(i) + '.log'
# Logs are written in log file
logging.basicConfig(filename=filename, level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %('
                                                                   'threadName)s : %(message)s')

# background thread for the heartbeat connection with the frontend
t1 = threading.Thread(target=heartbeat_order, args=(order_ip,heartbeat_port,))
t1.daemon = True
t1.start()

# Starting the server with support for multithreaded requests
app.run(threaded=True, debug=False, host=order_ip, port=order_port)
