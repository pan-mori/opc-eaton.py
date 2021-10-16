# coding=utf_8

import redis
import json
import datetime
import psycopg2

CONNECTION = "postgres://heimdall_user:heimdall-pass@192.168.123.51:5432/heimdall"
#CONNECTION = "postgres://username:password@host:port/dbname"
#The above method of composing a connection string is for test or development purposes only,
#for production purposes be sure to make sensitive details like your password, hostname, and port number environment variables.

r = redis.StrictRedis(host='192.168.123.65', port=6379, db=0)


def main():
    with psycopg2.connect(CONNECTION) as conn:
        print("In main function.")
        #Uncomment if needed to create new table
        #create_table(conn)
        #Call the function that needs the database connection
        data_to_timescale(conn)
        print("Data succesfully transfered.")


def data_to_timescale(conn):
    cur = conn.cursor()
    print("Now transfering data to timescale.")
    for key in r.keys():
        data = json.loads(r.get(key).decode('utf-8'))
        try:
            cur.execute("INSERT INTO Main VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",( key.decode('utf-8'), data["Temperatur_Permeat"], data["Füllstand_Vorlage"], data["Temperatur_Spülbehälter"], data["pH_Wert_Arbeitsbehälter"], data["pH_Wert_Permeat"], data["Füllstand"], data["Druck_UF_Loop_2"], data["Füllstand_UF_Vorlage"], data["Füllstand_Arbeitsbehälter"], data["Druck_UF_Loop_1"], data["Durchfluss_UF_Ablauf"], data["Durchfluss_Arbeitsbehälter"], data["Temperatur_Vorlage"], data["pH_Wert_Vorlage"], data["Temperatur_Arbeitsbehälter"], data ["Druck_Zulauf_UF"], data ["Füllstand_Spülbehälter"], data["Durchfluss_Permeat"], data["Durchfluss_UF_Loop"], data["Temperatur_UF_Loop"]))
            r.delete(key);
        except:
            print("This key is not valid.")
        conn.commit()


def create_table(conn):
    query_create_main_table = "CREATE TABLE Main(Date TIMESTAMP NOT NULL, Temperatur_Permeat REAL, Füllstand_Vorlage REAL, Temperatur_Spülbehälter REAL, pH_Wert_Arbeitsbehälter REAL, pH_Wert_Permeat REAL, Füllstand REAL, Druck_UF_Loop_2 REAL, Füllstand_UF_Vorlage REAL, Füllstand_Arbeitsbehälter REAL, Druck_UF_Loop_1 REAL, Durchfluss_UF_Ablauf REAL, Durchfluss_Arbeitsbehälter REAL, Temperatur_Vorlage REAL, pH_Wert_Vorlage REAL, Temperatur_Arbeitsbehälter REAL, Druck_Zulauf_UF REAL, Füllstand_Spülbehälter REAL, Durchfluss_Permeat REAL, Durchfluss_UF_Loop REAL, Temperatur_UF_Loop REAL);"
    cur = conn.cursor()
    cur.execute(query_create_main_table)
    conn.commit()
    cur.close()



main()