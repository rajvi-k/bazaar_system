import argparse
import logging
import os
import configparser

# Here based on the arguments the config files are read and then the values are returned

def parse():
    # Arguments for the config file number
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--c', metavar='c', type=str, help='config file', default='1')
    args = parser.parse_args()
    config_file = "../config/config_" + (args.c) + '.txt'

    this_folder = os.path.dirname(os.path.abspath(__file__))
    this_file = os.path.join(this_folder, config_file)
    config = configparser.ConfigParser()
    config.read(this_file)
    print(this_file)
    # reading ip and port from the config file
    order_ip1 = str(config.get('conf', 'order1'))
    order_port1 = str(config.get('conf', 'order_port1'))
    catalog_ip1 = str(config.get('conf', 'catalog1'))
    catalog_port1 = str(config.get('conf', 'catalog_port1'))
    order_ip2 = str(config.get('conf', 'order2'))
    order_port2 = str(config.get('conf', 'order_port2'))
    catalog_ip2 = str(config.get('conf', 'catalog2'))
    catalog_port2 = str(config.get('conf', 'catalog_port2'))
    frontend_ip = str(config.get('conf', 'frontend'))
    frontend_port = str(config.get('conf', 'frontend_port'))

    return order_ip1, order_port1,order_ip2, order_port2, catalog_ip1, catalog_port1,catalog_ip2, catalog_port2, frontend_ip, frontend_port


def parseLists():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--c', metavar='c', type=str, help='config file', default='1')
    args = parser.parse_args()
    config_file = "../config_" + (args.c) + '.txt'

    this_folder = os.path.dirname(os.path.abspath(__file__))
    this_file = os.path.join(this_folder, config_file)
    config = configparser.ConfigParser()
    config.read(this_file)
    print(this_file)
    order_server_list = config.get('conf', 'order_server').split(',')
    catalog_server_list = config.get('conf', 'catalog_server').split(',')
    return catalog_server_list, order_server_list

# here all the heartbeat ports for all the servers are read from the config file

def get_heartbeat_ports():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--c', metavar='c', type=str, help='config file', default='1')
    parser.add_argument('--i', metavar='i', type=str, help='config file', default='1')

    args = parser.parse_args()
    config_file = "../config/config_" + (args.c) + '.txt'

    this_folder = os.path.dirname(os.path.abspath(__file__))
    this_file = os.path.join(this_folder, config_file)
    config = configparser.ConfigParser()
    config.read(this_file)
    heartbeat_order_port1 = str(config.get('conf', 'heartbeat_order1'))
    heartbeat_order_port2 = str(config.get('conf', 'heartbeat_order2'))
    heartbeat_catalog_port1 = str(config.get('conf', 'heartbeat_catalog1'))
    heartbeat_catalog_port2 = str(config.get('conf', 'heartbeat_catalog2'))
    return heartbeat_catalog_port1, heartbeat_catalog_port2, heartbeat_order_port1, heartbeat_order_port2
