import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta



class Trat_INEMET:
    def __init__(self, path, encoding='utf-8', sep=';', type='none'):
        '''

        :param path:
        :param encoding:
        :param sep:
        :param type: Tipo de dados que tem no arquivo t_maxmin: Temperatura máxima e mínima
        '''
        def linha_inicio_df(arquivo):
            '''Abre o arquivo porém pula linhas em branco que por padrão são 4
            No inicio a primeira linha é transformada em head. Portanto, somamos+4+1'''
            df = pd.read_csv(arquivo, sep=';', on_bad_lines='skip',
                             encoding='latin-1')
            return len(df) + 2

        def find_cod(df):
            '''
            Encontra o código da estação no dataframe
            '''
            line_codigo = 0

            while True:
                temp = str(df.loc[line_codigo]).split()
                # se código aparece na linha, sabemos que é esta
                if 'Codigo' in temp:
                    ind = temp.index('Codigo')
                    temp = temp[ind + 2]
                    return temp
                line_codigo += 1

        def type_data(x):
            if x == ("t_maxmin" or "pr"): # Caso o usuário tenha digitado a variável
                return x
            df = pd.read_csv(path,skiprows=linha_inicio_df(path), nrows=50, on_bad_lines='skip')
            temp = str.lower(''.join(df.columns))
            if  'temperatura' in temp:
                if "minima" and 'maxima' in temp:
                    del df
                    del temp
                    return 't_maxmin'
                del df
                del temp
                return 't_med'
            if 'precipitacao':
                del df
                del temp
                return 'pr'

        def date(linha):

            '''
                        Encontra a altura da estação no dataframe
                        '''
            import datetime
            df = self.dataframe
            df = df.iloc[linha,0]
            df = datetime.datetime.strptime(df, '%Y-%m-%d')
            return df

        def coords(path):
            df = pd.read_csv(path, nrows=linha_inicio_df(path), index_col=False,
                                           on_bad_lines='skip', encoding='latin-1')
            line_codigo = 0
            cord = {'latitude':'', 'longitude':''}
            while True:
                temp = str(df.loc[line_codigo]).split()
                # se código aparece na linha, sabemos que é esta
                if 'Latitude:' in temp:
                    ind = temp.index('Latitude:')
                    temp = temp[ind+1]
                    cord['latitude'] = temp

                    line_codigo += 1
                    temp = str(df.loc[line_codigo]).split()
                    ind = temp.index('Longitude:')
                    temp = temp[ind + 1]
                    cord['longitude'] = temp
                    return cord
                line_codigo += 1

        def alt(path):
            df = pd.read_csv(path, nrows=linha_inicio_df(path), index_col=False,
                             on_bad_lines='skip', encoding='latin-1')
            line_codigo = 0
            while True:
                temp = str(df.loc[line_codigo]).split()
                # se código aparece na linha, sabemos que é esta
                if 'Altitude:' in temp:
                    ind = temp.index('Altitude:')
                    temp = temp[ind + 1]
                    return temp
                line_codigo+=1

        def situacao(path):
            df = pd.read_csv(path, nrows=linha_inicio_df(path), index_col=False,
                             on_bad_lines='skip', encoding='latin-1')
            line_codigo = 0
            while True:
                temp = str(df.loc[line_codigo]).split()
                # se código aparece na linha, sabemos que é esta
                if 'Situacao:' in temp:
                    ind = temp.index('Situacao:')
                    temp = temp[ind + 1]
                    return temp
                line_codigo += 1

        def cidade(path):
            df = pd.read_csv(path, nrows=linha_inicio_df(path), index_col=False,
                             on_bad_lines='skip', encoding='latin-1')
            line_codigo = 0
            while True:
                temp = str(df.loc[line_codigo]).split()
                # se código aparece na linha, sabemos que é esta
                if 'Nome:' in temp:
                    ind = temp.index('Nome:')
                    temp = temp[ind + 1]
                    return temp
                line_codigo += 1

        def dataframe():
            if self.type_data =='t_maxmin':
                df = pd.read_csv(path, encoding=encoding,
                                         index_col=False, sep=sep, skiprows=linha_inicio_df(path))
                df.columns = ['Data', 'max','min','']
                df = df.drop(columns='')

                return df
            if self.type_data == 'pr':
                df = pd.read_csv(path, encoding=encoding,
                                 index_col=False, sep=sep, skiprows=linha_inicio_df(path))
                df.columns = ['Data', 'pr','']
                df = df.drop(columns='')

                return df

        import pandas as pd
        self.type_data = type_data(type)
        self.dataframe = dataframe()
        self.codigo = find_cod(pd.read_csv(path, nrows=linha_inicio_df(path), index_col=False,
                                           on_bad_lines='skip', encoding='latin-1'))
        self.startdate = date(0)
        self.enddate = date(len(self.dataframe)-1)
        self.coord = coords(path)
        self.altitude = alt(path)
        self.situacao = situacao(path)
        self.cidade = cidade(path)
        self.columns = self.dataframe.columns
        self.len = len(self.dataframe)
    def show(self):
        print(self.dataframe)

    def dados_faltantes(self, type='relative',arredondar=2):
        import math
        # se estamos tratando de temperatura
        #colunas sobre datas
        if self.type_data == 'temperatura':
            cont_semdados = 0
            for k in range(len(self.dataframe)):
                if math.isnan(self.dataframe[self.columns[1]][k]):
                    cont_semdados += 1

            if type == 'relative':
                return round((cont_semdados / len(self.dataframe)) * 100,arredondar)
            elif type == 'absolute':
                return round(cont_semdados, arredondar)
            else:
                raise 'Selecione um dos dois tipos possiveis, "relative" ou "absolute"'

        # se estamos tratando de precipitação
        elif self.type_data == 'pr':
            cont_semdados = 0
            for k in range(len(self.dataframe)):
                if math.isnan(self.dataframe['PRECIPITACAO TOTAL, DIARIO(mm)'][k]):
                    cont_semdados += 1
            if type == 'relative':
                return round((cont_semdados / len(self.dataframe)) * 100, arredondar)
            elif type == 'absolute':
                return round(cont_semdados, arredondar)
            else:
                raise 'Selecione um dos dois tipos possiveis, "relative" ou "absolute"'

    def identificador(self, path):

        '''Path é o caminho até a pasta com os aquivos das estações'''

        import pandas as pd
        import os

        codigo = []
        lat=[]
        lon=[]
        # vai pegar o código e armazenar na variavel codigo
        for k in os.listdir(path):
            df = Trat_INEMET(path + '/' + k)
            codigo.append(df.codigo)
            lat.append(df.coord['latitude'])
            lon.append(df.coord['longitude'])

        return pd.DataFrame(list(zip(codigo,lat,lon)),columns=['Código','Latitude','Longitude'])

    def identificador_distancia(self, path, start_alt=0, stop_alt=1000, len=3,
                                limite_distancia=1000, return_distance=False, alt=True):
        '''
        Para o bom funcionamento, o primeiro termo é um Dataframe que precisa conter:
        colunas com 'Altitude', 'Latitude', 'Longitude' e 'Identificador_Estação'. Este último sendo um índice que
        você usa para distinguir estações.

        'a' é o código da estação que usaremos para encontrar o
          'Identificador_Estação' da estação que você está considando como referência
        'star_alt' é o valor mínimo de altura
        'Stop_alt' é o valor máximo de altura
        'len' é o número de estações que você quer coletar que sejam perto

        A função retorna uma lista com os índices das estações mais próximas em ordem crescente
        '''

        def find_cod(df):
            '''
            Encontra o código da estação no dataframe
            '''
            line_codigo = 0
            while True:
                temp = str(df.loc[line_codigo]).split()
                # se código aparece na linha, sabemos que é esta
                if 'Código' in temp:
                    ind = temp.index('Código')
                    temp = temp[ind + 2].split(':')
                    return int(temp[1])
                line_codigo += 1

        def haversine(lon1, lat1, lon2, lat2):

            """
            Calculate the great circle distance in kilometers between two points
            on the earth (specified in decimal degrees)
            """
            # convert decimal degrees to radians
            lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

            # haversine formula
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a3 = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * asin(sqrt(a3))
            r = 6371  # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
            return c * r

        from math import sqrt, cos, sin, asin, radians, inf
        import os
        l_e_p = []
        i_e_p = []
        tm_l =0
        identificador = Trat_INEMET(path + '/' + (os.listdir(path)[0]), encoding='latin-1',
                                    ).identificador(path)
        if not alt:
            altitude = 1

            '''Ajusta tamanho das estações'''
            for k in range(len + 2):
                tm_l+=1
                l_e_p.append(inf)
                i_e_p.append('Nan')

            if self.codigo in list(identificador['Código']):
                # indica a estação de referencia como a
                a = list(identificador['Código']).index(self.codigo)

                a = identificador['Identificador_Estação'][a]

                for b in identificador['Identificador_Estação']:
                    cont = 0
                    if a != b and stop_alt >= altitude >= start_alt:  # todos os valores menos o próprio
                        '''vereremos as estações e veremos as 3 mais próximas
                        cidade1 é a cidade que trataremos os dados
                        cidade2 é a cidade que analisaremos '''

                        lat1, lon1 = identificador['Latitude'][a], identificador['Longitude'][a]
                        lat2, lon2 = identificador['Latitude'][b], identificador['Longitude'][b]
                        distancia = haversine(lon1, lat1, lon2, lat2)


                        '''Se alguma cidade for mais próxima do que a que consta na lista, esta a substitui
                        Está em ordem crescente'''
                        for z in range(tm_l - 3):  # todas as linhas menos as 2 últimas
                            if l_e_p[z] > distancia and distancia <= limite_distancia:
                                for c in range(z + 1, tm_l):
                                    if l_e_p[c] > l_e_p[z]:
                                        l_e_p[c] = l_e_p[z]
                                        i_e_p[c] = i_e_p[z]
                                        break
                                i_e_p[z] = identificador['Identificador_Estação'][b]
                                l_e_p[z] = distancia
                                break

                if return_distance is True:
                    return l_e_p[0:len]
                else:
                    return i_e_p[0:len]
        else:
            '''Ajusta tamanho das estações'''
            for k in range(len + 2):
                l_e_p.append(inf)
                i_e_p.append('Nan')

                # indica a estação de referencia como a
                a = identificador['Código'].index(self.codigo)
                a = identificador['Identificador_Estação'][a]

                for b in identificador['Identificador_Estação']:
                    cont = 0
                    if a != b and stop_alt >= (
                            identificador['Altitude'][b]) >= start_alt:  # todos os valores menos o próprio
                        '''vereremos as estações e veremos as 3 mais próximas
                        cidade1 é a cidade que trataremos os dados
                        cidade2 é a cidade que analisaremos '''

                        lat1, lon1 = identificador['Latitude'][a], identificador['Longitude'][a]
                        lat2, lon2 = identificador['Latitude'][b], identificador['Longitude'][b]
                        distancia = haversine(lon1, lat1, lon2, lat2)

                        '''Se alguma cidade for mais próxima do que a que consta na lista, esta a substitui
                        Está em ordem crescente'''

                        for z in range(len(l_e_p) - 3):  # todas as linhas menos as 2 últimas
                            if l_e_p[z] > distancia and distancia <= limite_distancia:
                                for c in range(z + 1, len(l_e_p)):
                                    if l_e_p[c] > l_e_p[z]:
                                        l_e_p[c] = l_e_p[z]
                                        i_e_p[c] = i_e_p[z]

                                        break
                                i_e_p[z] = identificador['Identificador_Estação'][b]
                                l_e_p[z] = distancia

                                break
            print(l_e_p)
            if return_distance is True:
                return l_e_p[0:len]
            else:
                return i_e_p[0:len]
    def plot(self, title, xlabel, ylabel):
        from matplotlib import pyplot as plt
        from datetime import datetime
        colum = self.dataframe.columns
        if self.type_data == 'temperatura':
            y = self.dataframe[colum[1]]
            x = self.dataframe[colum[0]]
            temp =[]
            for k in x:
                temp.append(datetime.strptime(k,'%Y-%m-%d'))
            x = temp
            plt.plot(x,y,linewidth=0.1)
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()

        elif self.type_data == 'pr':
            y = self.dataframe[colum[1]]
            x = self.dataframe[colum[0]]
            temp = []
            for k in x:
                temp.append(datetime.strptime(k, '%Y-%m-%d'))
            x = temp
            plt.bar(x,y)
            #plt.plot(x,y)
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.tight_layout()

            plt.show()

    def format1(self, virgula_para_ponto=True, crescente=True):
        '''dataframe_organizar é o arquivo dataframe que será organizado; nos dados faltantes deve contér 'sd'
                         O INDEX deve ser a data em ano e mês, cada coluna coresponder à um dia do mês conforme e
                         o nome da coloca de datas deve se chamar 'Data' como modelo abaixo:

                         Data      dia1     dia2    dia3    dia4    dia5    dia6    dia7 ...
                         1993     0.1      0.3     0.7     0.8     0.6     0.4     0.1
                         1993     0.2      0.9     0.5     0.2     0.1     1.9     9.1
                         1993     0.7      0.2     0.9     0.8     0.7     0.4     0.1
                         .
                         .
                         .


                        Ano final é até que ano deve ser organizado
                        E deixamos da forma:

                        Data    precipitação
                        1997-07-01  0.1
                        1997-07-02  0.3
                        ....
                        ...
                        ...
                        2020-01-01  0.3
                        2020-01-02  0.0
                        '''
        import pandas as pd
        if self.type_data == 'pr':
            from datetime import datetime

            # Organizando o arquivo pela datas do menor até o maior
            df_ordenado = self.dataframe

            df_ordenado['Data Medicao'] = pd.to_datetime(df_ordenado['Data Medicao'], format="%Y-%m-%d")
            df_ordenado = df_ordenado.drop_duplicates(subset='Data Medicao')
            if virgula_para_ponto:
                df_ordenado = df_ordenado.replace({',': '.'}, regex=True)
                df_ordenado = df_ordenado.reset_index()
                df_ordenado = df_ordenado.drop(columns='index')
                self.dataframe = df_ordenado
            if not crescente:
                df_ordenado = df_ordenado.rename(columns={'Data Medicao': 'Data'})
                self.dataframe = df_ordenado.sort_values(by=['Data'], ascending=True)

            Data = []
            prec = []
            # indução
            colum = self.dataframe.columns
            for linha in range(len(self.dataframe)):
                Data.append(self.dataframe[colum[0]][linha])
                prec.append(self.dataframe[colum[1]][linha])

            df = pd.DataFrame(list(zip(Data, prec)), columns=['Data', 'precipitação'])
            return df
        elif self.type_data == 't_maxmin':
            from datetime import datetime

            # Organizando o arquivo pela datas do menor até o maior
            df_ordenado = self.dataframe

            df_ordenado['Data Medicao'] = pd.to_datetime(df_ordenado['Data Medicao'], format="%Y-%m-%d")
            df_ordenado = df_ordenado.drop_duplicates(subset='Data Medicao')
            if virgula_para_ponto:
                df_ordenado = df_ordenado.replace({',': '.'}, regex=True)
                df_ordenado = df_ordenado.reset_index()
                df_ordenado = df_ordenado.drop(columns='index')
                df_ordenado = df_ordenado.drop(['Unnamed: 3'],axis=1)
                self.dataframe = df_ordenado
            if not crescente:
                df_ordenado = df_ordenado.rename(columns={'Data Medicao': 'Data Medicao'})
                df_ordenado = df_ordenado.drop(['Unnamed: 3'],axis=1)
                self.dataframe = df_ordenado.sort_values(by=['Data Medicao'], ascending=True)

    def to_netcdf4(self, local=''):
        import xarray as xr
        if self.type_data == 'precipitacao':
            df = self.format1(crescente=False)

            df = df.rename(columns={'precipitação': 'pr'})  # verificar se é este o nome
            df = df.rename(columns={'Data': 'time'})
            # pr para numero
            temp = []
            for k in df['pr']:
                temp.append(float(k))
            df['pr'] = temp[:]

            # criando latitude e longitude com valor (0,0)
            lat = [float(self.coord['latitude'])] * len(df['pr'])
            lon = [float(self.coord['longitude'])] * len(df['pr'])
            df['lat'] = lat
            df['lon'] = lon
            # abrindo o df com o xarray
            ds = df.set_index(['time', 'lat', 'lon']).to_xarray()

            ds = xr.Dataset(ds)
            # add variable attribute metadata
            ds.attrs['lat'] = 'Units: °'
            ds.attrs['lon'] = 'Units: °'
            ds.attrs['time'] = 'Data diária'

            return ds.to_netcdf(local+f'/Dados{self.codigo}_D_{self.startdate.year}_{self.enddate.year}.nc')

        elif self.type_data == 'temperatura':
            # remove colunas em branco
            self.format1()

            df = self.dataframe.drop(['TEMPERATURA MINIMA, DIARIA(°C)'], axis=1)

            df = df.rename(columns={'TEMPERATURA MAXIMA, DIARIA(°C)': 'tas'})  # verificar se é este o nome
            df = df.rename(columns={'Data Medicao': 'time'})
            # pr para numero
            temp = []
            for k in df['tas']:
                temp.append(float(k))
            df['tas'] = temp[:]

            # criando latitude e longitude com valor (0,0)
            lat = [float(self.coord['latitude'])] * len(df['tas'])
            lon = [float(self.coord['longitude'])] * len(df['tas'])
            df['lat'] = lat
            df['lon'] = lon
            # abrindo o df com o xarray
            ds = df.set_index(['time', 'lat', 'lon']).to_xarray()

            ds = xr.Dataset(ds)
            # add variable attribute metadata
            ds.attrs['lat'] = 'Units: °'
            ds.attrs['lon'] = 'Units: °'
            ds.attrs['time'] = 'Data diária'

            ds.to_netcdf(local + f'/Dados{self.codigo}_D_{self.startdate.year}_{self.enddate.year}_max.nc')


            # Calcular mínimo
            df = self.dataframe.drop(['TEMPERATURA MAXIMA, DIARIA(°C)'], axis=1)

            df = df.rename(columns={'TEMPERATURA MINIMA, DIARIA(°C)': 'tas'})  # verificar se é este o nome
            df = df.rename(columns={'Data Medicao': 'time'})
            # pr para numero
            temp = []
            for k in df['tas']:
                temp.append(float(k))
            df['tas'] = temp[:]

            # criando latitude e longitude com valor (0,0)
            lat = [float(self.coord['latitude'])] * len(df['tas'])
            lon = [float(self.coord['longitude'])] * len(df['tas'])
            df['lat'] = lat
            df['lon'] = lon
            # abrindo o df com o xarray
            ds = df.set_index(['time', 'lat', 'lon']).to_xarray()

            ds = xr.Dataset(ds)
            # add variable attribute metadata
            ds.attrs['lat'] = 'Units: °'
            ds.attrs['lon'] = 'Units: °'
            ds.attrs['time'] = 'Data diária'

            ds.to_netcdf(local + f'/Dados{self.codigo}_D_{self.startdate.year}_{self.enddate.year}_min.nc')

    def date(self,linha):

        '''
                    Encontra a altura da estação no dataframe
                    '''
        import datetime
        df = self.dataframe
        df = df.iloc[linha, 0]
        df = datetime.datetime.strptime(df, '%Y-%m-%d')
        return df

    def close(self):
        import gc
        gc.collect()

    def ByYear(self,year,var):
        # percorre procurando por ano
        inicio, final= 0,0
        for linha in range(self.len):
            n=0
            l = linha
            if self.date(linha).year == year:
                inicio = linha #linha de inicio
                while self.date(l).year == year and l < self.len-1:
                    l+=1
                final = l
                break
        return np.array(self.dataframe[f'{var}'][inicio:final])

    def rx5day(self, valor=50, retornar='highest_five_day_precipitation_amount_per_time_period', selbyyear=0):
        import datetime
        '''
        :param valor:
        :param retornar:Opções para retornar: highest_five_day_precipitation_amount_per_time_period, que é uma lista 0 é o numero e 1 é o mês
        ; number_of_5day_heavy_precipitation_periods_per_time_period
        :return:
        '''

        # deixa apenas os dados de precipitação
        ds = self.dataframe
        number_of_5day_heavy_precipitation_periods_per_time_period = 0
        lista = []
        maior = {0: 0, 1: 0}
        cont = temp = 0
        for linha in range(len(self.dataframe)):
            # percorre as colunas
                # verifica se a data existe, se não, temos um erro
                data = self.date(linha)
                if data.year == selbyyear:
                    #
                    if cont < 5:
                        temp += float(ds.iloc[linha,1])
                        cont += 1
                    # se passou 5 dias, armazenamos na lista
                    elif cont == 5:
                        lista.append({'num': temp, 'month': (data+datetime.timedelta(days=-5))})
                        cont = 0
                        temp = 0

        # depois de criar uma lista, iremos percorre ela em busca dos valores
        for k in lista:
            # se teve um excedente de chuva acima de um valor
            if k['num'] > valor:
                if k['num'] > maior[0]:
                    maior = {0: k['num'], 1: k['month']}
                #print(k, valor)
                number_of_5day_heavy_precipitation_periods_per_time_period += 1

        if retornar == 'highest_five_day_precipitation_amount_per_time_period':
            return maior
        elif retornar == 'number_of_5day_heavy_precipitation_periods_per_time_period':
            return number_of_5day_heavy_precipitation_periods_per_time_period

    def TX(self,with_x=False):
        from indice import indice
        ind = indice(self.dataframe)
        ind = ind.TX(with_x= with_x, type_data=self.type_data, var='max')
        return ind

    def TN(self, with_x= False):
        from indice import indice
        ind = indice(self.dataframe)
        ind = ind.TN(with_x= with_x, type_data=self.type_data)
        return ind

    def TN90p(self, with_x=False):
        from indice import indice
        ind = indice(self.dataframe)
        ind = ind.TN90p(with_x=with_x)
        return ind

    def TX90p(self, with_x=False):
        from indice import indice
        ind = indice(self.dataframe)
        ind = ind.TX90p(with_x=with_x, type_data=self.type_data)
        return ind


a = Trat_INEMET('/media/thiagosilva/thigs/Projetos/Amazônia/selecionados/INEMET/Dados_INEMET_Convencionais/Temperatura/Manaus/dados_82331_D_1960-01-01_2022-01-01.csv')
#a= Trat_INEMET("/media/thiagosilva/thigs/Projetos/Amazônia/selecionados/INEMET/Dados_INEMET_Convencionais/Precipitação/Manaus/dados_82331_D_1960-01-01_2022-01-01.csv")
print(a.altitude)
x,y = a.TX(with_x=True)
plt.plot(x,y)
plt.show()
