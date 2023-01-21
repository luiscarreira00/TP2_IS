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

        cursor = db_dst.cursor()
        cursor1 = db_dst.cursor()
        
        listaJogadores=[]
        listaPais=[]

        cursor.execute("Select id, name, age, overall from players")
        cursor1.execute("Select id, name from nationalities")
        

        results = cursor.fetchall()
        results1 = cursor1.fetchall()
            
        for result in results:
            listaJogadores.append(result)  
        for result1 in results1:
            listaPais.append(result1)      
        for i in range(len(listaJogadores)):
            for j in range(len(listaPais)):
                if listaJogadores[i][4] == listaPais[j][0]:
                    listaJogadores[i][4] = listaPais[j][1]
    
        return listaJogadores


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

        cursor = db_dst.cursor()
        
        listaPais=[]

        cursor.execute("Select id, name from nationalities")
        

        results = cursor.fetchall()
            
        for result in results:
            listaPais.append(result)  
        return listaPais        
# set of all teams
# !TODO: replace by database access
teams = [
]

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

@app.route('/api/getJogadorPais', methods=['GET'])
def get_data():
    listaJogadorPais=getJogadoresDePais()
    return jsonify(listaJogadorPais)

@app.route('/api/getPais', methods=['GET'])
def get_data():
    listaPais=getPais()
    return jsonify(listaPais)

@app.route('/api/data', methods=['GET'])
def get_data():
    listaJogadores=getJogadores()
    return jsonify(listaJogadores)

@app.route('/api/teams/', methods=['GET'])
def get_teams():
    return jsonify([team.__dict__ for team in teams])


@app.route('/api/teams/', methods=['POST'])
def create_team():
    data = request.get_json()
    team = Team(name=data['name'])
    teams.append(team)
    return jsonify(team.__dict__), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
