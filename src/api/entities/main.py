import sys
import psycopg2
from psycopg2 import OperationalError

from flask import Flask, jsonify, request
from flask_cors import CORS

from entities import Team

#teste
#from main import odd_even, add
#import sys
#import os 

#dir_path = os.path.dirname(os.path.realpath("migrator"))
# adding Folder_2 to the system path
#sys.path.insert(0, dir_path+'/main.py')
#print(dir_path+'/main.py')
#fim teste

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000



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
        for h in range(len(listaJogadores2)):
            for u in range(len(listaPais2)):
                if listaJogadores2[h][4] == listaPais2[u][0]:
                    listaJogadores2[h][4] = listaPais2[u][1]
    
        return listaJogadores2


def getJogadores():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')

    while True:
        db_dst = None

        try:
           db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        except OperationalError as err:
            print_psycopg2_exception(err)

        if db_dst is None:
            continue

        cursor = db_dst.cursor()
        
        listaJogadores=[]

        cursor.execute("Select id, name, age, overall from players")
        

        results = cursor.fetchall()
            
        for result in results:
            listaJogadores.append(result)  
        return listaJogadores
        
def getPais():
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')

    while True:
        db_dst = None

        try:
           db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        except OperationalError as err:
            print_psycopg2_exception(err)

        if db_dst is None:
            continue

        cursor2 = db_dst.cursor()
        
        listaPais=[]

        cursor2.execute("Select id, name from nationalities")
        

        results2 = cursor2.fetchall()
            
        for result2 in results2:
            listaPais.append(result2)  
        return listaPais

# set of all teams
# !TODO: replace by database access
teams = [
]

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

@app.route('/api/getJogadorPais', methods=['GET'])
def get_data2():
    listaJogadores2=getJogadoresDePais()
    return jsonify(listaJogadores2)

@app.route('/api/getPais', methods=['GET'])
def get_data1():
    listaPais=getPais()
    return jsonify(listaPais)

@app.route('/api/data', methods=['GET'])
def get_data():
    listaJogadores1=getJogadores()
    return jsonify(listaJogadores1)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
