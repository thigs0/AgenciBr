import os
import xarray as xr
import requests
import numpy as np
import pandas as pd
from datetime import datetime as dt
from datetime import date

now = dt.now()
class Merge:
    def __init__(self, file=None):
        if file!= None:
            self.dataset = file
    def __download_file(self, url, endereco, nome):
        # access the site
        resposta = requests.get(url)
        # Get content and save it
        if resposta.status_code == requests.codes.OK:
            with open(endereco + f'/{nome}.grib2', 'wb') as novo:
                novo.write(resposta.content)
        else:
            resposta.raise_for_status()

    def download2(self, path, start_year=2000,start_month=1, start_day=1,
                        end_year=now.year, end_month=now.month, end_day=now.day):
        start_dt = date(start_year, start_month, start_day).strftime('%Y-%m-%d')
        end_dt = date(end_year, end_month, end_day).strftime('%Y-%m-%d')
        files = []
        for i in np.arange(start_dt, end_dt, dtype='datetime64[D]'):
            print(i)
            date_str_format = pd.to_datetime(i).strftime('%Y%m%d')
            self.__download_file(
                    url=f'http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/DAILY/{date_str_format[:-4]}/{date_str_format[4:-2]}/'
                    f'MERGE_CPTEC_{date_str_format}.grib2',
                    endereco=f'{path}',
                    nome=f'MERGE_CPTEC_{date_str_format}')
            files.append(f'{path}/MERGE_CPTEC_{date_str_format}')

        df = xr.open_mfdataset(rf'{path}\*.grib2', engine="cfgrib")
        df.to_netcdf(f"{path}\MERGE_CPTEC_{start_dt}_{end_dt}.nc")
        os.system(rf"rm {path}\*.idx")
        os.system(rf"rm {path}\*.grip2")
      
    def to_netcdf(self, path):
        import xarray as xr
        loc = os.listdir(path)
        for i in loc:
            df = xr.open_dataset(f"{path}/{i}", engine="cfgrib")
            df.to_netcdf(f"{path}/{i[:-6]}.nc")
            os.remove(f"{path}/{i}")
        os.system(f"rm {path}/*.idx")
        df = xr.open_mfdataset(f"{path}/*.nc")
        os.system(f"rm {path}/*.idx")
