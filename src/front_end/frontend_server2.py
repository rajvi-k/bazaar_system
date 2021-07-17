from flask import Flask, render_template, jsonify, request, Blueprint
from front_end_routes import router
import configparse
import json
import sqlite3 as sql
import requests
import argparse
import logging
import pickle
import os
import configparser


# This is the front end server which takes the request from the client and processes it
app = Flask(__name__)

#Register blueprint for routes
app.register_blueprint(router)

#parse config file
order_ip1,order_port1,order_ip2,order_port2,catalog_ip1,catalog_port1,catalog_ip2,catalog_port2,frontend_ip,frontend_port = configparse.parse()

# starting server with support for multithreaded requests
app.run(threaded=True, debug=True, host=frontend_ip, port=frontend_port)
