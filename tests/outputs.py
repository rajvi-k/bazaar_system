from flask import Flask, render_template, jsonify
import json
import requests
import os
import configparser
import argparse


app = Flask(__name__)

# This is the client to make requests to the front end to test the entire system


def list_books():
    print("List Books Test")
    string = 'http://' + frontend_ip + ':' + frontend_port + '/list'
    print(string)
    res = json.loads(requests.get('http://' + frontend_ip + ':' + frontend_port + '/list').content.decode("utf-8"))
    return res


def search(topic):
    print("Search request test")
    request_dict = {"topic": topic}
    return json.loads(
        requests.post('http://' + frontend_ip + ':' + frontend_port + '/search/', json=request_dict).content.decode(
            "utf-8"))




def lookup(item_number):
    print("lookup test for item ", item_number)
    return json.loads(requests.get('http://'+frontend_ip+':'+frontend_port+'/lookup/' + item_number).content.decode("utf-8"))


def get_quantity(item_number):
    print("get quantity test for item ", item_number)
    res=json.loads(requests.get('http://'+frontend_ip+':'+frontend_port+'/get_quantity/' + item_number).content.decode("utf-8"))
    return res



def update_c(item_number, cost):
    print("update cost test for item ", item_number, " to ", cost)
    request_dict = {"item_number": item_number, "cost": cost}
    return json.loads(requests.post(
        'http://' + frontend_ip + ':' + frontend_port + '/update_c/', json=request_dict).content.decode("utf-8"))


def update_q(item_number, quantity):
    print("update quantity test for item ", item_number, " to ", quantity)
    request_dict = {"item_number": item_number, "quantity": quantity}
    return json.loads(requests.post(
        'http://' + frontend_ip + ':' + frontend_port + '/update_q/',
        json=request_dict).content.decode(
        "utf-8"))


def buy(item_number):
    print("Buy test for item ", item_number)
    request_dict = {"item_number": item_number}
    return json.loads(
        requests.post('http://' + frontend_ip + ':' + frontend_port + '/buy/',
                      json=request_dict).content.decode("utf-8"))


print("Client started running tests for json post requests")


parser = argparse.ArgumentParser(description='')
parser.add_argument('--c', metavar='c', type=str,
                    help='config file')

args = parser.parse_args()
config_file = "config_" + (args.c) + '.txt'

this_folder = os.path.dirname(os.path.abspath(__file__))
this_file = os.path.join(this_folder, config_file)
config = configparser.ConfigParser()
config.read(this_file)

frontend_ip = str(config.get('conf', 'frontend'))
frontend_port = str(config.get('conf', 'frontend_port'))


print("================================================")
print("Running some tests")
# print("Listing all the items present and their details\n", list_books())

print(get_quantity("1"))
print("================================================")
print(lookup("1"))
print("================================================")
print(update_c('1', '10'))
print("================================================")
#
# print(search("Distributed_systems"))
# print("================================================")
#
# print(buy("1"))
# print("================================================")
#
# print(lookup("1"))
# print("================================================")

# print(lookup("1"))
# print("================================================")
# print(lookup("3"))
# print("================================================")
# print(lookup("3"))
# print("================================================")

print(get_quantity("1"))
print("================================================")


