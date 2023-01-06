class Merge:
    import xarray as xr
    from datetime import datetime

    def __init__(self, arquivo=None):
        if arquivo!= None:
            self.dataset =arquivo
    
    def download(self, path_save, year_start=2000, year_end=datetime.now().year, to="original"):
        import datetime
        import requests

        total = (year_end-year_start)*365
        cont=0
        def download_file(url, endereco, nome):
            # acessa o site
            resposta = requests.get(url)
            # Acessa o conteúdo e salva em um arquivo
            if resposta.status_code == requests.codes.OK:
                with open(endereco + f'/{nome}.grip2', 'wb') as novo:
                    novo.write(resposta.content)
            else:
                resposta.raise_for_status()

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
                                    nome=f'MERGE_CPTEC{time.year}0{time.month}0{time.day}')
                            else:
                                print(
                                    f'http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/DAILY/{time.year}/{time.month}/'
                                    f'MERGE_CPTEC_{time.year}{time.month}0{time.day}.grib2')
                                download_file(
                                    url=f'http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/DAILY/{time.year}/{time.month}/'
                                        f'MERGE_CPTEC_{time.year}{time.month}0{time.day}.grib2',
                                    endereco=f'{path_save}',
                                    nome=f'MERGE_CPTEC{time.year}{time.month}0{time.day}')
                                print(f'Foi a data {time.date()}')
                        else:  # se pegamos dias maioress que 9
                            if time.month < 10:  # Adicionamos 0 também
                                download_file(
                                    url=f'http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/DAILY/{time.year}/0{time.month}/'
                                        f'MERGE_CPTEC_{time.year}0{time.month}{time.day}.grib2',
                                    endereco=f'{path_save}',
                                    nome=f'MERGE_CPTEC{time.year}0{time.month}{time.day}')
                            else:
                                download_file(
                                    url=f'http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/DAILY/{time.year}/{time.month}/'
                                        f'MERGE_CPTEC_{time.year}{time.month}{time.day}.grib2',
                                    endereco=f'{path_save}',
                                    nome=f'MERGE_CPTEC{time.year}{time.month}{time.day}')
                    except:
                        print('erro')
                    print((cont/total)*100)
        if to != "original":
            # Want save the data in other extension that no grip2
            escrever=0
