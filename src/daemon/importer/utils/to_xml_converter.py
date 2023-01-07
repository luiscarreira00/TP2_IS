import csv
import xml.dom.minidom as md
import xml.etree.ElementTree as ET
import csv

from utils.reader import CSVReader
from entities.country import Country
from entities.team import Team
from entities.player import Player


class CSVtoXMLConverter:

    listaNacionalidades = [list]


    inputFile = csv.reader(open('/csv/fifa.csv', encoding="utf8"))
    inputFile2 = csv.reader(open('/csv/fifa.csv', encoding="utf8"))
    outputData = open('/shared/output/fifa.xml', 'w', encoding="utf8")
    outputData2 = open('/shared/output/fifa.xml', 'a', encoding="utf8")
    outputData.write('<?xml version="1.0" encoding="utf-8" standalone="yes"?>' + "\n")
    # there must be only one top-level tag
    outputData.write('<Players_List>' + "\n")

    rowNum = 0
    idNum = 1
    outputData.write('  <Nationalities>' + "\n")
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
                        outputData.write('    <' + str(tags[i]) + ' id ="' + str(idNum) + '"' + '>' + str(row[i]) + '</' + str(tags[i]) + '>' + "\n")
                        listaNacionalidades.append(str(row[i]))
                        idNum += 1
        rowNum += 1
    outputData.write('  </Nationalities>' + "\n")

    outputData.close()


    rowNum2 = 0

    for row2 in inputFile2:
        if rowNum2 == 0:
            tags = row2
            for i in range(len(tags)):
                tags[i] = tags[i].replace('   ', '')
        else:
            outputData2.write('  <Player>' + "\n")
            for i in range(len(tags)):
                if (i == 1 or i == 3 or i == 8 ) :
                    # replace ampersand with character entity.
                    row2[i] = row2[i].replace('&', '&amp;')
                    row2[i] = row2[i].replace('  ', '')
                    outputData2.write('    <' + str(tags[i]) + '>' + str(row2[i]) + '</' + str(tags[i]) + '>' + "\n")

                if (i == 7) :
                    id=0
                    # replace ampersand with character entity.
                    row2[i] = row2[i].replace('&', '&amp;')
                    row2[i] = row2[i].replace('  ', '')
                    for country in range(len(listaNacionalidades)):
                        if (str(row2[i]) == listaNacionalidades[country]):
                            id= (country)

                    outputData2.write('    <' + str(tags[i]) + '>' + str(id) + '</' + str(tags[i]) + '>' + "\n")

            outputData2.write('  </Player>' + "\n")
        rowNum2 += 1

    outputData2.write('</Players_List>' + "\n")
    outputData2.close()

