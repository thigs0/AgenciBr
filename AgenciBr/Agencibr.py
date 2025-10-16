import numpy as np
import pandas as pd

class Agencibr():
    def __init__(self, file=None, code=np.nan):
        self.file = file
        self.code = code

    def download(self,path="./teste.csv", code=np.nan, format='csv', tipo_especifico=False, 
                 save_zip=False, state="nan", city="nan"):
        """
        Download the Ana data. Code from https://github.com/joaohuf/Ferramentas_HidroWeb
        Data os stations code etc, from http://telemetriaws1.ana.gov.br/EstacoesTelemetricas.aspx
        :param codigo: Code that Ana use to define each station
        :param format: The format of save .mdb, .txt, .csv
        :param dir: The directory to save the file
        :param tipo_especifico:
        :param save_zip: Save file in zip or not
        :param state: Is the acronym of states, example: SP, RJ, SC
        :return:
        """
        import requests
        from io import BytesIO
        from zipfile import ZipFile, BadZipFile

        # Link onde estão os dados das estações convencionaiss convencionais
        BASE_URL = 'http://www.snirh.gov.br/hidroweb/rest/api/documento/convencionais'
        if code == np.nan:
            raise("Station don't have code")
        
        def unzip_station_data(station_raw_data, dir, tipo_especifico):
            try:
                main_zip_bytes = BytesIO(station_raw_data)
                main_zip = ZipFile(main_zip_bytes)

                for inner_file_name in main_zip.namelist():
                    inner_file_content = main_zip.read(inner_file_name)
                    inner_file_bytes = BytesIO(inner_file_content)
                    if not tipo_especifico:
                        with ZipFile(inner_file_bytes, 'r') as zipObject:
                            zipObject.extractall(dir)
                    elif tipo_especifico in inner_file_name:
                        with ZipFile(inner_file_bytes, 'r') as zipObject:
                            zipObject.extractall(dir)
            except BadZipFile:
                print('No .zip founded')

        # Change the format to Ana format
        if format == 'csv':
            params = {'tipo': 3, 'documentos': code}
            r = requests.get(BASE_URL, params=params)
        elif format == 'txt':
            params = {'tipo': 2, 'documentos': code}
            r = requests.get(BASE_URL, params=params)
        elif format == 'mdb':
            params = {'tipo': 1, 'documentos': code}
            r = requests.get(BASE_URL, params=params)
        else:
            raise "the data format is not csv , mdb or txt"

        # Check if the code exist in Ana file
        if not isinstance(r.content, bytes):
            print(f'Arquivo {code} inválído')
            return

        # if save_zip is true, save zip
        if save_zip:
            print(f'Salvando dados {code} como zip')
            with open(f'{path} estacao_{code}.zip', 'wb') as f:
                f.write(r.content)
        # else, unpack each zip file
        else:
            print(f'Extraindo dados da estação {code} do zip')
            unzip_station_data(r.content, path, tipo_especifico)
     
