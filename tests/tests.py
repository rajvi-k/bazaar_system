from flask import Flask, render_template, jsonify
import json
import sqlite3 as sql
import requests

import os
import configparse
import argparse
import time

app = Flask(__name__)
# This file is was used to perform tests and evaluation and performance experiments
# It makes requests to the front end server and checks for latency in cache how it helps and how it is an overhead
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



order_ip1, order_port1,order_ip2, order_port2, catalog_ip1, catalog_port1,catalog_ip2, catalog_port2, frontend_ip, frontend_port,i =configparse.parse()

t0 = time.time()
get_q=0
i='1'
by=0
up_c=0;up_q=0;llk=0
for i in  range(1):

    t1 = time.time()
    get_quantity(str(i))
    t2=time.time()
    get_q+=t2-t1

    t4 = time.time()
    update_c(str(i), str(10))
    t5 = time.time()
    up_c += t5 - t4

    t6 = time.time()
    update_q(str(i), str(20))
    t7 = time.time()
    up_q += t7 - t6

    t8 = time.time()
    print(buy(str(i)))
    t9 = time.time()

    by += t9 - t8
    t10 = time.time()
    lookup(str(i))
    t11 = time.time()
    llk=t11=t10
print(get_q/4,up_c/4,up_q/4,by/4,llk/4)
# print(update_c(str(2),'0'))
# print(buy("3"))
# print(search('games'))
#
# print(list_books())