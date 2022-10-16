import pandas as pd
import numpy as np
import datetime

class TratBolivia():
    def __init__(self, path, encoding='utf-8', sep='|', type='t_maxmin', serie='diário'):

        def dataframe():
            if type == 't_maxmin':
                df = pd.read_csv(path, encoding=encoding,
                                 index_col=False, sep=sep)
                print(df)
                return df

        import pandas as pd
        self.dataframe = dataframe()
        self.type_data = type
        self.len = len(self.dataframe)

    def ByYear(self, year, var):
        # percorre procurando por ano
        inicio, final = 0, 0
        for linha in range(self.len):
            l = linha
            if self.date(linha).year == year:
                inicio = linha  # linha de inicio
                while self.date(l).year == year and l < self.len - 1:
                    l += 1
                final = l
                break
        return np.array(self.dataframe[f'{var}'][inicio:final])

    def TX(self, with_x=False):
        '''
        Encontra a temperatura máxima da máxima anual.
        Os dados necessitam ser diários
        :return:
        '''
        if self.type_data != 't_maxmin':
            raise 'O arquivo não está citado "type" como temp_maxmin'
        if with_x == False:
            y = [0]
            date_start = self.date(0).year  # Indice que fixa o ano para analisar
            cont = 0
            for tam in range(0, self.len):  # Percorre cada índice dos elementos
                if date_start == self.date(tam).year:
                    if y[cont] < float(self.dataframe['max'][tam]):
                        y[cont] = float(self.dataframe['max'][tam])
                else: # Se não atualizamos os índices para cálcular o próximo ano
                    y.append(0)
                    cont += 1
                    date_start += 1
            return y[0:-2]
        elif with_x == True:
            x = np.arange(self.date(0).year, self.date(self.len-1).year)
            y = [0]
            date_start = self.date(0).year  # Indice qua fixa o ano para analisar
            cont = 0
            for tam in range(0, self.len):  # Percorre cada índice dos elementos
                if date_start == self.date(tam).year:
                    if y[cont] < float(self.dataframe['Valor'][tam]):
                        y[cont] = float(self.dataframe['Valor'][tam])
                else:  # Se não atualizamos os índices para cálcular o próximo ano
                    y.append(0)
                    cont += 1
                    date_start += 1
            return x, y[0:-1]

    def TN(self, with_x=False):
        '''
                Encontra a temperatura máxima da mínima anual.
                Os dados necessitam ser diários
                :return:
                '''
        if self.type_data != 't_maxmin':
            raise 'O arquivo não está citado "type" como temp_maxmin'
        if with_x == False:
            y = [0]
            date_start = self.date(0).year
            cont = 0
            for tam in range(0, self.len):
                if date_start == self.date(tam).year:
                    if y[cont] < float(self.dataframe['Valor'][tam]):
                        y[cont] = float(self.dataframe['Valor'][tam])
                else:
                    y.append(0)
                    cont += 1
                    date_start += 1
            return y[0:-2]
        elif with_x == True:
            x = np.arange(self.date(0).year, self.date(self.len-1).year)
            y = [0]
            date_start = self.date(0).year
            cont = 0
            for tam in range(0, self.len):
                if date_start == self.date(tam).year:
                    if y[cont] < float(self.dataframe['Valor'][tam]):
                        y[cont] = float(self.dataframe['Valor'][tam])
                else:
                    y.append(0)
                    cont += 1
                    date_start += 1
            return x, y[0:-1]

    def TX90p(self, with_x=False):
        '''
        Encontra o percentil de 90% do TX para o mesmo período

        :param with_x:
        :return:
        '''
        #x, y = self.TX(with_x=True) # Calcula o TXx
        x = np.arange(self.date(0).year,self.date(self.len-1).year)
        y = []      #
        cont = i =0
        tx90p = [0]                 # O vetor começa em 0
        for ano in x:
            dias = 0
            ptx = np.nanpercentile(self.ByYear(ano, var='Valor'),90)
            print(ptx)
            while self.date(cont).year == ano:  # enquanto trabalharmos em um mesmo ano
                if self.dataframe['Valor'][cont] > ptx:  # compara com o percentil 90% do TX anual
                    tx90p[i] += 1
                cont += 1
                dias += 1
            tx90p[i] = 100 * tx90p[i] / dias   #Deixa em percentual anual
            i += 1
            tx90p.append(0)

        if with_x:
            return x, tx90p[0:-1]
        return tx90p[0:-1]

    def TN90p(self, with_x=True):
        '''

        :param with_x: True or False, se deseja que venha o valor da data também
        :return:
        '''
        x = np.arange(self.date(0).year, self.date(self.len - 1).year)
        cont = i = 0
        tn90p = [0]  # O vetor começa em 0
        for ano in x:
            dias = 0
            ptx = np.nanpercentile(self.ByYear(ano, var='Valor'), 90)
            print(ptx)
            while self.date(cont).year == ano:  # enquanto trabalharmos em um mesmo ano
                if self.dataframe['Valor'][cont] > ptx:  # compara com o percentil 90% do TX anual
                    tn90p[i] += 1
                cont += 1
                dias += 1
            tn90p[i] = 100 * tn90p[i] / dias  # Deixa em percentual anual
            i += 1
            tn90p.append(0)

        if with_x:
            return x, tn90p[0:-1]
        return tn90p[0:-1]

    def CDD(self):
        import climdex.precipitation as pdex
        indices = pdex.indices(time_dim='time')
        ds_cwd = indices.cwd(self.dataframe, varname='pr', period='Y')

    def date(self, line_number):
        return datetime.datetime.strptime(self.dataframe['Fecha'][line_number], "%Y-%m-%d %X")
