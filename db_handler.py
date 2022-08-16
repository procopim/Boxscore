#!/usr/bin/env python
from msilib.schema import tables
import mysql.connector
from mysql.connector import errorcode

'''
This module creates a mysql db instance - we set it to localhost for time being. 
ASSUMES INSTALLATION OF MYSQL SERVER
To be configured when deployed on AWS
'''

DB_NAME = "game_payload"

TABLES = {}
TABLES['GAMERECORD'] = (
    "CREATE TABLE `GAMERECORD` ("
    "DATE date NOT NULL,"
    "gamePK INT NOT NULL,"
    "record JSON"
    ")"
    )

'''
@brief db_connect method
@detail establishes connection with database and returns the connection object
@detail for time being, this will not take any credentials. we will create on localhost only
@return mysql.connector.connection_cext.CMySQLConnection object
'''
def DB_connect():
    cnx = mysql.connector.connect(
        host = "localhost",
        database = "mysql",
        user = "user",
        pw = "pw",
        use_pure=True
    )
    return cnx

def DB_close(cnx):
    cnx.close()
    print "db conection closed"

def open_DB_cursor(cnx):
    cursorObj = cnx.cursor()
    return cursorObj

def close_DB_cursor(cursor):
    cursor.close()
    print "db cursor closed"

'''
@brief use_DB method
@detail tries to use DB_NAME as db. Exception provokes creation of db
@return None
'''
def use_DB(cnx, cursor):
    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_DB(cnx, cursor)
    else:
        print(err)
        exit(1)

'''
@brief create_DB method
@detail handles initial setup databse - should be used on first time init
@detail requires db connection as passed in parameter
@return None
'''
def create_DB(cnx,cursor):
    try:
        #create db
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        print "mysql cmd: CREATE DATABASE {}".format(DB_NAME)
        print "is successful? : {}".format(is_correct_db(cnx))
        #cnx.database = DB_NAME --- do we need to set this before running is_correct_db() ? 
        print "creating tables..."

        create_tables(cnx, cursor)

    except mysql.connector.Error as err:
        print "Failed to create database: {}".format(err)
        exit(1)

def create_tables(cnx, cursor):
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name))
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    close_DB_cursor(cursor)
    DB_close(cnx)

def is_correct_db(cnx):
    if cnx.database == DB_NAME:
        return True
    else: 
        return False

#create function that writes gamePK, home and away team to a table. so you can index teams by gamePK