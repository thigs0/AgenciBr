import datetime
import os
from typing import List, Any
import pandas as pd
import numpy as np

def completa(lista):
    maior_len = 0
    l=np.array([])
    for k in range(len(lista)): # percorre os índices
        if len(lista[k]) > maior_len:
            maior_len = len(lista[k])
    for k in range(len(lista)):
        if len(lista[k]) < maior_len:
            while len(lista[k]) != maior_len:
                lista[k].append(0)

    return lista


class Ana:
    def __init__(self, arquivo, sep=';', index_col=False, list=False, encoding='latin-1',
                 on_bad_lines='skip', virgula_to_ponto=True, type="pr"):
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

        def linha_inicio_df(arquivo):
            '''Abre o arquivo porém pula linhas em branco que por padrão são 4
            No inicio a primeira linha é transformada em head. Portanto, somamos+4+1'''
            df = pd.read_csv(arquivo, sep=';',
                             encoding='latin-1', on_bad_lines='skip')
            return len(df) + 1 + 4

        def dataset(path):
            df = pd.read_csv(path, skiprows=linha_inicio_df(path), sep=sep, encoding=encoding,
                             index_col=index_col, on_bad_lines=on_bad_lines)
            if virgula_to_ponto:
                temp = []
                for k in df['Data']:
                    temp.append(datetime.datetime.strptime(k, '%d/%m/%Y'))
                df['Data'] = temp.copy()
                df = df.sort_values(by='Data')
                df = df.reset_index()
                return df.replace({',': '.'}, regex=True)
            else:
                df = df.sort_values(by='Date')
                df = df.reset_index()

                return df

        if not list:
            self.dataset = dataset(arquivo)
            self.codigo = find_cod(pd.read_csv(arquivo, nrows=50, index_col=False,
                                               on_bad_lines='skip', encoding='latin-1'))
            self.fonte = pd.read_csv(arquivo, nrows=2, index_col=False,
                                     on_bad_lines='skip', encoding='latin-1')
            self.startdate = self.dataset['Data'][0]  # data_starend(arquivo)[0]
            self.enddate = self.dataset['Data'][len(self.dataset) - 1]
            self.len = len(self.dataset)
            self.type_data = type

        else:
            self.path = arquivo
            self.list = arquivo

    def only_mondata(self, list=False):
        from datetime import datetime
        """" Remove all columns that is not referent of month precipitation and day
        """
        # Caso sejá uma estação
        if list == False:
            df = self.dataset
            lista_meses = ['Data']
            # adicionamos as colunas dos dados
            for k in range(32):
                'Os dados de precipitação são dados com Chuva ou Clima, seguidos ' \
                'da data no mês'
                if k < 10:
                    lista_meses.append(f'Chuva0{k}')
                    lista_meses.append(f'Clima0{k}')
                else:
                    lista_meses.append(f'Chuva{k}')
                    lista_meses.append(f'Clima{k}')
            columns = df.columns
            for a in columns:
                if a not in lista_meses:
                    del df[a]
            self.dataset = df
        # Caso seja uma lista de estações
        elif list == True:
            list_temp = []
            for k in self.list:
                df = k
                lista_meses = ['Data', 'Chuva01', 'Chuva02', 'Chuva03', 'Chuva04', 'Chuva05',
                               'Chuva06', 'Chuva07', 'Chuva08', 'Chuva09', 'Chuva10',
                               'Chuva11', 'Chuva12', 'Chuva13', 'Chuva14', 'Chuva15',
                               'Chuva16', 'Chuva17', 'Chuva18', 'Chuva19', 'Chuva20',
                               'Chuva21', 'Chuva22', 'Chuva23', 'Chuva24', 'Chuva25',
                               'Chuva26', 'Chuva27', 'Chuva28', 'Chuva29', 'Chuva30',
                               'Chuva31']
                columns = df.columns
                for a in columns:
                    if a not in lista_meses:
                        del df[a]
                list_temp.append(df)


        else:
            return 'List é apenas True ou False'
    def sum_month(self):
        # testar
        """Seleciona os dados diários e retorna o aculmulado mensal"""
        import numpy as np
        df = self.format1()
        mes = pd.to_datetime(df['Data'][0]).month  # primeiro mês
        soma = 0
        t = var = np.array([])
        size = len(df)
        ano = pd.to_datetime(df['Data'][0]).year
        for k in range(len(df["Data"])):
            if pd.to_datetime(df["Data"][k]).month != mes:
                if mes == 12:
                    var = np.append(var, soma)
                    soma = 0
                    mes = 1
                    ano += 1
                    t = np.append(t, datetime.datetime(ano, mes, 1))
                    print(f'Se foram {round(100 * k / size, 2)} %')
                else:
                    var = np.append(var, soma)
                    soma = 0
                    mes += 1
                    t = np.append(t, datetime.datetime(ano, mes, 1))
            soma += df['pr'][k]
        return t, var
    def date(self, linha):
        """Retorna a data da linha que você seleciona"""
        from datetime import datetime
        return datetime.strptime(self.dataset['Data'][linha], '%Y/%D/%M')
    def show(self):

        self.only_mondata()
        for k in range(self.len):
            print(self.dataset[k])
    def trat_dados_arimetica(self, path_estations, ano,
                             mes, dia, numero_estacoes=3, start_alt=0, stop_alt=1000, len=3,
                             limite_distancia=1000, return_distance=False, alt=True):
        def IdentificadorEstação_p_codigo(df, identificador_estacao):
            '''Abrimos o arquivo identificador e pegamos o código para o respetivo
            identificador'''
            ind = df['Identificador_Estação'].index(identificador_estacao)
            return df['Código'][ind]

        import pandas as pd

        # importando arquivos
        indices = self.identificador_distancia(path_estations, start_alt=start_alt, stop_alt=stop_alt,
                                               len=len, limite_distancia=limite_distancia,
                                               return_distance=return_distance
                                               , alt=alt)
        # constantes
        var1 = 0
        cont = 1
        k = 0
        while k < numero_estacoes:  # Temos o indice da estação, pegamos o valor de mesma linha nele
            indice_linha = indices[cont]  # indices das estações mais próximas
            try:
                indice_linha = int(indice_linha)

                if type(indice_linha) == int:

                    arquivo = Trat_ANA(
                        f'chuvas_T_'
                        f'{IdentificadorEstação_p_codigo(self.identificador(path_estations), k)}.txt')
                    arquivo = arquivo.dados_to_padrao()
                    # Se a arquivo que estamos olhando, tem a data. Se sim, adicionamos o valor em var1
                    if ano in arquivo[' Ano'] and mes in arquivo['Mês'] and dia in arquivo['Dia']:

                        filtro1 = arquivo[' Ano'] == ano

                        arquivo_1 = arquivo[filtro1]
                        filtro1 = arquivo_1['Mês'] == mes
                        arquivo2 = arquivo_1[filtro1]
                        filtro1 = arquivo2['Dia'] == dia
                        arquivo3 = arquivo2[filtro1]

                        try:
                            float(arquivo3['Precipitação'])
                            var1 += float(arquivo3['Precipitação'])
                            k += 1
                            cont += 1
                        except:  # se o valor é SD
                            cont += 1

                    else:  # se a data não consta
                        cont += 1

                else:
                    cont += 1

            except:
                break

        var = var1 / numero_estacoes

        return var
    def trat_dados_ponderada(self, indices, distancia, estacao_referencia, ano, mes,
                             dia, numero_estacoes=3, P=1):
        '''Indices é o arquivo em dataframe padrão:

        distancia é a distância máxima que a estação pode estar afastada

        ano, mes e dia é referente a data a ser tratada

        número de estações é o número de estações a serem consideradas ao cálculo

        P é o peso que deve ser dado à distância nos cálculos '''
        # importando arquivos
        cont = 1  # contador que pula de estação
        k = 0
        soma_ED = 0
        soma_D = 0
        while k < numero_estacoes:  # Temos o indice da estação, pegamos o valor de mesma linha nele
            indice_linha = indices.iloc[estacao_referencia, cont]
            distancia_linha = distancia.iloc[estacao_referencia, cont]
            try:
                indice_linha = int(indice_linha)
                distancia_linha = float(distancia_linha)

                if type(indice_linha) == int:

                    arquivo = pd.read_csv(
                        f'E:/Dados_clima/Prec/Precipitação_organizado/prec_estacao_SP_{indice_linha}.txt',
                        sep='\t', skiprows=2)
                    # se a arquivo que estamos olhando, tem a data. Se sim, adicionamos o valor em var1
                    if ano in arquivo[' Ano'] and mes in arquivo['Mês'] and dia in arquivo['Dia']:

                        filtro1 = arquivo[' Ano'] == ano

                        arquivo_1 = arquivo[filtro1]
                        filtro1 = arquivo_1['Mês'] == mes
                        arquivo2 = arquivo_1[filtro1]
                        filtro1 = arquivo2['Dia'] == dia
                        arquivo3 = arquivo2[filtro1]

                        try:
                            float(arquivo3['Precipitação'])
                            soma_ED += float(arquivo3['Precipitação']) / (distancia_linha ** P)
                            soma_D += 1 / (distancia_linha ** P)
                            k += 1
                            cont += 1
                        except:  # se o valor é SD
                            cont += 1

                    else:  # se a data não consta
                        cont += 1

                else:
                    raise 'Erro, uma das estações não está como um numero inteiro'
                    cont += 1

            except:
                break

        var = soma_ED / soma_D

        return var
    def identificador(self, path, only_line=50):

        '''Path é o caminho até a pasta com os aquivos das estações'''

        import pandas as pd
        import os

        codigo = []

        for k in os.listdir(path):
            df = pd.read_csv(path + '/' + k, nrows=only_line + 1, encoding='latin-1',
                             on_bad_lines='skip')
            line_codigo = 0
            # encontra a linha que contém o código da estação
            # vai pegar o código e armazenar na variavel codigo

            while True:

                temp = str(df.loc[line_codigo]).split()

                # se código aparece na linha, sabemos que é esta
                if 'Código' in temp:
                    ind = temp.index('Código')
                    temp = temp[ind + 2].split(':')
                    codigo.append(int(temp[1]))
                    break
                line_codigo += 1
        # lendo o arquivo com todas as estações
        ref = pd.read_csv('../estacoes.csv', usecols=['Código', 'Latitude',
                                                      'Longitude', 'X', 'Y']
                          , index_col=False)
        ref = ref[ref['Código'].isin(codigo)]
        ref = ref.reset_index(drop=True)
        ref = ref.reset_index()
        ref = ref.rename(columns={'index': 'Identificador_Estação'})
        return ref
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

        l_e_p = []
        i_e_p = []
        tm_l = 0
        identificador = TratAna(path + '/' + (os.listdir(path)[0]), encoding='latin-1',
                                index_col=False).identificador(path)
        if alt == False:
            altitude = 1

            '''Ajusta tamanho das estações'''
            for k in range(len + 2):
                tm_l += 1
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
            if return_distance is True:
                return l_e_p[0:len]
            else:
                return i_e_p[0:len]
    def dados_to_padrao(self, ano_final='máximo', crescente=True, virgula_para_ponto=False, floats=2):
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
        '''
        import pandas as pd

        # Organizando o arquivo pela datas do menor até o maior
        dataframe_organizar = self.dataset
        if ano_final == 'máximo':
            ano_final = pd.to_datetime(max(self.dataset['Data']), format="%d/%m/%Y").year

        dataframe_organizar['Data'] = pd.to_datetime(dataframe_organizar['Data'], format="%d/%m/%Y")
        df_ordenado = dataframe_organizar
        df_ordenado = df_ordenado.drop_duplicates(subset='Data')
        if virgula_para_ponto:
            df_ordenado = df_ordenado.replace({',': '.'}, regex=True)
        if not crescente:
            df_ordenado = df_ordenado.sort_values(by=['Data'], ascending=True)
        df_ordenado = df_ordenado.reset_index()
        df_ordenado = df_ordenado.drop(columns='index')
        # criando as listas, valores de inicio e parada
        ano_inicial = (min(dataframe_organizar['Data'])).year
        lista = []
        lista_mes30 = [4, 6, 9, 11]
        lista_mes31 = [1, 3, 5, 7, 8, 10, 12]
        lista_bissexto = []

        k = 0  # valor que armazena a posição da linha
        dataframe = {'Ano': '', 'Mês': '', 'Dia': '', 'Precipitação': ''}
        # Algoritmo para ano bissexto
        for c in range(1900, ano_final):
            ano = c
            if (ano % 4 == 0 and ano % 100 != 0) or ano % 400 == 0:
                lista_bissexto.append(c)

        if 1 > 0:
            # Iniciando a organização dos dados
            while ano_inicial <= ano_final and k < len(df_ordenado) - 1:
                # Se o 'Ano inicial' ano que estamos querendo estiver no dataframe ordenado

                if ano_inicial == (
                        df_ordenado['Data'][k]).year:  # como cada linha representa um mês, K é a posição da linha

                    dataframe['Ano'] = (df_ordenado['Data'][k]).year

                    for b in range(1, 13):
                        # Verifica se o mês existe na linha

                        if k == len(df_ordenado['Data']) - 1 or k == len(df_ordenado['Data']):
                            break
                        if b == df_ordenado.iloc[k]['Data'].month:

                            # Verifica se o ano é bissexto
                            if ano_inicial in lista_bissexto:
                                # Se o mês tem 31 dias
                                if b in lista_mes31:
                                    dataframe['Mês'] = b
                                    for c in range(1, 32):
                                        try:
                                            dataframe['Precipitação'] = round(float(df_ordenado.iloc[k, c]), floats)
                                            dataframe['Dia'] = c
                                            lista.append(dataframe.copy())
                                        except:
                                            dataframe['Precipitação'] = 'SD'
                                            dataframe['Dia'] = c
                                            lista.append(dataframe.copy())
                                # Se o mês têm 30 dias
                                elif b in lista_mes30:
                                    dataframe['Mês'] = b
                                    for c in range(1, 31):
                                        try:
                                            dataframe['Precipitação'] = round(float(df_ordenado.iloc[k, c]), floats)
                                            dataframe['Dia'] = c
                                            lista.append(dataframe.copy())
                                        except:
                                            dataframe['Precipitação'] = 'SD'
                                            dataframe['Dia'] = c
                                            lista.append(dataframe.copy())
                                # Se é fevereiro, é bissexto
                                else:
                                    dataframe['Mês'] = b
                                    for c in range(1, 30):
                                        try:
                                            dataframe['Precipitação'] = round(float(df_ordenado.iloc[k, c]), 2)
                                            dataframe['Dia'] = c
                                            lista.append(dataframe.copy())
                                        except:
                                            dataframe['Precipitação'] = 'SD'
                                            dataframe['Dia'] = c
                                            lista.append(dataframe.copy())

                                k += 1
                            else:
                                # Se o mês têm 31 dias
                                if b in lista_mes31:
                                    dataframe['Mês'] = b
                                    for c in range(1, 32):

                                        try:
                                            dataframe['Precipitação'] = round(float(df_ordenado.iloc[k, c]), 2)
                                            dataframe['Dia'] = c
                                            lista.append(dataframe.copy())
                                        except:
                                            dataframe['Precipitação'] = 'SD'
                                            dataframe['Dia'] = c
                                            lista.append(dataframe.copy())
                                    k += 1
                                # Se o mês têm 30 dias
                                elif b in lista_mes30:
                                    dataframe['Mês'] = b

                                    for c in range(1, 31):
                                        try:
                                            dataframe['Precipitação'] = round(float(df_ordenado.iloc[k, c]), floats)
                                            dataframe['Dia'] = c
                                            lista.append(dataframe.copy())
                                        except:
                                            dataframe['Precipitação'] = 'SD'
                                            dataframe['Dia'] = c
                                            lista.append(dataframe.copy())
                                    k += 1
                                # Se é fevereiro, não bissexto
                                else:
                                    dataframe['Mês'] = b
                                    for c in range(1, 29):
                                        try:
                                            dataframe['Precipitação'] = round(float(df_ordenado.iloc[k, c]), floats)
                                            dataframe['Dia'] = c
                                            lista.append(dataframe.copy())
                                        except:
                                            dataframe['Precipitação'] = 'SD'
                                            dataframe['Dia'] = c
                                            lista.append(dataframe.copy())
                                    k += 1

                        # se não existir, será colocado espaços vazios nos dados do mês
                        else:
                            # separar nos casos de meses 31 e 30 e cria valores vazios
                            if ano_inicial in lista_bissexto:
                                if b in lista_mes31:
                                    dataframe['Mês'] = b
                                    for c in range(1, 32):
                                        dataframe['Precipitação'] = 'SD'
                                        dataframe['Dia'] = c
                                        lista.append(dataframe.copy())
                                elif b in lista_mes30:
                                    dataframe['Mês'] = b
                                    for c in range(1, 31):
                                        dataframe['Precipitação'] = 'SD'
                                        dataframe['Dia'] = c
                                        lista.append(dataframe.copy())
                                else:
                                    dataframe['Mês'] = b
                                    for c in range(1, 30):
                                        dataframe['Precipitação'] = 'SD'
                                        dataframe['Dia'] = c
                                        lista.append(dataframe.copy())

                            else:
                                if b in lista_mes31:
                                    dataframe['Mês'] = b
                                    for c in range(1, 32):
                                        dataframe['Precipitação'] = 'SD'
                                        dataframe['Dia'] = c
                                        lista.append(dataframe.copy())
                                elif b in lista_mes30:
                                    dataframe['Mês'] = b
                                    for c in range(1, 31):
                                        dataframe['Precipitação'] = 'SD'
                                        dataframe['Dia'] = c
                                        lista.append(dataframe.copy())
                                else:
                                    dataframe['Mês'] = b
                                    for c in range(1, 29):
                                        dataframe['Precipitação'] = 'SD'
                                        dataframe['Dia'] = c
                                        lista.append(dataframe.copy())

                    ano_inicial += 1
                # Caso em que o ano da linha pulou para outro ano. Ano faltante
                else:
                    dataframe['Ano'] = ano_inicial
                    # criamos o que seriam os meses e dias, porém com dados em branco

                    for b in range(1, 13):
                        if ano_inicial in lista_bissexto:
                            if b in lista_mes31:
                                dataframe['Mês'] = b
                                for c in range(1, 32):
                                    dataframe['Precipitação'] = 'SD'
                                    dataframe['Dia'] = c
                                    lista.append(dataframe.copy())
                            elif b in lista_mes30:
                                dataframe['Mês'] = b
                                for c in range(1, 31):
                                    dataframe['Precipitação'] = 'SD'
                                    dataframe['Dia'] = c
                                    lista.append(dataframe.copy())
                            else:
                                dataframe['Mês'] = b
                                for c in range(1, 30):
                                    dataframe['Precipitação'] = 'SD'
                                    dataframe['Dia'] = c
                                    lista.append(dataframe.copy())
                        else:
                            if b in lista_mes31:
                                dataframe['Mês'] = b
                                for c in range(1, 32):
                                    dataframe['Precipitação'] = 'SD'
                                    dataframe['Dia'] = c
                                    lista.append(dataframe.copy())
                            elif b in lista_mes30:
                                dataframe['Mês'] = b
                                for c in range(1, 31):
                                    dataframe['Precipitação'] = 'SD'
                                    dataframe['Dia'] = c
                                    lista.append(dataframe.copy())
                            else:
                                dataframe['Mês'] = b
                                for c in range(1, 29):
                                    dataframe['Precipitação'] = 'SD'
                                    dataframe['Dia'] = c

                    ano_inicial += 1

            datad = pd.DataFrame(lista)
            #
            self.dataset = datad
    def save_csv(self, pasta, sep=';', index=False):
        self.dataset.to_csv(pasta, sep=sep, index=index)
    def dados_faltantes(self):
        lista_meses = []
        temp = []
        for k in range(32):
            'Os dados de precipitação são dados com Chuva ou Clima, seguidos ' \
            'da data no mês'
            if k < 10:
                lista_meses.append(f'Chuva0{k}')
                lista_meses.append(f'Clima0{k}')
            else:
                lista_meses.append(f'Chuva{k}')
                lista_meses.append(f'Clima{k}')

        contador_sd = 0
        total = 0
        # muda de virgula para ponto
        arquivo = self.dataset.replace({',': '.'}, regex=True)
        for k in lista_meses:
            if k in arquivo.columns:
                temp.append(k)
        lista_meses.clear()
        lista_meses = temp

        for a in range(self.len):
            for b in lista_meses:
                # caso do nan
                if type(arquivo[b][a]) is float:
                    contador_sd += 1
                else:
                    try:
                        float(arquivo[b][a])
                    except:
                        contador_sd += 1
                    total += 1
        return (contador_sd / total) * 100
    def do_data_lost(self):
        import datetime
        # se não estiver crescente, deixa crescente
        if self.enddate < self.startdate:
            self.dataset = self.dataset.sort_values(by=['Data'], ascending=True)
        for a in range(self.len):
            if self.date(a) > self.date(a):
                obh = 0
    def plot(self, title='', xlabel='', ylabel='', save=''):
        from datetime import datetime
        from matplotlib import pyplot as plt
        a = self.format1()
        colum = a.columns
        y = a[colum[1]]
        x = a[colum[0]]
        temp = []
        for k in x:
            temp.append(k)
        x = temp[:]
        temp.clear()
        for k in y:
            temp.append(float(k))
        y = temp[:]
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()
        plt.bar(x, y)

        plt.savefig(save)
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

                E deixamos da forma:

                Data        pr
                1997-07-01  0.1
                1997-07-02  0.3
                ....
                ...
                ...
                2020-01-01  0.3
                2020-01-02  0.0
                '''

        import pandas as pd
        from datetime import datetime

        # Organizando o arquivo pela datas do menor até o maior
        df_ordenado = self.dataset
        df_ordenado['Data'] = pd.to_datetime(df_ordenado['Data'], format="%d/%m/%Y")
        df_ordenado = df_ordenado.drop_duplicates(subset='Data')
        if virgula_para_ponto:
            df_ordenado = df_ordenado.replace({',': '.'}, regex=True)
            df_ordenado = df_ordenado.reset_index()
            df_ordenado = df_ordenado.drop(columns='index')
            self.dataset = df_ordenado
        if not crescente:
            self.dataset = df_ordenado.sort_values(by=['Data'], ascending=True)

        Data = []
        prec = []
        self.only_mondata()
        # indução
        colum = self.dataset.columns
        for linha in range(len(self.dataset)):
            for dia in range(1, 32):
                try:
                    temp = self.dataset[colum[0]][linha]
                    Data.append(datetime(temp.year, temp.month, dia))
                    prec.append(float(self.dataset[colum[dia]][linha]))
                except:
                    n = 0
        df = pd.DataFrame(list(zip(Data, prec)), columns=['Data', 'pr'])
        return df
    def to_netcdf4(self, local):
        import xarray as xr
        df = self.format1(crescente=False)
        df = df.rename(columns={'pr': 'pr', 'Data': 'time'})
        # pr para numero
        temp = []
        for k in df['pr']:
            temp.append(float(k))
        df['pr'] = temp[:]

        # criando latitude e longitude com valor (0,0)
        lat = [0] * len(df['pr'])
        lon = [0] * len(df['pr'])
        df['lat'] = lat
        df['lon'] = lon
        # abrindo o df com o xarray
        ds = df.set_index(['time', 'lat', 'lon']).to_xarray()

        ds = xr.Dataset(ds)
        # add variable attribute metadata
        ds.attrs['lat'] = 'Units: °'
        ds.attrs['lon'] = 'Units: °'
        ds.attrs['time'] = 'Data diária'

        ds.to_netcdf(local + f'_{self.codigo}_{self.type_data}.nc')
    def rx5day(self, with_x=False):
        from indice import Indice
        ind = Indice(self.format1())
        ind = ind.rx5day(type_data=self.type_data, with_x=with_x)
        return ind
    def cdd(self, with_x=False):
        from indice import Indice
        ind = Indice(self.format1())
        ind = ind.cdd(type_data=self.type_data, with_x=with_x)
        return ind
    def cwd(self, with_x=False):
        from indice import Indice
        print(self.type_data)
        ind = Indice(self.format1())
        ind = ind.cwd(type_data=self.type_data, with_x=with_x)
        return ind
    def prcptot(self, with_x=False):
        from indice import Indice
        ind = Indice(self.format1())
        ind = ind.prcptot(type_data=self.type_data, with_x=with_x)
        return ind
    def prcptot_monthly(self, with_x=False):
        from indice import Indice
        ind = Indice(self.format1())
        ind = ind.prcptot_monthly(type_data=self.type_data, with_x=with_x)
        return ind
    def r99p(self, with_x=False):
        from indice import Indice
        ind = Indice(self.format1())
        ind = ind.r99p(type_data=self.type_data, with_x=with_x)
        return ind
    def rnnmm(self, number, with_x=False):
        from indice import Indice
        ind = Indice(self.format1())
        ind = ind.rnnmm(number=number, type_data=self.type_data, with_x=with_x)
        return ind
    def r10mm(self, with_x=False):
        from indice import Indice
        ind = Indice(self.format1())
        ind = ind.r10mm(type_data=self.type_data, with_x=with_x)
        return ind
    def r20mm(self, with_x=False):
        from indice import Indice
        ind = Indice(self.format1())
        ind = ind.r20mm(type_data=self.type_data, with_x=with_x)
        return ind
    def r99ptot(self, with_x=False):
        from indice import Indice
        ind = Indice(self.format1())
        ind = ind.r99pTOT(type_data=self.type_data, with_x=with_x)
        return ind
    def rx1day_anual(self, with_x=False):
        from indice import Indice
        ind = Indice(self.format1())
        ind = ind.rx1day_anual(type_data=self.type_data, with_x=with_x)
        return ind
    def rx1day_monthly(self, with_x=False):
        from indice import Indice
        ind = Indice(self.format1())
        ind = ind.rx1day_monthly(type_data=self.type_data, with_x=with_x)
        return ind
import matplotlib.pyplot as plt

a = Ana(
    '/media/thiagosilva/thigs/Projetos/Amazônia/total/ANA/Medicoes_convencionais_Manaus_ANA/chuvas_T_00359005.txt')
x, y = a.rx1day_anual(with_x=True)

plt.plot(x, y)
plt.show()
