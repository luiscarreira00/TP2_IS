import sys
import time
import psycopg2
from psycopg2 import OperationalError
import requests
import pycountry
from geojson import loads
import json
from shapely.geometry import shape

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
            if(str(row[0])=="England" or str(row[0])=="Scotland" or str(row[0])=="Wales" or str(row[0])=="Northern Ireland"): 
                country = pycountry.countries.lookup("United Kingdom")
            
            elif(str(row[0])=="Korea Republic"):
                country = pycountry.countries.lookup("Korea, Republic of")
            elif(str(row[0])=="Côte dIvoire"):
                country = pycountry.countries.lookup("Côte d'Ivoire")
            elif(str(row[0])=="Russia"):
                country = pycountry.countries.lookup("Russian Federation")
            elif(str(row[0])=="Congo DR"):
                country = pycountry.countries.lookup("Congo")
            elif(str(row[0])=="China PR"):
                country = pycountry.countries.lookup("China")
            elif(str(row[0])=="Iran"):
                continue
            elif(str(row[0])=="Republic of Ireland"):
                country = pycountry.countries.lookup("Ireland")
            elif(str(row[0])=="Cape Verde Islands"):
                country = pycountry.countries.lookup("Cabo Verde")
            elif(str(row[0])=="Syria"):
                country = pycountry.countries.lookup("Syrian Arab Republic")
            elif(str(row[0])=="Guinea Bissau"):
                country = pycountry.countries.lookup("Guinea-Bissau")
            elif(str(row[0])=="Curacao"):
                country = pycountry.countries.lookup("Curaçao")
            elif(str(row[0])=="Palestine"):
                country = pycountry.countries.lookup("Palestine, State of")
            elif(str(row[0])=="Korea DPR"):
                continue
            elif(str(row[0])=="Chinese Taipei"):
                continue
            elif(str(row[0])=="Kosovo"):
                continue
            else:
                country = pycountry.countries.lookup(str(row[0]))
  
            url = f"https://nominatim.openstreetmap.org/search?format=geojson&polygon_geojson=1&country={country.alpha_2}"
            response = requests.get(url, headers=headers)

            data = response.json()
            if 'features' in data and len(data['features']) > 0:
                feature = data['features'][0]
                if feature['geometry']['type'] == 'Polygon' or feature['geometry']['type'] == 'MultiPolygon':
                    # Convert the GeoJSON feature to a shapely Polygon or MultiPolygon
                    geo = shape(feature['geometry'])
                    # Convert the shapely Polygon or MultiPolygon to a WKT string
                    wkt = geo.wkt
                    # Execute an SQL query to update the "nationalities" table
                    cur.execute("UPDATE nationalities SET geom = ST_SetSRID(ST_GeomFromText(%s),4326), updated_on = NOW() WHERE name = %s", (wkt, str(row[0])))
                    db_dst.commit()


        
        db_dst.close()




        # !TODO: 2- Use the entity information to retrieve coordinates from an external API
        # !TODO: 3- Submit the changes
        time.sleep(POLLING_FREQ)



        


