#!/usr/bin/env python
from msilib.schema import tables
import mysql.connector
from mysql.connector import errorcode

'''
This module creates a mysql db instance
ASSUMES INSTALLATION OF MYSQL SERVER
To be configured when deployed on AWS
'''

DB_NAME = "game_payload"

TABLES = {}
TABLES['GAMERECORD'] = """
    CREATE TABLE GAMERECORD (
    DATE DATETIME NOT NULL,
    GAMEPK INT NOT NULL,
    HOMETEAM VARCHAR(75) NOT NULL,
    AWAYTEAM VARCHAR(75) NOT NULL,
    RECORD TEXT
    )"""

#todo
'''create external config file with mysql creds'''

'''
@brief db_connect method
@detail establishes connection with database and returns the connection object
@detail for time being, this will not take any credentials. we will create on localhost only
@return mysql.connector.connection_cext.CMySQLConnection object
'''
def connect():
    cnx = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "mark",
        use_pure=True
    )
    return cnx

def close_connection(cnx):
    cnx.close()
    print "db conection closed"

def open_cursor(cnx):
    cursorObj = cnx.cursor()
    return cursorObj

def close_cursor(cursor):
    cursor.close()
    print "db cursor closed"

'''
@brief use_DB method
@detail tries to use DB_NAME as db. Exception provokes creation of db
@return None
'''
def use(cnx, cursor):
    try:
        cursor.execute("USE {}".format(DB_NAME))
        print "mysql> USE {}".format(DB_NAME)
        print "is correct db? : {}".format(is_correct_db(cnx))
    except mysql.connector.Error as err:
        print("error: {}").format(err)
        #print("Database {} does not exists.".format(DB_NAME))
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
        cursor.use(DB_NAME)
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

def is_correct_db(cnx):
    if cnx.database == DB_NAME:
        return True
    else: 
        return False

#create function that writes gamePK, home and away team to a table. so you can index teams by gamePK
def write(cnx,cursor,data):
    sql = """
    INSERT INTO GAMERECORD (DATE,GAMEPK,HOMETEAM,AWAYTEAM,RECORD)
    VALUES (%s,%s,%s,%s,%s)
    """
    row = {
        'DATE':data[0],
        'GAMEPK':data[1],
        'HOMETEAM':data[2],
        'AWAYTEAM':data[3],
        'RECORD':data[4]
    }
    cursor.execute(sql,data)
    cnx.commit()

'''TABLES['GAMERECORD'] = (
    "CREATE TABLE `GAMERECORD` ("
    "DATE date NOT NULL,"
    "GAMEPK INT NOT NULL,"
    "HOMETEAM VARCHAR(50)",
    "AWAYTEAM VARCHAR(50)",
    "RECORD JSON"
    ")"
    )'''