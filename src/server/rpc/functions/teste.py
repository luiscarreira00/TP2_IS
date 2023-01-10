import psycopg2
import csv
from xml.etree.ElementTree import ElementTree
import json

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
     
        cursor.execute("SELECT * from players where name like ("+player+")")

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







def selectPlayersFromOverall(overall):
    try:
        connection = psycopg2.connect(user="is",
                                    password="is",
                                    host="db-rel",
                                    database="is")

        cursor = connection.cursor()

        
        
        cursor.execute("""SELECT xpath('//Player/Overall[text()="%s"]/../Name/text()',"xml")
        
        
        from "imported_documents"  where "file_name" ='fifaPlayers'; """ % overall)


        result = cursor.fetchall()
        
        for row in result:
            print("\n\n   Name = ", row[0] )
            

    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    finally:
        if connection:
            cursor.close()
            connection.close()

    return "Jogador listado com sucesso!"




def countPlayersFromOverall(overall):
    try:
        connection = psycopg2.connect(user="is",
                                    password="is",
                                    host="localhost",
                                    port="15432",
                                    database="is")

        cursor = connection.cursor()

        
        
        cursor.execute("""SELECT xpath('count(//Player/Overall[text()="%s"])',"xml")
        
        
        from "imported_documents"  where "file_name" ='fifaPlayers'; """ % overall)


        result = cursor.fetchall()
        
        for row in result:
            print("\n\n   Número de jogadores = ", row[0] )
            

    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    finally:
        if connection:
            cursor.close()
            connection.close()

    return "Jogador listado com sucesso!"







def countPlayersFromNationality(nationality):
    listaNacionalidades=listaNacionalidade
    try:
        connection = psycopg2.connect(user="is",
                                    password="is",
                                    host="localhost",
                                    port="15432",
                                    database="is")

        cursor = connection.cursor()

        for pais in range(len(listaNacionalidades)):
                if (nationality == listaNacionalidades[pais]):
                    nationality = pais
                    break  

        
        
        cursor.execute("""SELECT xpath('count(//Player/Nationality[text()="%s"])',"xml")
        
        
        from "imported_documents"  where "file_name" ='fifaPlayers'; """ % nationality)


        result = cursor.fetchall()
        
        for row in result:
            print("\n\n   Número de jogadores = ", row[0])
            

    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    finally:
        if connection:
            cursor.close()
            connection.close()

    return "Jogador listado com sucesso!"







def selectPlayersBetweenOverall(overall1, overall2):
    try:
        connection = psycopg2.connect(user="is",
                                    password="is",
                                    host="localhost",
                                    port="15432",
                                    database="is")

        cursor = connection.cursor()

        
        
        cursor.execute("""SELECT xpath('//Player[Overall>="%s" and Overall<="%s"]/Name/text()',"xml"),
                                xpath('//Player[Overall>="%s" and Overall<="%s"]/Overall/text()',"xml")
        
        
        from "imported_documents"  where "file_name" ='fifaPlayers'; """ % (overall1, overall2, overall1, overall2))


        result = cursor.fetchall()
        
        for row in result:
            print("\n\n   Name = ", row[0] )
            print("\n\n   Overall = ", row[1] )
            

    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    finally:
        if connection:
            cursor.close()
            connection.close()

    return "Jogador listado com sucesso!"



    
def selectPlayersBetweenOverallAndAge(overall1, overall2, age1, age2):
    try:
        connection = psycopg2.connect(user="is",
                                    password="is",
                                    host="localhost",
                                    port="15432",
                                    database="is")

        cursor = connection.cursor()

        
        
        cursor.execute("""SELECT xpath('//Player[Overall>="%s" and Overall<="%s" and Age>="%s" and Age<="%s"]/Name/text()',"xml"),
                                 xpath('//Player[Overall>="%s" and Overall<="%s" and Age>="%s" and Age<="%s"]/Overall/text()',"xml"),
                                 xpath('//Player[Overall>="%s" and Overall<="%s" and Age>="%s" and Age<="%s"]/Age/text()',"xml")
        
        
        from "imported_documents"  where "file_name" ='fifaPlayers'; """ % (overall1, overall2, age1, age2, overall1, overall2, age1, age2, overall1, overall2, age1, age2))


        result = cursor.fetchall()
        
        for row in result:
            print("\n\n   Name = ", row[0] )
            print("\n\n   Overall = ", row[1] )
            print("\n\n   Age = ", row[2] )
            

    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    finally:
        if connection:
            cursor.close()
            connection.close()

    return "Jogador listado com sucesso!"


