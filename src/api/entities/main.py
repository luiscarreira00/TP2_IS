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

        #print("Checking data...")
        
        listaJogadores=[]

        cursor.execute("Select id, name from players")
        

        results = cursor.fetchall()
            
        for result in results:
            listaJogadores.append(result)
        #data = [row.__dict__ for row in results]
        
        #for row in data:
        #    row.pop('_sa_instance_state')

       # print("jogador.........")
       # for element in listaJogadores:
        #    if element[0]==3:
        #        print(element[1])
        #print(listaJogadores)    
        
# set of all teams
# !TODO: replace by database access
teams = [
]

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

data = [{'name': 'example1', 'value': 1}, {'name': 'example2', 'value': 2}]
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(data)

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
