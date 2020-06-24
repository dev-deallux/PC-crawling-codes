# -----------------------------------------------
# LUXPACE SERVICE LIBRARY
# -----------------------------------------------
# Usage: Store/Restore Common Core Data to access
#        Luxpace-related DB / Servers
# -----------------------------------------------

# -------------------------------------
# Primitive Data for Lux Service
# -------------------------------------
# 2019. 12. 18. (Tue)
# -------------------------------------

# --------------------------------------
# Import External Modules
# --------------------------------------

import sys
import os

# sys.path.append('/home/ec2-user/sshutl_env/include')

import pymysql
import socket
import ssl
from woocommerce import API

import urllib
import requests
from requests import get
import json

from suds.client import Client
import logging

import csv
import time
import datetime

from dateutil.parser import parse

# -------------------------------------
# luxpace_db data
# -------------------------------------

DB_NAME = "luxpace_db"
DB_user = "root"
DB_password = "dmswjddl1"
DB_charset = 'utf8'
DB_host = "localhost"

"""
# -------------------------------------
# sshutl_table core data
# -------------------------------------

SS_CORE_TABLE = "ss_sys_data"
SS_CORE_ID = "ss_sys_id"
SS_CORE_KEY = "ss_key"
SS_CORE_VALUE = "ss_value"
SS_CORE_CREATEDTIME = "ss_created_time"
SS_CORE_LASTMODITIME = "ss_last_modified_time"

# ---------------------------------------
# sshutl_table system operation log table
# ---------------------------------------

SS_SYS_OP_LOG_TABLE = "ss_sys_op_log"
SS_SYS_OP_ID = "ss_sys_op_id"
SS_SYS_SW_PATH = "ss_sw_path"
SS_SYS_SW_MODULE = "ss_sw_module"
SS_SYS_SW_ARGS = "ss_sw_args"
SS_SYS_OP_TIME = "ss_op_time"

# ------------------------------------
# sshutl_table some primitive keywords
# ------------------------------------

SS_CURR_SVR = "curr_svr"

# --------------------------------------------
# mysql query for accessing specific key-value
# --------------------------------------------

sql_cmd_get_value_from_core_db = \
       "select {0} from {1} where {2}=%s;".format(SS_CORE_VALUE, \
                                    SS_CORE_TABLE, SS_CORE_KEY)
sql_cmd_set_value_to_core_db = \
       "update {0} set {1}=%s, {2}=now() where {3}=%s;".format(SS_CORE_TABLE,\
                            SS_CORE_VALUE, SS_CORE_LASTMODITIME, SS_CORE_KEY)
"""

# -------------------
# connect_database ()
# -------------------
def connect_database (db_char=DB_charset):
    db = pymysql.connect (host=DB_host, port=3306, \
                         user=DB_user, password=DB_password, \
                         db=DB_NAME, charset=DB_charset, \
                         autocommit=True, local_infile=True)
    return (db)


# -------------------
# close_database (db)
# -------------------
def close_database(db):
    db.close()

"""
# --------------------------------
# check_data_exist_in_database()
# : Check the data is in DB or not
# --------------------------------

def check_data_exist_in_database(cursor,str_table,str_condition):

    sql = "select EXISTS (select * from {0} where {1}) as success;".format(str_table,str_condition) 

    # print (sql)

    cursor.execute(sql)
    result = cursor.fetchall()

    return (result[0][0])


# -----------------------
# call_service()
# -----------------------

def call_service(cursor):
    url = get_sshutl_data(cursor,"studio69_url")
    wsdl = url+"?wsdl"
    curr_id = get_sshutl_data(cursor, "studio69_id")
    curr_pw = get_sshutl_data(cursor, "studio69_pw")

    print ("DEBUGGING: ", wsdl, " ", curr_id)
    # print (curr_id, curr_pw)

    try_cnt = 0
    max_try = 5

    while max_try > try_cnt:

        try:

            try_cnt += 1
            client = Client(wsdl, username=curr_id, password=curr_pw)
            max_try = try_cnt

        except Exception as e:
            print (" ")
            print (" Exception : call_service() of ss_sys_data ", e)
            print (" Retry COUNT : ", try_cnt)
            print (" Will try to contact 30 seconds later")
            print (" ")
            if (try_cnt == max_try):
                print (" MAX Try count exceeds & Retry later ")
                exit()
            sleep (10)


    print ("Contacting Studio69 Server")
    result = client.service.CheckWebService()
    print (result)
    return (result, client)


# ------------------
# get_sshutl_data ()
# ------------------
def get_sshutl_data (cursor,key):
    cursor.execute(sql_cmd_get_value_from_core_db,(key))
    ret = cursor.fetchall()

    if len(ret) == 1:
        return (ret[0][0])
    else:
        return ""


# ------------------
# set_sshutl_data ()
# ------------------
def set_sshutl_data (cursor,key,value):
    cursor.execute(sql_cmd_set_value_from_core_db,(value,key))
    ret = cursor.fetchall()

    if len(ret) == 1:
        return (ret[0][0])
    else:
        return ""


# ===================================================
# ---------------------------------------------------
# For logging SShutl Back-End Server Apps' Operations
# ---------------------------------------------------
# ===================================================


sql_cmd_sys_op = "insert into {0} ({1}, {2}, {3}) values (%s, %s,%s)".format(SS_SYS_OP_LOG_TABLE, SS_SYS_SW_PATH, SS_SYS_SW_MODULE, SS_SYS_SW_ARGS)


# -------------
# log_sys_op ()
# -------------
def log_sys_op(curr_sw, curr_args):
    db = connect_database()
    cursor = db.cursor()

    temp = ' '.join(curr_args[0:])
    realpath = os.getcwd()
    cursor.execute(sql_cmd_sys_op, (realpath, curr_sw, temp))

    close_database (db)
"""
