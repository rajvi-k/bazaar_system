from flask import Flask, render_template, jsonify, request, Blueprint
from front_end_routes import router
import configparse
from front_end_routes import heartbeat_catalog, heartbeat_order
import json
import sqlite3 as sql
import requests
import argparse
import logging
import pickle
import time
import os
import configparser
import threading
from threading import Lock
import socket
from configparse import parseLists

# This is the front end server which takes the request from the client and processes it
app = Flask(__name__)



# Register blueprint for routes
app.register_blueprint(router)

# parse config file
order_ip1,order_port1,order_ip2,order_port2,catalog_ip1,catalog_port1,catalog_ip2,catalog_port2,frontend_ip,frontend_port = configparse.parse()
heartbeat_catalog_port1, heartbeat_catalog_port2, heartbeat_order_port1, heartbeat_order_port2 = configparse.get_heartbeat_ports()

# reading ip and port from the config file
heartbeat_catalog_servers = [[str(catalog_ip1), str(heartbeat_catalog_port1)], [str(catalog_ip2), str(heartbeat_catalog_port2)]]


heartbeat_order_servers = [[str(order_ip1), str(heartbeat_order_port1)], [str(order_ip2),str(heartbeat_order_port2)]]


# starting background threads for heartbeat with catalog
t1 = threading.Thread(target=heartbeat_catalog, args=(heartbeat_catalog_servers,))
t1.daemon = True
t1.start()

#  starting background threads for heartbeat with  and the order servers

t2 = threading.Thread(target=heartbeat_order, args=(heartbeat_order_servers,))
t2.daemon = True
t2.start()

# starting server with support for multithreaded requests
if __name__=='__main__':
    app.run(threaded=True, debug=False, host=frontend_ip, port=frontend_port)
