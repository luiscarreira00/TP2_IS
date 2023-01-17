import asyncio
import time
import uuid
import psycopg2

import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

from utils.to_xml_converter import CSVtoXMLConverter

listaFicheirosConvertidos = []

def get_csv_files_in_input_folder():
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(CSV_INPUT_PATH) for f in filenames if
            os.path.splitext(f)[1] == '.csv']

def generate_unique_file_name(directory):
    return f"{directory}/fifa.xml"

def convert_csv_to_xml():
    CSVtoXMLConverter()

class CSVHandler(FileSystemEventHandler):
    def __init__(self, input_path, output_path):
        self._output_path = output_path
        self._input_path = input_path

        # generate file creation events for existing files
        for file in [os.path.join(dp, f) for dp, dn, filenames in os.walk(input_path) for f in filenames]:
            event = FileCreatedEvent(os.path.join(CSV_INPUT_PATH, file))
            event.event_type = "created"
            self.dispatch(event)

    async def convert_csv(self, csv_path):
        # here we avoid converting the same file again
        # !TODO: check converted files in the database
        if csv_path in await self.get_converted_files():
            return

        print(f"new file to convert: '{csv_path}'")

        # we generate a unique file name for the XML file
        xml_path = generate_unique_file_name(self._output_path)

        # we do the conversion
        # !TODO: once the conversion is done, we should updated the converted_documents tables
        convert_csv_to_xml()
        print(f"new xml file generated: '{xml_path}'")

        connection = None
        cursor = None

        try:
            connection = psycopg2.connect(user="is",
                                        password="is",
                                        host="db-xml",
                                        database="is")

            cursor = connection.cursor()
           

        
            cursor.execute("INSERT INTO converted_documents (src, file_size, dst) VALUES (%s, %s, %s);", (csv_path, os.stat(xml_path).st_size , xml_path))

            connection.commit()
            
                

        # !TODO: we should store the XML document into the imported_documents table

            cursor.execute("INSERT INTO imported_documents (file_name, xml, estado) VALUES (%s, %s, 'imported');", (csv_path, xml_path))

            connection.commit()

        except (Exception, psycopg2.Error) as error:
                    print("Failed to fetch data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()

    async def get_converted_files(self):
        # !TODO: you should retrieve from the database the files that were already converted before


        connection = None
        cursor = None

        try:
            connection = psycopg2.connect(user="is",
                                        password="is",
                                        host="db-xml",
                                        database="is")

            cursor = connection.cursor()

        
            cursor.execute("SELECT src from converted_documents")


            result = cursor.fetchall()
            
            for file in result:
                listaFicheirosConvertidos.append(file[0])
                
                
        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()

        return listaFicheirosConvertidos

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"):
            asyncio.run(self.convert_csv(event.src_path))


if __name__ == "__main__":

    CSV_INPUT_PATH = "/csv"
    XML_OUTPUT_PATH = "/shared/output"

    # create the file observer
    observer = Observer()
    observer.schedule(
        CSVHandler(CSV_INPUT_PATH, XML_OUTPUT_PATH),
        path=CSV_INPUT_PATH,
        recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
