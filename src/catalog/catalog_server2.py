from flask import Flask, render_template, jsonify, request
import json
import sqlite3 as sql
import requests
import os
from catalog_routes import catalog_router
import configparser
import logging
import argparse
import configparse
import threading
import socket
import pickle
from database_and_table_creation import start_db_connection

app = Flask(__name__)

# This is the catalog server which is responsible for all the actions related to the db
# Select, Update are implemented through the get and post requests of HTTP

# Register blueprint for routes
app.register_blueprint(catalog_router)


# Maintain Heartbeat connection with front end
def heartbeat_catalog(catalogip, heartbeat_port):
    print(" catalog heartbeat port listening at:", heartbeat_port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((catalogip, int(heartbeat_port)))

    # listens for requests from frontend
    while True:

        s.listen(1)

        # print('waiting for connection')
        conn, addr = s.accept()

        # print('connected with frontend - Connection address: ', addr)

        data = conn.recv(1024)

        if not data:
            break

        message = pickle.loads(data)

        # responds with I am up reply
        conn.send("Yes I am up".encode('ascii'))

        conn.close()


# read config file
order_ip1, order_port1, order_ip2, order_port2, catalog_ip1, catalog_port1, catalog_ip2, catalog_port2, frontend_ip, frontend_port, i, restart = configparse.parse()
heartbeat_catalog_port1, heartbeat_catalog_port2, heartbeat_order_port1, heartbeat_order_port2 = configparse.get_heartbeat_ports()

# choose replica instance
if i == "1":
    catalog_ip = catalog_ip1
    catalog_port = catalog_port1
    heartbeat_port = heartbeat_catalog_port1
else:
    catalog_ip = catalog_ip2
    catalog_port = catalog_port2
    heartbeat_port = heartbeat_catalog_port2

filename = 'catalog_server' + str(i) + '.log'
# Logs are written in log file
logging.basicConfig(filename=filename, level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %('
                                                                   'threadName)s : %(message)s')

# if restart == '0':
# start db connection
start_db_connection(i)

# starting background thread for heartbeat with frontend server
t1 = threading.Thread(target=heartbeat_catalog, args=(catalog_ip, heartbeat_port,))
t1.daemon = True
t1.start()

print("Running on ", catalog_ip, catalog_port)
# Starting with multithread request support
app.run(threaded=True, debug=False, host=catalog_ip, port=catalog_port)
