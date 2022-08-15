#!/usr/bin/env python
from msilib.schema import tables
import mysql.connector

'''
This module creates a mysql db instance - we set it to localhost for time being. 
ASSUMES INSTALLATION OF MYSQL SERVER
To be configured when deployed on AWS
'''

'''
@brief db_connect method
@detail establishes connection with database and returns the connection object
@detail for time being, this will not take any credentials. we will create on localhost only
@return mysql.connector.connection_cext.CMySQLConnection object
'''
def db_connect():
    cnx = mysql.connector.connect(
        host = "localhost",
        database = "mysql",
        user = "user",
        pw = "pw"
    )
    return cnx

def db_close(cnx):
    cnx.close()
    print "db conection closed"

'''
@brief init_setup_db method
@detail handles initial setup databse - should be used on first time init
@detail requires db connection as passed in parameter
@return None
'''
def init_setup_db(cnx):
    #create cursor object
    cursorObj = cnx.cursor()
    #create db
    cursorObj.execute("CREATE DATABASE game_payload")
    print "mysql cmd: CREATE DATABASE game_payload"
    print "is successful? : {}".format(is_correct_db(cnx))
    print "creating tables..."

    create_gameRecord_tbl = """CREATE TABLE GAMERECORD (
        DATE date NOT NULL,
        gamePK INT NOT NULL,
        record JSON
    );
    """
    cursorObj.execute(create_gameRecord_tbl)
    db_close(cnx)

def is_correct_db(cnx):
    if cnx.database == "game_payload":
        return True
    else: 
        return False

#create function that writes gamePK, home and away team to a table. so you can index teams by gamePK