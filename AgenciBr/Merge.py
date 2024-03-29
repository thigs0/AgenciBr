import os
import xarray as xr
class Merge:
    from datetime import datetime

    def __init__(self, arquivo=None):
        if arquivo!= None:
            self.dataset =arquivo
    
    def download(self, path_save, year_start=2000, year_end=datetime.now().year, date=None, to="original"):
        import datetime
        import requests

        total = (year_end-year_start)*360
        cont=0
        def download_file(url, endereco, nome):
            # acessa o site
            resposta = requests.get(url)
            # Acessa o conteúdo e salva em um arquivo
            if resposta.status_code == requests.codes.OK:
                with open(endereco + f'/{nome}.grib2', 'wb') as novo:
                    novo.write(resposta.content)
            else:
                resposta.raise_for_status()
        if ( date != None):
            if ( date.month < 10):
                if ( date.day < 10):
                    download_file(
                    url=f'http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/DAILY/{date.year}/0{date.month}/'
                    f'MERGE_CPTEC_{date.year}0{date.month}0{date.day}.grib2',
                    endereco=f'{path_save}',
                    nome=f'MERGE_CPTEC_{date.year}0{date.month}0{date.day}')
                    if to == "netcdf":
                        df = xr.open_dataset(f"{path_save}/MERGE_CPTEC_{date.year}0{date.month}0{date.day}.grib2", engine="cfgrib")
                        df.to_netcdf(f"{path_save}/MERGE_CPTEC_{date.year}0{date.month}0{date.day}.nc")
                        os.remove(f"{path_save}/MERGE_CPTEC_{date.year}0{date.month}0{date.day}.grib2")
                        os.system(f"rm {path_save}/*.idx")


                else:
                    download_file(
                    url=f'http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/DAILY/{date.year}/0{date.month}/'
                    f'MERGE_CPTEC_{date.year}0{date.month}{date.day}.grib2',
                    endereco=f'{path_save}',
                    nome=f'MERGE_CPTEC_{date.year}0{date.month}{date.day}')
                    if to == "netcdf":
                        df = xr.open_dataset(f"{path_save}/MERGE_CPTEC_{date.year}0{date.month}{date.day}.grib2", engine="cfgrib")
                        df.to_netcdf(f"{path_save}/MERGE_CPTEC_{date.year}0{date.month}{date.day}.nc")
                        os.remove(f"{path_save}/MERGE_CPTEC_{date.year}0{date.month}{date.day}.grib2")
                        os.system(f"rm {path_save}/*.idx")


            else:
                if ( date.day < 10):
                    download_file(
                    url=f'http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/DAILY/{date.year}/{date.month}/'
                    f'MERGE_CPTEC_{date.year}{date.month}0{date.day}.grib2',
                    endereco=f'{path_save}',
                    nome=f'MERGE_CPTEC_{date.year}{date.month}0{date.day}')
                    if to == "netcdf":
                        df = xr.open_dataset(f"{path_save}/MERGE_CPTEC_{date.year}{date.month}0{date.day}.grib2", engine="cfgrib")
                        df.to_netcdf(f"{path_save}/MERGE_CPTEC_{date.year}{date.month}0{date.day}.nc")
                        os.remove(f"{path_save}/MERGE_CPTEC_{date.year}{date.month}0{date.day}.grib2")
                        os.system(f"rm {path_save}/*.idx")
                else:
                    download_file(
                    url=f'http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/DAILY/{date.year}/{date.month}/'
                    f'MERGE_CPTEC_{date.year}{date.month}{date.day}.grib2',
                    endereco=f'{path_save}',
                    nome=f'MERGE_CPTEC_{date.year}{date.month}{date.day}')
                    if to == "netcdf":
                        df = xr.open_dataset(f"{path_save}/MERGE_CPTEC_{date.year}{date.month}{date.day}.grib2", engine="cfgrib")
                        df.to_netcdf(f"{path_save}/MERGE_CPTEC_{date.year}{date.month}{date.day}.nc")
                        os.remove(f"{path_save}/MERGE_CPTEC_{date.year}{date.month}{date.day}.grib2")
                        os.system(f"rm {path_save}/*.idx")
        
        else:
            #all the cases name of file to download
            for ano in range(year_start, year_end):
                for mes in range(1, 13):
                    for dia in range(1, 32):
                        # Criaremos um arquivo datetime com a data dos loops, se não existir, ignora
                        try:
                            # Como o padrão do site é "06" e não "6" ára mês e dia, são conversões
                            if ano == 2000 and mes < 6:
                                break
                            time = datetime.datetime(ano, mes, dia)
                            if time.day < 10:  # adiciona o 0 na frente do marcador mês
                                if time.month < 10:  # Adicionamos 0 também
                                    download_file(
                                        url=f'http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/DAILY/{time.year}/0{time.month}/'
                                            f'MERGE_CPTEC_{time.year}0{time.month}0{time.day}.grib2',
                                        endereco=f'{path_save}',
                                        nome=f'MERGE_CPTEC_{time.year}0{time.month}0{time.day}')
                                else:

                                    download_file(
                                        url=f'http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/DAILY/{time.year}/{time.month}/'
                                            f'MERGE_CPTEC_{time.year}{time.month}0{time.day}.grib2',
                                        endereco=f'{path_save}',
                                        nome=f'MERGE_CPTEC_{time.year}{time.month}0{time.day}')
                            else:  # se pegamos dias maiores que 9
                                if time.month < 10:  # Adicionamos 0 também
                                    download_file(
                                        url=f'http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/DAILY/{time.year}/0{time.month}/'
                                            f'MERGE_CPTEC_{time.year}0{time.month}{time.day}.grib2',
                                        endereco=f'{path_save}',
                                        nome=f'MERGE_CPTEC_{time.year}0{time.month}{time.day}')
                                else:
                                    download_file(
                                        url=f'http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/DAILY/{time.year}/{time.month}/'
                                            f'MERGE_CPTEC_{time.year}{time.month}{time.day}.grib2',
                                        endereco=f'{path_save}',
                                        nome=f'MERGE_CPTEC_{time.year}{time.month}{time.day}')
                            cont+=1
                        except:
                            continue
                    print(f"{round((cont/total)*100)}% concluídos")
            if to == "netcdf":
                loc = os.listdir(path_save)
                for i in loc:
                    df = xr.open_dataset(f"{path_save}/{i}", engine="cfgrib")
                    df.to_netcdf(f"{path_save}/{i[:-6]}.nc")
                    os.remove(f"{path_save}/{i}")
                os.system(f"rm {path_save}/*.idx")
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

    def format2(self):
        self.dataset = self.dataset
