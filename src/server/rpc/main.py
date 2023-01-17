import signal, sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from functions.teste import selectPlayersFromOverall

import psycopg2
import csv
from xml.etree.ElementTree import ElementTree
import json

def is_even(n):
    print("teste no server")
    return n % 2 == 0

def listaNacionalidade():
   listaNacionalidades = [list]

   inputFile = csv.reader(open('/csv/fifa.csv', encoding="utf8"))

   rowNum = 0
   idNum = 1
   for row in inputFile:
      if rowNum == 0:
         tags = row
         for i in range(len(tags)):
               tags[i] = tags[i].replace('   ', '')
      else:
         for i in range(len(tags)):
               pertence = False
               if (i == 7):
                  for pais in range(len(listaNacionalidades)):
                     if( row[i] == listaNacionalidades[pais]):
                           pertence = True
                           break
                  if(pertence == False):
                     # replace ampersand with character entity.
                     row[i] = row[i].replace('&', '&amp;')
                     row[i] = row[i].replace('  ', '')
                     listaNacionalidades.append(str(row[i]))
                     idNum += 1
      rowNum += 1
   return listaNacionalidades   


connection = None
cursor = None

def selectPlayer(player):
    listaNacionalidades=listaNacionalidade
    try:
        connection = psycopg2.connect(user="is",
                                    password="is",
                                    host="db-rel",
                                    database="is")

        cursor = connection.cursor()

        cursor.execute("SELECT * from players where name like ({})".format(player))

        result = cursor.fetchall()
        
        for row in result:
            print("\n   Name = ", row[0])
            print("   Age = ", row[1])
            print("   Overall = ", row[2])
            x = '{ "Name":"'+row[0]+'", "Age":"'+row[1]+'", "Overall":"'+row[2]+'"}'
            data = json.loads(x)
            
            for pais in range(len(listaNacionalidades)):
                if (str(row[3]) == ('{' + str(pais) + '}')):
                    print("   Nationality = ", ('{' + str(listaNacionalidades[pais]) + '}'))
                    y='{ "Nationality":"'+str(listaNacionalidades[pais])+'"}'
                    break

            data.update(y)      

    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    finally:
        if connection:
            cursor.close()
            connection.close()

    return data



PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

if __name__ == "__main__":
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)

    with SimpleXMLRPCServer(('0.0.0.0', PORT), requestHandler=RequestHandler) as server:
        server.register_introspection_functions()

       # def signal_handler(signum, frame):
        #    print("received signal")
       #     server.server_close()

            # perform clean up, etc. here...
        #    print("exiting, gracefully")
        #    sys.exit(0)

        # signals
        #signal.signal(signal.SIGTERM, signal_handler)
        #signal.signal(signal.SIGHUP, signal_handler)
        #signal.signal(signal.SIGINT, signal_handler)

        # register both functions

        server.register_function(is_even, "iseven")
        server.register_function(selectPlayer,"select_player") # player - string do nome de um jogador
        server.register_function(selectPlayersFromOverall) # overall - inteiro do overall de um jogador

        # start the server
        print(f"Starting the RPC Server in port {PORT}...")
        server.serve_forever()
