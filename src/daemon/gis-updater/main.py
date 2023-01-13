import sys
import time
import psycopg2
from psycopg2 import OperationalError
import requests
import pycountry
from geojson import loads
import json

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60
ENTITIES_PER_ITERATION = int(sys.argv[2]) if len(sys.argv) >= 3 else 10

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

    headers = {'Api-User-Agent': 'myBot/0.0.1'}

    while True:
        print(f"Getting up to {ENTITIES_PER_ITERATION} entities without coordinates...")
        # !TODO: 1- Use api-gis to retrieve a fixed amount of entities without coordinates (e.g. 100 entities per iteration, use ENTITIES_PER_ITERATION)

        db_dst = None

        try:
            db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        except OperationalError as err:
            print_psycopg2_exception(err)

        if db_dst is None:
            continue

        cur = db_dst.cursor()

        print("Checking updates...")

       
        cur.execute("SELECT name FROM nationalities WHERE geom IS NULL LIMIT %s", (ENTITIES_PER_ITERATION,))

        rows = cur.fetchall()

        # Iterate over the rows
        for row in rows:
            # Do something with the row
            print(str(row[0]))
            country = pycountry.countries.lookup(str(row[0]))
            url = " https://nominatim.openstreetmap.org/search?format=json&country={}".format(country.alpha_2)
            response = requests.get(url, headers=headers)

            data = response.json()
            
            json_string = json.dumps(data)

            # Convert to geojson
            geom = loads(json_string)

            cur.execute("Update nationalities SET geom = (%s) WHERE name = %s", ((json.dumps(geom),), str(row[0])))


        db_dst.commit()
        db_dst.close()




        # !TODO: 2- Use the entity information to retrieve coordinates from an external API
        # !TODO: 3- Submit the changes
        time.sleep(POLLING_FREQ)



        


