from flask import Flask, render_template, jsonify
import json
import sqlite3 as sql
import requests
app = Flask(__name__)
import os
import configparser
import argparse

# The front end server supports three operations:
#
# search(topic) - which allows the user to specify a topic and returns all
# entries belonging to that category (a title and an item number are displayed for each match).
# lookup(item_number) - which allows an item number to be specified and returns details
# such as number of items in stock and cost
# buy(item_number) - which specifies an item number for purchase.



def list_books():
    res=json.loads(requests.get('http://'+frontend_ip+':'+frontend_port+'/list').content.decode("utf-8"))
    return res

def search(topic):
    return json.loads(requests.get('http://'+frontend_ip+':'+frontend_port+'/search/' + topic).content.decode("utf-8"))


def lookup(item_number):
    return json.loads(requests.get('http://'+frontend_ip+':'+frontend_port+'/lookup/' + item_number).content.decode("utf-8"))


def get_quantity(item_number):
    res=json.loads(requests.get('http://'+frontend_ip+':'+frontend_port+'/get_quantity/' + item_number).content.decode("utf-8"))
    return res

def update_c(item_number,cost):
    return json.loads(requests.get('http://'+frontend_ip+':'+frontend_port+'/update_c/'+item_number+'/'+cost).content.decode("utf-8"))

def update_q(item_number,quantity):
    return json.loads(requests.get('http://'+frontend_ip+':'+frontend_port+'/update_q/'+item_number+'/'+quantity).content.decode("utf-8"))


def buy(item_number):
    return json.loads(requests.get('http://'+frontend_ip+':'+frontend_port+'/buy/'+item_number).content.decode("utf-8"))





# parser = argparse.ArgumentParser(description='Process some integers.')
# parser.add_argument('--p', metavar='p', type=str,
#                     help='peer id')
# parser.add_argument('--c', metavar='c', type=str,
#                     help='config file')
#
# args = parser.parse_args()
# print(args.p, args.c)
# peer_id = "peer" + (args.p)
# config_file = "config_" + (args.c) + '.txt'

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--c', metavar='c', type=str,
                    help='config file',default='2')
args = parser.parse_args()
config_file = "config_" + (args.c) + '.txt'

this_folder=os.path.dirname(os.path.abspath(__file__))

this_folder = os.path.dirname(os.path.abspath(__file__))
this_file = os.path.join(this_folder, config_file)
config = configparser.ConfigParser()
config.read(this_file)

order_ip =str(config.get('conf', 'order'))
order_port = str(config.get('conf', 'order_port'))
catalog_ip =str(config.get('conf', 'catalog'))
catalog_port = str(config.get('conf', 'catalog_port'))
frontend_ip =str(config.get('conf', 'frontend'))
frontend_port = str(config.get('conf', 'frontend_port'))

print("Changing quantity of item 3 to 0")
print(update_q(str(3),'-153'))
print("Trying to buy item 3")
print(buy("3"))
# print(search('games'))
#
# print(list_books())