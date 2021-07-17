import subprocess
import pandas  as pd
import sqlite3 as sql
import os
import requests
import json
import db_logger
import argparse
import configparse

def db(database_name='database.db'):
    return sql.connect(database=database_name)



def resync(server,replica):

    #choose db replica
    database_name = 'database' + str(replica) + '.db'
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, database_name)

    # query the other catalog server to get the update log file
    URL = 'http://' + resync_contact_ip + ':' + resync_contact_port + '/files/'
    print(URL)
    response = requests.get('http://' + resync_contact_ip + ':' + resync_contact_port + '/files/')
    print("In resync")
    print(response.text)

    # create a copy locally
    with open('db_log_file_for_resync.csv', 'wb') as f:
        f.write(response.content)

    # resynch server
    # use the update log obtained from other catalog server to synchronize the missed updates to db
    correct="1"
    if replica=="1":
        correct="2"
    faulty=pd.read_csv("db_log_file_for_resync.csv")
    corrected = pd.read_csv("db_log" + server + correct + ".csv")
    last_copied_index = len(faulty.index)
    pending_trans = corrected.iloc[last_copied_index:]
    print("last_copied_index",last_copied_index,len(pending_trans.index))

    for index, row in pending_trans.iterrows():

        query=row["query"]
        field=row["field"]
        item_number=str(row["item_number"])
        value=str(row["value"])
        #log = 'update_c method: item ' + str(item_number) + ' cost to be updated ' + str(cost)
        print("query being executed:", query,field,value,index)
        #logging.debug(log)
        msg = ''
        try:
            with sql.connect(db_path) as con:
                res = requests.get('http://' + frontend_ip + ':' + frontend_port + '/invalidate/' + item_number).content
                cur = con.cursor()
                cur.execute(query, (value, item_number))
                con.commit()
                db_logger.db_log(query, field, item_number, value,i)
                msg = "Cost of item :" + str(item_number) + " successfully updated to:" + str(value)
        #
        except:
            con.rollback()
            msg = "error in update operation"

        finally:
            # log = 'update_c method: ' + msg
            # logging.debug(log)
            con.close()
        print(msg)



#read config file
frontend_ip="127.0.0.1";frontend_port='35303'

order_ip1,order_port1,order_ip2,order_port2,catalog_ip1,catalog_port1,catalog_ip2,catalog_port2,frontend_ip,frontend_port,i,z = configparse.parse()
# parser = argparse.ArgumentParser(description='')
# parser.add_argument('--r', metavar='r', type=str, help='config file', default='1')
# parser.add_argument('--s', metavar='s', type=str, help='config file', default='1')
# args = parser.parse_args()

if i=='1':
    resync_contact_ip = catalog_ip2
    resync_contact_port = catalog_port2
else:
    resync_contact_ip = catalog_ip1
    resync_contact_port = catalog_port1

resync('catalog',i)
