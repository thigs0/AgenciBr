import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from datetime import timedelta

#Site to get data http://dhime.ideam.gov.co/atencionciudadano/

class Ideam():
    def __init__(self, path, encoding='utf-8', sep='|', type='t_maxmin', serie='diário'):
        def type_data(df, type):
            return type

        def dataframe():
            if type == 't_maxmin':
                df = pd.read_csv(path, encoding=encoding,
                                 index_col=False, sep=sep)
                df["Fecha"] = pd.to_datetime(df['Fecha']).dt.date
                return df

        import pandas as pd
        self.dataframe = dataframe()
        self.type = "original" 
        self.len = len(self.dataframe)
        self.type_data = type_data(self.dataframe, type)
        self.startdate = self.dataframe['Fecha'][0]
        self.enddate = self.dataframe['Fecha'][len(self.dataframe) - 1]
    def byYear(self, year, var):
        """
        This function get the file and the var and return the data from this year

        :param year: type int
        :param var: type str with data var to get
        :return: data from colum 'var' and data in year 'year'
        """

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

    def report(self, path):
        """
        Save a txt file with importants informations

        """
        self.format1()
        if (self.type_data == "precipitation"):
            with open(path, 'w') as f:
                #f.write(f"Station {self.city} {self.code}\n")
                f.write(f"Empty data of : {self.empty_data()}\n")
                f.write(f"Max value: {np.max(self.dataframe.iloc[:, 1])}\n")
                v= self.dataframe.iloc[np.argmax(self.dataframe.iloc[:, 1]),0]
                f.write(f"Date of max value: {v.day}/{v.month}/{v.year}\n")
                f.write(f"Min value: {np.min(self.dataframe.iloc[:, 1])}\n")
                v= self.dataframe.iloc[np.argmin(self.dataframe.iloc[:, 1]),0]
                f.write(f"Date of min value: {v.day}/{v.month}/{v.year}\n")
                f.close()
    def byMonth(self, year, month, var):
        """
        English:
            With array dayly with many years, we select only year and month request
        Português:
            Dado um array diário com vários anos, ele seleciona e retorna apenas uma região daquele mês pedido
        :param year:
        :param month:
        :param var:
        :return: return a array with data in date requests
        """

        inicio, final = 0, 0
        for linha in range(self.len):
            l = linha
            if self.date(linha).year == year and self.date(linha).month == month:
                inicio = linha  # start line
                while self.date(l).year == year and self.date(l).month == month and l < self.len - 1:
                    l += 1
                final = l
                break
        return np.array(self.dataframe[f'{var}'][inicio:final])

    def rx5day(self, with_x=False):
       import indice
       a = indice.Indice(self.dataframe)
       a = a.rx5day(with_x=with_x)
       return a

    def rx5day_month(self, with_x=False):
        k = 0
        m = x = y = np.array([0])
        kano = 0
        for ano in range(self.startdate.year, self.enddate.year + 1):
            for mes in range(1, 13):
                while self.date(k).month == mes:  # while in the month
                    t = 0
                    for k2 in range(5):
                        if k == self.len - 1:
                            break
                        t += float(self.dataframe["Valor"][k])
                        k += 1
                    if t > y[kano]:
                        y[kano] = t
                        m[kano] = int(mes)
                    if k == self.len - 1:
                        break
            y = np.append(y, 0)
            m = np.append(m, 0)
            kano += 1

        return np.arange(self.startdate.year, self.enddate.year + 1), y[:-1], m[:-1]

    def tx(self, with_x=False):
        """
        English:
            Find the absolute max temperature from maximum temperature dairy, by year
            The data needs be daily

        Português:
            Encontra a temperatura máxima da máxima anual.
            Os dados necessitam ser diários
        :return: return
        """
        if self.type_data != 't_maxmin':
            raise "The file has not 'type'= 'temp_maxmin' "

        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataframe)
        return ind.tx(with_x=with_x)

    def tn(self, with_x=False):
        '''
        English:
            Find the absolute max temperature from minimun temperature dairy, by year
            The data needs be diary

        Portuguese:
                Encontra a temperatura máxima da mínima anual.
                Os dados necessitam ser diários
        :return: Return array with data or data and date
        '''
        if self.type_data != 't_maxmin':
            raise "The file is not cited 'type_data' as temp_maxmin "

        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataframe)
        ind = ind.tn(with_x=with_x)
        return ind

    def tx90p(self, with_x=False):
        '''
        English:
            Find the 90% percentil of tx in all array

        Português:
            Encontra o percentil de 90% do TX para o mesmo período

        :param with_x: True or False, return date array from data
        :return: Return array with data or data and date
        '''
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataframe)
        return ind.tx90p(with_x=with_x)

    def tn90p(self, with_x=True):
        '''
        English:
            Find the 90% percentil of tn in all array

        Português:
            Encontra o percentil de 90% do tn para o mesmo período

        :param with_x: True or False, se deseja que venha o valor da data também
        :return: Return array with data or data and date
        '''

        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataframe)
        return ind.tn90p(with_x=with_x)

    def prcptot(self, with_x=False):
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataset)
        ind = ind.prcptot(with_x=with_x)
        return ind

    def prcptot_monthly(self, with_x=False):
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataframe)
        ind = ind.prcptot_monthly(with_x=with_x)
        return ind

    def date(self, line_number):
        if self.type == 'format1':
            return self.dataframe['time'][line_number]
        return self.dataframe['Fecha'][line_number]

    def empty_data(self, type="absolute"):
        if self.type != "format1":
            self.format1()
        if (self.type_data == "precipitation"):
            if type == 'relative':
                s = np.sum(np.isnan(self.dataframe.iloc[:,1]))
                s = (s / self.len) * 100
                return s
            elif (type == "absolute"):
                return np.sum(np.isnan(self.dataframe.iloc[:,1])) # The absolute

    def format1(self, comma_to_dot=True, grow=True, years=(0,0)):
        """
                We change the file format to
                1) put date that can be jumped
                2) organize the file from to smaller to larger based in time
                3) Change the ',' to '.'
                4) Remove same values from file
                5) Change the name of time variable to time
                6) padronize a file to work with Ana, Inemet, Merge and etc
                7) have option to select a series of year start and year end. The date that not exist, are created and set NaN


                The out file is in format

                                time    pr
                                1997-07-01  0.1
                                1997-07-02  0.3
                                ....
                                ...
                                ...
                                2020-01-01  0.3
                                2020-01-02  0.0

                """
        import pandas as pd
        if years != (0,0) and self.type != "format1": # if is not format1 and select date
            self.dataframe['Fecha'] = pd.to_datetime(self.dataframe['Fecha'])
            self.dataframe['Valor'] = np.array(self.dataframe['Valor']).astype(float)
            self.dataframe = self.dataframe.rename(columns={'Fecha': 'time', 'Valor': 'pr'})
            if comma_to_dot:
                self.dataframe = self.dataframe.replace({',': '.'}, regex=True)

            data = self.dataframe["time"]
            pr = self.dataframe["pr"]

            # chech if have date jump
            a = pd.date_range(start=str(years[0]), end=str(years[1]), freq='D')
            a=a[:-1]
            pr_def = np.full(len(a), np.nan)
            for i in range(len(data)):
                ind = np.argwhere(data[i] == a)
                pr_def[ind] = pr[i]

            df = pd.DataFrame(list(zip(a, pr_def)), columns=['time', 'pr'])

            # atualize the format and len
            self.type = "format1"
            df = df[(df.iloc[:, 0].dt.year <= years[1])]
            self.dataframe = df[df.iloc[:, 0].dt.year >= years[0]]
            self.len = len(self.dataframe)
            self.enddate = df.iloc[-1,0] 
            self.startdate = df.iloc[0, 0]

            # atualize the format and len
            self.type = "format1"
            self.len = len(self.dataframe)

        elif self.type != "format1":
            self.dataframe['Fecha'] = pd.to_datetime(self.dataframe['Fecha'])
            self.dataframe['Valor'] = np.array(self.dataframe['Valor']).astype(float)
            self.dataframe = self.dataframe.rename(columns={'Fecha': 'time', 'Valor': 'pr'})
            if comma_to_dot:
                self.dataframe = self.dataframe.replace({',': '.'}, regex=True)

            colum = self.dataframe.columns
            data = pd.to_datetime(self.dataframe[colum[0]])
            pr = self.dataframe[colum[1]].to_numpy()

            # chech if have date jump
            a = pd.date_range(start=self.startdate, end=self.enddate, freq='D')
            a=a[:-1]
            pr_def = np.full(len(a), np.nan)
            for i in range(len(data)):
                ind = np.argwhere(data[i] == a)
                pr_def[ind] = pr[i]

            self.dataframe = pd.DataFrame(list(zip(a, pr_def)), columns=['time', 'pr'])


        self.type_data = 'precipitation'
        self.type = "format1"

    def get_year(self,year, with_x=False, return_x0=False):
        """
        English:
            From array multi-year, return a year specific

        Português:
            Do array, retorna um ano específico

        :param year: can by a Int, or list of Int
        :param with_x: True or False, to return date array or no
        :param return_x0: Return the index init
        :return:
        """
        self.format1()
        if isinstance(year, int): # if is only a year
            try:
                a = pd.to_datetime(
                    self.dataframe['time']).dt.year.to_numpy() == year  # array with true or false if the year is that we want
            except:
                raise f"The Data don't have the year {year}"

            a= np.where(a== True)[0] # Return array with index of True and correct the list format
            if with_x:
                return self.dataframe['time'][a], self.dataframe['pr'][a]
            elif return_x0:
                return a[0], self.dataframe['time'][a]
            return self.dataframe['pr'][a]
        else: # is many years
            xf = pd.Series([])
            yf = np.array([])
            for i in year:
                try:
                    a = pd.to_datetime(
                        self.dataframe[
                            'time']).dt.year.to_numpy() == i # array with true or false if the year is that we want
                except:
                    raise f"The Data don't have the year {i}"

                a = np.where(a == True)[0]  # Return array with index of True and correct the list format
                xf = pd.concat([xf, self.dataframe['time'][a]])
                yf = np.concatenate([yf, self.dataframe['pr'][a].to_numpy()])
            if with_x:
                return xf, yf
            elif return_x0:
                raise "This function exist only to one year"
            return yf
    def get_month(self, month, year, with_x=False):
        """
        English:
            From array muti-year, return a month specific

        Portuguese:
            Do array, retorna um mês específico
        :param month: The month to select as Int, or list of month to get
        :param year: The year to select
        :with_x: return the data, True or Not
        :return: Array with data of month select
        """
        if self.type_data != "format'":
            self.format1()
        #x0 is the index wen start the year that we want
        x0, time = self.get_year(year, return_x0=True)
        if isinstance(month, int):
            try:
                a = time.dt.month.to_numpy() == month  # array with true or false if the year is that we want
            except:
                raise f"The data has't the month {month}"
            a = np.where(a == True)[0]  # Return array with index of True and correct the list format
            a += x0
            if with_x:
                return self.dataframe['time'][a], self.dataset['pr'][a]
            return self.dataframe['pr'][a]
        else:
            xf = pd.Series([])
            yf = np.array([])
            for i in month:
                try:
                    a = time.dt.month.to_numpy() == i  # array with true or false if the year is that we want
                except:
                    raise f"The data has't the month {i}"
                a = np.where(a == True)[0]  # Return array with index of True and correct the list format
                a += x0
                xf = pd.concat([xf, self.dataframe['time'][a]])
                yf = np.concatenate([yf, self.dataframe['pr'][a].to_numpy()])
            if with_x:
                return xf, yf
            return yf
    def to_csv(self, path):
        """
         English:
            This function save the file that is save in .dataframe
        Português:
            Essa função salva o arquivo salvo dentro do .dataframe como um arquivo csv

        :param path:  str path to safe file and format .csv
        :return:
        """
        self.dataframe.to_csv(path)
    def to_netcdf(self,path):
        import xarray as xr
        t = self.dataframe.to_xarray()
        t = xr.Dataset(t)
        t.to_netcdf(path)
