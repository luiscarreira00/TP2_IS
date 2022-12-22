import sys
import time

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
        # !TODO: 1- Execute a SELECT query to check for any changes on the table
        # !TODO: 2- Execute a SELECT queries with xpath to retrieve the data we want to store in the relational db

        cursor1.execute("SELECT xml from imported_documents")

        result = cursor1.fetchall()


        for fileI in result:
            mydoc = ElementTree(file=open(fileI[0], encoding="UTF8").read() )

            idPlayer = 1
            for e in mydoc.findall('/Football/Teams/Team/Players//Player@name'):
                cursor2.execute("INSERT INTO players (id, age) VALUES ({}, {})".format(idPlayer, e.text))
                idPlayer += 1



        # !TODO: 3- Execute INSERT queries in the destination db
        # !TODO: 4- Make sure we store somehow in the origin database that certain records were already migrated.
        #          Change the db structure if needed.

        cursor1.execute("UPDATE imported_documents SET estado = 'migrated' VALUES (%s, %s);", (csv_path, xml_path))

        db_org.commit()

        db_org.close()
        db_dst.close()

        time.sleep(POLLING_FREQ)
