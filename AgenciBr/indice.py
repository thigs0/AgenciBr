import datetime

import numpy
import numpy as np
import pandas as pd

# The index are based in: https://www.climdex.org/learn/indices/
class Indice:
    def __init__(self, x, y):
        self.x = pd.to_datetime(x)
        self.y = y
        self.len = len(self.x)

    def date(self, linha):
        '''
                Encontra a altura da estação no dataframe
        '''
        import datetime
        df = self.x[linha]
        try:  # Caso já esteja em Datetime
            temp = df.year
            del temp
            return df
        except:
            df = datetime.datetime.strptime(df, '%Y-%m-%d')
            return df

    def ByYear(self, year, with_x=False):
        """
        :param year: A data que queremos
        :param var: A variável do dataframe
        :return: Retorna um array com todos os valores no período anual
        """
        # percorre procurando por ano
        inicio, final = 0, 0
        for linha in range(self.len):
            l = linha
            if self.date(linha).year == year:
                inicio = linha  # linha de inicio
                while l <= self.len - 1 and self.date(l).year == year:
                    l += 1
                final = l
                break
        if with_x:
            return (np.array(self.x[inicio:final]) ,np.array(self.y[inicio:final]))
        return np.array(self.y[inicio:final])

    def ByMonth(self, year, month, var):
        """
        Dado um array diário com vários anos, ele seleciona e retorna apenas uma região daquele mês pedido
        :param year:
        :param month:
        :param var:
        :return:
        """
        # percorre procurando por ano
        inicio, final = 0, 0
        for linha in range(self.len):
            n = 0
            l = linha
            if self.date(linha).year == year and self.date(linha).month == month:
                inicio = linha  # linha de inicio
                while self.date(l).year == year and self.date(l).month == month and l < self.len - 1:
                    l += 1
                final = l
                break
        return np.array(self.dataframe[f'{var}'][inicio:final])
        #  íncides de temperatura

    def tx(self, with_x=False, type_data='t_maxmin'):
        """
        Find the maximum temperature annual for the serie
        The data need by daily
        :param with_x: (Boolean) return the day when the maximum
        :param type_data:
        :param var:
        :return:
        """
        inicio = self.date(0).year # return the initial year
        fim = self.date(self.len - 1).year #the last year

        tx = np.zeros(fim+1-inicio)  # variable
        x = np.empty(fim+1-inicio, dtype='<U4')

        for k in range(inicio, fim+1):  # range the years
            x0,y0 = self.ByYear(k, with_x=True)
            x[k-inicio] = x0[np.nanargmax(y0)]
            tx[k-inicio]= np.nanmax(y0) 
            
            del x0 
            del y0
        if with_x:
            return x, tx
        return tx

    def tn(self, with_x=False, type_data='t_maxmin'):
        """
        Find the maximum temperature annual for the serie
        The data need by daily
        :param with_x: (Boolean) return the day when the maximum
        :param type_data:
        :param var:
        :return:
        """
        inicio = self.date(0).year # return the initial year
        fim = self.date(self.len - 1).year #the last year

        tn = np.zeros(fim+1-inicio)  # variable
        x = np.empty(fim+1-inicio, dtype='<U4')

        for k in range(inicio, fim+1):  # range the years
            x0,y0 = self.ByYear(k, with_x=True)
            x[k-inicio] = x0[np.nanargmax(y0)]
            tn[k-inicio]= np.nanmax(y0) 
            
            del x0 
            del y0
        if with_x:
            return x, tn
        return tn

    def tx90p(self, with_x=False, type_data='t_maxmin', var='tmax'):
        '''
        Encontra o percentil de 90% do TX para o mesmo período

        :param with_x:
        :return:
        '''

        x = np.arange(self.date(0).year, self.date(self.len - 1).year)
        cont = i = 0
        tx90p = [0]  # O vetor começa em 0
        for ano in x:
            dias = 0
            ptx = np.nanpercentile(self.ByYear(ano, var=f'{var}'), 90)
            while self.date(cont).year == ano:  # enquanto trabalharmos em um mesmo ano
                if self.dataframe[f'{var}'][cont] > ptx:  # compara com o percentil 90% do TX anual
                    tx90p[i] += 1
                cont += 1
                dias += 1
            tx90p[i] = 100 * tx90p[i] / dias  # Deixa em percentual anual
            i += 1
            tx90p.append(0)

        if with_x:
            return x, tx90p[0:-1]
        return tx90p[0:-1]

    def tn90p(self, with_x=True, var='min'):
        '''

        :param with_x: True or False, se deseja que venha o valor da data também
        :var:
        :return:
        '''
        x = np.arange(self.date(0).year, self.date(self.len - 1).year)
        cont = i = 0
        tn90p = [0]  # O vetor começa em 0
        for ano in x:
            dias = 0
            ptx = np.nanpercentile(self.ByYear(ano, var=f'{var}'), 90)
            while self.date(cont).year == ano:  # enquanto trabalharmos em um mesmo ano
                if self.dataframe[f'{var}'][cont] > ptx:  # compara com o percentil 90% do TX anual
                    tn90p[i] += 1
                cont += 1
                dias += 1
            tn90p[i] = 100 * tn90p[i] / dias  # Deixa em percentual anual
            i += 1
            tn90p.append(0)

        if with_x:
            return x, tn90p[0:-1]
        return tn90p[0:-1]

    def tn10p(self, with_x=False, type_data='t_maxmin'):
        '''

            :param with_x: True or False, se deseja que venha o valor da data também
            :return:
            '''
        if type_data == 't_maxmin':
            x = np.arange(self.date(0).year, self.date(self.len - 1).year)
            cont = i = 0
            tn90p = [0]  # O vetor começa em 0
            for ano in x:
                dias = 0
                ptx = np.nanpercentile(self.ByYear(ano, var='min'), 10)
                while self.date(cont).year == ano:  # enquanto trabalharmos em um mesmo ano
                    if self.dataframe['min'][cont] > ptx:  # compara com o percentil 90% do TX anual
                        tn90p[i] += 1
                    cont += 1
                    dias += 1
                tn90p[i] = 100 * tn90p[i] / dias  # Deixa em percentual anual
                i += 1
                tn90p.append(0)

            if with_x:
                return x, tn90p[0:-1]
            return tn90p[0:-1]

    def fd(self, with_x=False):
        """
        Number of frost days: annual count of days when TN (daily minimum temperature) <0°C
        :param type_data:  Tipo de informação contida no array
        :return: Return the quantide of days  with temperature < 0°C by year
        """
        inicio = self.date(0).year  # initial year
        fim = self.date(self.len-1).year  # end year
        fd = np.zeros(fim+1-inicio)  # values

        for k in range(inicio, fim + 1):
            t = self.ByYear(k)  # vetor com dados de um ano
            fd[k-inicio] = np.sum(t < 0)
        if with_x:
            return np.arange(inicio, fim+1), fd
        return fd

    def su(self, with_x=False, type_data='t_maxmin'):
        """
        Number of summer days: annual count of days when TX (daily maximum temperature) >25°C
        :param with_x: Retorna o vetor com datas ou não (True, False)
        :param type_data: Tipe de data que está entrando
        :return: Retorna a quantidade de dias da temperatura máxima > 25°C por ano
        """
        inicio = self.date(0).year  # initial year
        fim = self.date(self.len-1).year  # end year
        su = np.zeros(fim+1-inicio)  # values

        for k in range(inicio, fim + 1):
            t = self.ByYear(k)  # vetor com dados de um ano
            su[k-inicio] = np.sum(t > 25)
        if with_x:
            return np.arange(inicio, fim+1), su
        return su

    def tr(self, with_x=False, type_data='t_maxmin', var=('tmax', 'tmin')):
        """
        TR, Number of tropical nights: Annual count of days when TN (daily minimum temperature) > 20°C.
        :param with_x: Retorna o vetor com datas ou não (True, False)
        :param type_data: Tipe de data que está entrando
        :param var: um vetor em que a primeira componente é o nome da temperatura máxima e o segundo da temperatura mínima
        :return: Retorna A temperatura máxima mensal menos a mínima
        """
        inicio = self.date(0).year  # initial year
        fim = self.date(self.len-1).year  # end year
        tr = np.zeros(fim+1-inicio)  # values

        for k in range(inicio, fim + 1):
            t = self.ByYear(k)  # vetor com dados de um ano
            tr[k-inicio] = np.sum(t > 20)
        if with_x:
            return np.arange(inicio, fim+1), tr
        return tr

    # índices de chuvas
    def rnnmm(self, number, with_x=False, type_data='pr'):
        """
        Rnnmm Annual count of days when PRCP≥ nnmm, nn is a user defined threshold
        :param with_x: Retorna o array com as datas de cada dado
        :param type_data:
        :param var:
        :return:
        """

        inicio = self.date(0).year  # start year
        fim = self.date(self.len-1).year  # End year
        rnnmm = np.zeros(fim+1-inicio)  # Data

        for ano in range(inicio, fim + 1):
            t = self.ByYear(ano)  #
            rnnmm = np.append(rnnmm, np.sum(t >= number))  # number of values > number
        if with_x:
            return np.arange(inicio, fim+1), rnnmm
        return rnnmm

    def rx5day(self, valor=1, retornar='number_of_5day_heavy_precipitation_periods_per_time_period', time='y',
               selbyyear=0,
               with_x=False, type_data='pr'):
        '''
        rx5day is a function that return the highest 5 days acumulatted in a year
        :param valor: valor fixo do mínimo que consideramos
        :param retornar:Opções para retornar: highest_five_day_precipitation_amount_per_time_period, que é uma lista 0 é o numero e 1 é o mês
        ; number_of_5day_heavy_precipitation_periods_per_time_period
        :time:
        :return: The value
        '''

        import datetime
        import pandas as pd

        # deixa apenas os dados de precipitação
        number_of_5day_heavy_precipitation_periods_per_time_period = 0
        date = [0]
        maior = {0: 0, 1: 0}

        start = self.date(0).year 
        resul = [0]
        resul = np.zeros(self.date(self.len-1).year + 1-start)
        cont = r = 0
        while cont < len(data) - 1:  # while is not the end year
            temp = 0
            for k in range(5):
                if cont + k < len(data) - 2 and self.date(
                        cont + k).year == start:  # Se continuamos no mesmo ano
                    temp += float(self.y[cont + k])

                else:
                    break
            if temp > resul[r]:  # Se a sequência atual é maior que a anterior
                resul[r] = temp
                date[r] = self.date(cont).month

            if self.date(cont).year != start:  # pulamos de ano
                r += 1
                cont += 1
                date.append(0)
                start += 1
            else:
                cont += 5
        number_of_5day_heavy_precipitation_periods_per_time_period = resul

        # Retorna
        if retornar == 'highest_five_day_precipitation_amount_per_time_period':
            if with_x:  # retornamos o eixo x também
                return np.arange(self.date(0).year, self.date(-1).year + 1), maior
            else:
                return maior
        elif retornar == 'number_of_5day_heavy_precipitation_periods_per_time_period':
            return (range(self.date(0).year, self.date(-1).year + 1),
                    number_of_5day_heavy_precipitation_periods_per_time_period)
        elif retornar == "date":
            return  (range(self.date(0).year, self.date(-1).year + 1), date)

    def cdd(self, with_x=False, type_data='pr'):
        serie = np.array(self.dataframe.iloc[:, 1]).astype(float)
        start = self.date(0).year
        resul = [0]
        cont = r = 0
        while cont <= len(self.dataframe) - 1:  # Enquanto não for o último ano
            temp = 0
            if cont < len(self.dataframe) - 1:
                if serie[cont] <= 1 and isinstance(serie[cont], float):  # Se não choveu
                    while serie[cont] <= 1 and self.date(cont).year == start and cont < len(
                            self.dataframe) - 1:  # Enquanto não chover, conta os dias
                        temp += 1
                        cont += 1
                else:
                    cont += 1

            if temp > resul[r]:  # Se a sequência atual é maior que a anterior
                resul[r] = temp
            if self.date(cont).year != start:  # pulamos de ano
                r += 1
                cont += 1
                resul.append(0)
                start += 1
            else:
                cont += 1
        if with_x:
            return np.arange(self.date(0).year, self.date(-1).year + 1), resul
        return resul

    def cwd(self, with_x=False, type_data='pr'):
        serie = np.array(self.dataframe.iloc[:, 1]).astype(float)
        start = self.date(0).year
        resul = np.array([0])
        cont = r = 0
        while cont <= len(self.dataframe) - 1:  # Enquanto não for o último ano
            temp = 0
            # print(cont)
            if serie[cont] >= 1 and isinstance(serie[cont], float):  # Se não choveu ou o dado é inválido
                while serie[cont] >= 1 and self.date(cont).year == start and cont < len(
                        self.dataframe) - 1:  # Enquanto não chover, conta os dias
                    temp += 1
                    cont += 1
            else:
                cont += 1

            if temp > resul[r]:  # Se a sequência atual é maior que a anterior

                resul[r] = temp

            if self.date(cont).year != start:  # pulamos de ano
                r += 1
                cont += 1
                resul = np.append(resul, 0)
                start += 1
            else:
                cont += 1
        if with_x:
            return np.arange(self.date(0).year, self.date(-1).year + 1), resul
        return resul

    def prcptot(self, with_x=False, type_data='pr', var='pr'):
        if type_data == 'pr':
            start = self.date(0).year
            r = np.array([])
            for ano in range(start, self.date(self.len-1).year+1):
                r = np.append(r, np.nansum(self.ByYear(ano,var)))
            if with_x:
                return np.arange(self.date(0).year, self.date(-1).year), r
            return r
        else:
            raise "This index can only be calculated with precipitation (type_data='pr')"

    def prcptot_monthly(self, with_x=False, type_data='pr', var='pr'):
        if type_data == 'pr':
            prcptot = np.array([])
            inicio = self.date(0).year  # Ano de inicio
            fim = self.date(self.len-1).year  # Ano de termino
            for ano in range(inicio, fim + 1):
                for mes in range(1, 13):
                    if ano == inicio: # Se é o ano inicial
                        if mes>=self.date(0).month: # se o mês for válido
                            prcptot = np.append(prcptot, np.nansum(self.ByMonth(ano, mes, var=var)))
                    elif ano == fim: # se é o último ano
                        if mes <= self.date(self.len-1).month:
                            prcptot = np.append(prcptot, np.nansum(self.ByMonth(ano, mes, var=var)))
                    else:
                        prcptot = np.append(prcptot, np.nansum(self.ByMonth(ano, mes, var=var)))
            if with_x:
                return pd.date_range(start =f'{inicio}-{self.date(0).month}-01',end =f'{fim}-{self.date(self.len-1).month}-1', freq = '1M'), prcptot[:-1]
            return prcptot
        else:
            raise "This index can only be calculated with precipitation (type_data='pr')"

    def r99p(self, with_x=False, type_data='pr', var='pr'):
        #Refazer
        if type_data == 'pr':
            x = np.arange(self.date(0).year, self.date(self.len-1).year+1)
            cont = i = 0
            tn90p = [0]  # O vetor começa em 0
            for ano in x:
                dias = 0
                ptx = np.percentile(self.ByYear(ano, var=var), 99)
                while cont < self.len and self.date(cont).year == ano:  # enquanto trabalharmos em um mesmo ano
                    if self.dataframe[f'{var}'][cont] > ptx:  # compara com o percentil 99% do percentil anual
                        tn90p[i] += 1
                    cont += 1
                    dias += 1
                tn90p[i] = 100 * tn90p[i] / dias  # Deixa em percentual anual
                i += 1
                tn90p.append(0)

            if with_x:
                return x, tn90p[0:-1]
            return tn90p[0:-1]

    def r95p(self, with_x=False, type_data='pr', var='pr'):
        """
        :param with_x:
        :param type_data:
        :param var:
        :return: Retorna o vetor anual em que o percentil de 95
        """
        if type_data == 'pr':
            # Refazer, dar um jeito no nan
            x = np.arange(self.date(0).year, self.date(self.len - 1).year + 2)
            cont = i = 0
            r95p = [0]  # O vetor começa em 0
            for ano in x:
                dias = 0
                ptx = np.nanpercentile(self.ByYear(ano, var=var), 95)
                while self.date(
                        cont).year == ano:  # enquanto tra                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          balharmos em um mesmo ano
                    if self.dataframe['pr'][cont] > ptx:  # compara com o percentil 90% do TX anual
                        r95p[i] += 1
                    cont += 1
                    dias += 1
                r95p[i] = 100 * r95p[i] / dias  # Deixa em percentual anual
                i += 1
                r95p.append(0)

            if with_x:
                return x, r95p[0:-1]
            return r95p[0:-1]

    def r10mm(self, with_x=False, type_data='pr', var='pr'):
        if type_data == 'pr':
            r10mm = np.array([])  # Vetor com dados
            inicio = self.date(0).year  # Ano de inicio
            fim = self.date(self.len-1).year  # Ano de término
            for ano in range(inicio, fim + 1):
                t = self.ByYear(ano, var)  # vetor com dados de um ano
                r10mm = np.append(r10mm, np.nansum(t >= 10))  # adiciona a soma do vetor True onde t>=10
            if with_x:
                return np.arange(inicio, fim+1), r10mm
            return r10mm

    def r20mm(self, with_x=False, type_data='pr', var='pr'):
        """

        :param with_x:
        :param type_data:
        :param var:
        :return:
        """
        if type_data == 'pr':
            r10mm = np.array([])  # Vetor com dados
            inicio = self.date(0).year  # Ano de inicio
            fim = self.date(self.len-1).year  # Ano de termino
            for ano in range(inicio, fim + 1):
                t = self.ByYear(ano, var)  # vetor com dados de um ano
                r10mm = np.append(r10mm, np.sum(t >= 20))  # adiciona a soma do vetor True onde t>=20
            if with_x:
                return np.arange(inicio, fim+1), r10mm
            return r10mm

    def r99pTOT(self, with_x=False, type_data='pr', var='pr'):
        """
        Contribution to total precipitation from very wet days

        :param with_x:
        :param type_data:
        :param var
        :return:
        """
        if type_data == 'pr':
            inicio = self.date(0).year  # Ano de inicio
            fim = self.date(self.len-1).year  # Ano de termino
            r99ptot = 100 * (self.r99p()/self.prcptot())
            if with_x:
                return np.arange(inicio, fim+1), r99ptot
            return r99ptot

    def rx1day_anual(self, with_x=False, type_data='pr', var='pr'):
        """

        :param with_x:
        :param type_data:
        :param var:
        :return:
        """
        if type_data == 'pr':
            rx1day = np.array([])
            inicio = self.date(0).year  # Ano de inicio
            fim = self.date(self.len-1).year  # Ano de termino
            for ano in range(inicio, fim + 1):
                rx1day = np.append(rx1day, np.nanmax(self.ByYear(ano, var=var)))  # o máximo de precipitação diária no ano
            if with_x:
                return np.arange(inicio, fim+1), rx1day
            return rx1day

    def rx1day_monthly(self, with_x=False, type_data='pr', var='pr'):
        """

        :param with_x:
        :param type_data:
        :param var:
        :return: Retorna um array com a precipitação máxima em cada mês
        """

        if type_data == 'pr':
            rx1day = np.array([])
            inicio = self.date(0).year  # Ano de inicio
            fim = self.date(self.len-1).year  # Ano de termino
            for ano in range(inicio, fim + 1):
                for mes in range(1, 13):
                    try:
                        rx1day = np.append(rx1day,
                                           np.max(self.ByMonth(ano, mes, var=var)))  # o máximo de precipitação diária no ano
                    except:
                        oi=1
            if with_x:
                return pd.date_range(start =f'{inicio}-{self.date(0).month}-01',end =f'{fim}-{self.date(self.len-1).month}-1', freq = '1M'), rx1day[:-1]
            return rx1day
