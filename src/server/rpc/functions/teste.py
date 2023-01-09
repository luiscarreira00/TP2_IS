import psycopg2
import csv
from xml.etree.ElementTree import ElementTree

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

def selectPlayer(player,listaNacionalidades):
    try:
        connection = psycopg2.connect(user="is",
                                    password="is",
                                    host="localhost",
                                    port="15432",
                                    database="is")

        cursor = connection.cursor()

        
        cursor.execute("""SELECT xpath('//Player/Name[text()="%s"]/text()',"xml"),
                                 xpath('//Player/Name[text()="%s"]/../Age/text()',"xml"),
                                 xpath('//Player/Name[text()="%s"]/../Overall/text()',"xml"),
                                 xpath('//Player/Name[text()="%s"]/../Nationality/text()',"xml")
        
        
        from "imported_documents"  where "file_name" ='fifaPlayers'; """ % (player, player, player, player))


        result = cursor.fetchall()
        
        for row in result:
            print("\n   Name = ", row[0])
            print("   Age = ", row[1])
            print("   Overall = ", row[2])
            
            for pais in range(len(listaNacionalidades)):
                if (str(row[3]) == ('{' + str(pais) + '}')):
                    print("   Nationality = ", ('{' + str(listaNacionalidades[pais]) + '}'))
                    break  

    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)

    finally:
        if connection:
            cursor.close()
            connection.close()

    return "Jogador listado com sucesso!"







def selectPlayersFromOverall(overall):
    try:
        connection = psycopg2.connect(user="is",
                                    password="is",
                                    host="localhost",
                                    port="15432",
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







def countPlayersFromNationality(nationality,listaNacionalidades):
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







menuOptions = {
    1: 'Listar jogador',
    2: 'Listar jogadores de determinado overall',
    3: 'Saber quantos jogadores existem de determinado overall',
    4: 'Saber quantos jogadores existem de determinada nacionalidade',
    5: 'Listar jogadores com overall entre determinados valores',
    6: 'Listar jogadores com overall e idade entre determinados valores',
    0: 'Sair do programa',
}



def menu(option,*args):
    if option == 1:
        jogador = input("Insira o nome do jogador pelo qual procura: ")
        return  selectPlayer(jogador)
    elif option == 2:
        overall = input("Insira o overall dos jogadores: ")
        return  selectPlayersFromOverall(overall)
    elif option == 3:
        overall = input("Insira o overall dos jogadores: ")
        return  countPlayersFromOverall(overall)
    elif option == 4:
        nationality = input("Insira a nacionalidade dos jogadores: ")
        return  countPlayersFromNationality(nationality)
    elif option == 5:
        overall1 = input("Insira o overall mínimo: ")
        overall2 = input("Insira o overall máximo: ")
        return  selectPlayersBetweenOverall(overall1, overall2)
    elif option == 6:
        overall1 = input("Insira o overall mínimo: ")
        overall2 = input("Insira o overall máximo: ")
        idade1 = input("Insira a idade mínima: ")
        idade2 = input("Insira a idade máxima: ")
        return  selectPlayersBetweenOverallAndAge(overall1, overall2, idade1, idade2)
    elif option == 0:
        print('Adeus!')
        exit()
    else:
        print('Opção invalida, por favor escolha uma opção entre 1 a 6')

opcao=100

while (opcao != 0):
    print("\n\n\nBem vindo á Base de Dados de jogadores do FIFA23!")
    for key in menuOptions.keys():
        print(key, '--', menuOptions[key])
    opcao = int(input('Introduz a opcao pretendida: '))
    menu(opcao)

