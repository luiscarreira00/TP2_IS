import sys
import time
import os

import psycopg2
from psycopg2 import OperationalError
from xml.etree.ElementTree import ElementTree



POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60


def print_psycopg2_exception(ex):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print("\npsycopg2 ERROR:", ex, "on line number:", line_num)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print("\nextensions.Diagnostics:", ex.diag)

    # print the pgcode and pgerror exceptions
    print("pgerror:", ex.pgerror)
    print("pgcode:", ex.pgcode, "\n")


if __name__ == "__main__":

    
    
    mydoc = ElementTree(file='fifa.xml')

    db_org = psycopg2.connect(host='db-xml', database='is', user='is', password='is')
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')

    while True:

        # Connect to both databases
        db_org = None
        db_dst = None

        try:
            db_org = psycopg2.connect(host='db-xml', database='is', user='is', password='is')
            db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        except OperationalError as err:
            print_psycopg2_exception(err)

        if db_dst is None or db_org is None:
            continue

        cursor1 = db_org.cursor()
        cursor2 = db_dst.cursor()

        print("Checking updates...")

       
        idPlayer = 1
        for e in mydoc.findall('./Player/Age'):
            cursor2.execute("INSERT INTO players (id, age) VALUES ({}, {}) ON CONFLICT DO NOTHING".format(idPlayer, e.text))
            idPlayer += 1

        idPlayer = 1
        for e in mydoc.findall('./Player/Name'):
            cursor2.execute("Update players SET name  = {}, updated_on = NOW() WHERE id = {}".format("'" + str(e.text.replace("'", "")) + "'", idPlayer))
            idPlayer += 1

        idPlayer = 1
        for e in mydoc.findall('./Player/Overall'):
            cursor2.execute("Update players SET overall = {}, updated_on = NOW() WHERE id = {}".format(e.text, idPlayer))
            idPlayer += 1
        
        idPlayer = 1
        for e in mydoc.findall('./Player/Nationality'):
            cursor2.execute("Update players SET nationality = {}, updated_on = NOW() WHERE id = {}".format( e.text, idPlayer))
            idPlayer += 1

        idNationality = 1
        for e in mydoc.findall('./Nationalities/Nationality'):
            cursor2.execute("INSERT INTO nationalities  VALUES ({}, {}) ON CONFLICT DO NOTHING".format(idNationality, "'" + str(e.text.replace("'", "")) + "'"))
            idNationality += 1

        

        db_dst.commit()


        # !TODO: 4- Make sure we store somehow in the origin database that certain records were already migrated.
        #          Change the db structure if needed.

        cursor1.execute("UPDATE imported_documents  SET estado = 'migrated', updated_on = NOW() WHERE imported_documents.file_name LIKE '/csv/fifa.csv';")

        db_org.commit()

        db_org.close()
        db_dst.close()

        time.sleep(POLLING_FREQ)
