from flask import Flask, render_template, jsonify
import json
import sqlite3 as sql
import requests
app = Flask(__name__)
import os
import configparse
import argparse
import time
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
    res=json.loads(requests.get('http://'+frontend_ip+':'+frontend_port+'/update_c/'+item_number+'/'+cost).content.decode("utf-8"))
    return res
def update_q(item_number,quantity):
    requests.get('http://'+frontend_ip+':'+frontend_port+'/update_q/'+item_number+'/'+quantity).content.decode("utf-8")
    return


def buy(item_number):
    return json.loads(requests.get('http://'+frontend_ip+':'+frontend_port+'/buy/'+item_number).content.decode("utf-8"))

frontend_ip='127.0.0.1'; frontend_port='35303'
# update_c("1","200")






t0 = time.time()
get_q=0;ltt=0
i='1'
by=0
up_c=0;up_q=0;lk=0
for j in  range(1000):

    t1 = time.time()
    get_quantity(str(i))
    t2=time.time()
    get_q+=t2-t1

    t4 = time.time()
    update_c(str(i), str(1000))
    t5 = time.time()
    up_c += t5 - t4

    t6 = time.time()
    update_q(str(i), str(2000))
    t7 = time.time()
    up_q += t7 - t6

    t8 = time.time()
    buy(str(i))
    t9 = time.time()

    by += t9 - t8

    t10 = time.time()
    lookup(str(i))
    t11 = time.time()
    lk+=t11-t10

    t12 = time.time()
    list()
    t13 = time.time()
    ltt+= t13 - t12
print(get_q/1000,up_c/1000,up_q/1000,by/1000,lk/1000,ltt/1000)
# print(update_c(str(2),'0'))
# print(buy("3"))
# print(search('games'))
#
# print(list_books())