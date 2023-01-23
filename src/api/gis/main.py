import sys
import time
import psycopg2
from psycopg2 import OperationalError

from flask import Flask, jsonify, request
from flask_cors import CORS
from geopy.geocoders import Nominatim
import requests

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True

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


def getJogadoresDePais():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')

    while True:
        db_dst = None

        try:
           db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        except OperationalError as err:
            print_psycopg2_exception(err)

        if db_dst is None:
            continue

        cursorJog = db_dst.cursor()
        cursorNat = db_dst.cursor()
        
        listaJogadores2=[]
        listaPais2=[]

        cursorJog.execute("Select id, name, age, overall, nationality from players")
        cursorNat.execute("Select id, name from nationalities")
        

        resultsJog = cursorJog.fetchall()
        resultsNat = cursorNat.fetchall()
            
        for resultJog in resultsJog:
            listaJogadores2.append(resultJog)  
        for resultNat in resultsNat:
            listaPais2.append(resultNat)      
        new_listaJogadores2 = []
        for h in range(len(listaJogadores2)):
            for u in range(len(listaPais2)):
                if listaJogadores2[h][4] == listaPais2[u][0]:
                    new_listaJogadores2.append(list(listaJogadores2[h][:4])+[listaPais2[u][1]])

        keys = ["id", "name", "age", "overall", "country"]
        result = [{keys[i]: item[i] for i in range(len(keys))} for item in new_listaJogadores2]
        #result.sort(key=lambda x: x["id"])

        print("vai entrar no for")
        for player in result:
            # Define the country name
            country_name = player["country"]

            # Make a request to the Nominatim API
            url = f"https://nominatim.openstreetmap.org/search?q={country_name}&format=json"
            response = requests.get(url)

            # Parse the response
            exe = response.json()

            # Get the coordinates of the first result
            latitude = exe[0]["lat"]
            longitude = exe[0]["lon"]
            player["coordinates"] = [latitude, longitude]


        return result

@app.route('/api/markersJogadores', methods=['GET'])
def get_data3():
    listaJogadores2=getJogadoresDePais()
    return jsonify(listaJogadores2)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
