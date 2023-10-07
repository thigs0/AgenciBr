import os
import numpy as np
import shutil
from datetime import datetime, timedelta
from zipfile import ZipFile
import requests
from matplotlib import pyplot as plt

class Inemet:
    def __init__(self, path, encoding='utf-8', sep=';', type=None, list=False):

        """
        :param path:
        :param encoding:
        :param sep:
        :param type: Tipo de dados que tem no arquivo t_maxmin: Temperatura máxima e mínima
        """

        def linha_inicio_df(arquivo):
            """Abre o arquivo porém pula linhas em branco que por padrão são 4
            No inicio a primeira linha é transformada em head. Portanto, somamos+4+1"""
            df = pd.read_csv(arquivo, sep=';', on_bad_lines='skip',
                             encoding='latin-1')
            return len(df) + 2

        def find_cod(df):
            """
            Encontra o código da estação no dataframe
            """
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
            if x in ("t_maxmin", "precipitation"):  #If user say the variable
                return x
            df = pd.read_csv(path, skiprows=linha_inicio_df(path), nrows=50, on_bad_lines='skip')
            temp = str.lower(''.join(df.columns))
            if 'temperatura' in temp:
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
                return 'precipitation'

        def date(linha):

            """
                        Encontra a altura da estação no dataframe
                        """
            import datetime
            df = self.dataframe
            df = df.iloc[linha, 0]
            df = datetime.datetime.strptime(df, '%Y-%m-%d')
            return df

        def coords(path):
            df = pd.read_csv(path, nrows=linha_inicio_df(path), index_col=False,
                                           on_bad_lines='skip', encoding='latin-1')
            line_codigo = 0
            cord = {'lat': '', 'lon': ''}
            while True:
                temp = str(df.loc[line_codigo]).split()
                # se código aparece na linha, sabemos que é esta
                if 'Latitude:' in temp:
                    ind = temp.index('Latitude:')
                    temp = temp[ind+1]
                    cord['lat'] = temp

                    line_codigo += 1
                    temp = str(df.loc[line_codigo]).split()
                    ind = temp.index('Longitude:')
                    temp = temp[ind + 1]
                    cord['lon'] = temp
                    return cord
                line_codigo += 1

        def alt(path):
            df = pd.read_csv(path, nrows=linha_inicio_df(path), index_col=False,
                             on_bad_lines='skip', encoding='latin-1')
            line_codigo = 0
            while True:
                temp = str(df.loc[line_codigo]).split()
                # If the code appear at line
                if 'Altitude:' in temp:
                    ind = temp.index('Altitude:')
                    temp = temp[ind + 1]
                    return temp
                line_codigo += 1

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
            if self.type_data == 't_maxmin':
                df = pd.read_csv(path, encoding=encoding,
                                         index_col=False, sep=sep, skiprows=linha_inicio_df(path))
                df.columns = ['Data', 'max', 'min','']
                df = df.drop(columns='')
                return df
            elif self.type_data == 'precipitation':
                df = pd.read_csv(path, encoding=encoding,
                                 index_col=False, sep=sep, skiprows=linha_inicio_df(path))
                df.columns = ['Data', 'pr', '']
                df = df.drop(columns='')
                return df
            elif self.type_data == 't_med':
                df = pd.read_csv(path, encoding=encoding,
                                 index_col=False, sep=sep, skiprows=linha_inicio_df(path))
                df.columns = ['Data', 'med', '']
                df = df.drop(columns='')

                return df

        import pandas as pd
        if not list:
            self.type_data = type_data(type)
            self.dataframe = dataframe()
            self.code = find_cod(pd.read_csv(path, nrows=linha_inicio_df(path), index_col=False,
                                               on_bad_lines='skip', encoding='latin-1'))
            self.startdate = date(0)
            self.enddate = date(len(self.dataframe)-1)
            self.lat, self.lon = coords(path)['lat'], coords(path)['lon']
            self.altitude = alt(path)
            self.situacao = situacao(path)
            self.type= 'original'
            self.city = cidade(path)
            self.columns = self.dataframe.columns
            self.len = len(self.dataframe)
            self.list = False
        else:
            self.path = path
            self.list = True

    def show(self):
        print(self.dataframe)

    def empty_data(self, type='absolute'):
        import math

        if self.type != "format1":
            self.format1(comma_to_dot=True)
        # if data is temperature
        if self.type_data == 't_maxmin':
            cmax = np.sum(np.isnan(self.dataframe.iloc[:,1])) # Nan of max temperature
            cmin = np.sum(np.isnan(self.dataframe.iloc[:,2])) #Nan of min temperature
            if type == 'relative':
                return ((cmax / len(self.dataframe)) * 100, (cmin/len(self.dataframe))*100)
            elif type == 'absolute':
                return cmax, cmin
            else:
                raise "select one of two possibles types 'relative' or 'absolute'"

        # se estamos tratando de precipitação
        elif self.type_data == 'precipitation':
            c = np.sum(np.isnan(self.dataframe.iloc[:, 1]))
            if type == 'relative':
                return round((c / len(self.dataframe)) * 100)
            elif type == 'absolute':
                return round(c)
            else:
                raise "select one of two possibles types 'relative' or 'absolute'"
    def report(self, path):
        """
        Save a txt file with importants informations

        """
        self.format1()
        if (self.type_data == "t_maxmin"):
            with open(path, 'w') as f:
                f.write(f"Station {self.city} {self.code}\n")
                f.write(f"Empty data of {self.type_data} : {self.empty_data()}\n")
                f.write(f"Max value of max temperature: {np.max(self.dataframe.iloc[:, 1])}\n")
                f.write(f"Max value of min temperature: {np.max(self.dataframe.iloc[:, 2])}\n")
                v= self.dataframe.iloc[np.argmax(self.dataframe.iloc[:, 1]),0]
                f.write(f"Date of max value of max temperature: {v.day}/{v.month}/{v.year}\n")
                v= self.dataframe.iloc[np.argmax(self.dataframe.iloc[:, 2]),0]
                f.write(f"Date of max value of min temperature: {v.day}/{v.month}/{v.year}\n")
                f.write(f"Min value of max temperature: {np.min(self.dataframe.iloc[:, 1])}\n")
                f.write(f"Min value of min temperature: {np.min(self.dataframe.iloc[:, 2])}\n")
                v= self.dataframe.iloc[np.argmin(self.dataframe.iloc[:, 1]),0]
                f.write(f"Date of min value of max temperature: {v.day}/{v.month}/{v.year}\n")
                v= self.dataframe.iloc[np.argmin(self.dataframe.iloc[:, 2]),0]
                f.write(f"Date of min value of min temperature: {v.day}/{v.month}/{v.year}\n")
                f.close()
        elif (self.type_data == "precipitation"):
            with open(path, 'w') as f:
                f.write(f"Station {self.city} {self.code}\n")
                f.write(f"Empty data of {self.type_data}: {self.empty_data()}\n")
                f.write(f"Max value: {np.max(self.dataframe.iloc[:, 1])}\n")
                v= self.dataframe.iloc[np.argmax(self.dataframe.iloc[:, 1]),0]
                f.write(f"Date of max value: {v.day}/{v.month}/{v.year}\n")
                f.write(f"Min value: {np.min(self.dataframe.iloc[:, 1])}\n")
                v= self.dataframe.iloc[np.argmin(self.dataframe.iloc[:, 1]),0]
                f.write(f"Date of min value: {v.day}/{v.month}/{v.year}\n")
                f.close()
    def report_mf(self, path_in, path_out, var="precipitation", years=(0, 0)):
            """
            Save a txt file with imports informations of multiples files

            :param path_in: folder when are the files, only the files
            :param path_out: Folder when the output will be save
            """
            import pandas as pd
            files = os.listdir(path_in)
            if ( var == "t_maxmin" ):
                df = pd.DataFrame(columns=["Code of station", "Period", "Missing data Tmax","Missing data Tmin", "Max value Tmax","Max value Tmin", "Date of max Tmax", "Date max Tmin"])
                df["Code of station"] = np.arange(len(files))
                for i in range(len(files)):
                    ana = Inemet(path_in+"/"+files[i])
                    if (years == (0,0)):
                        ana.format1()
                    else:
                        ana.format1(years=years)
                    df.iloc[i, 0] = ana.code #Salva o código da estação 
                    df.iloc[i, 1] = f"{ana.startdate.day}/{ana.startdate.month}/{ana.startdate.year} - {ana.enddate.day}/{ana.enddate.day}/{ana.enddate.year}" #Salva o período da estação 
                    df.iloc[i, 2], df.iloc[i, 3] = ana.empty_data() #Salva os dados faltantes 
                    df.iloc[i, 4] = np.max(ana.dataframe.iloc[:, 1]) #Salva o valor máximo 
                    df.iloc[i, 5] = np.max(ana.dataframe.iloc[:, 2]) #Salva o valor máximo 
                    df.iloc[i, 6] = ana.dataframe.iloc[np.argmax(ana.dataframe.iloc[:, 1]), 0]
                    df.iloc[i, 7] = ana.dataframe.iloc[np.argmax(ana.dataframe.iloc[:, 2]), 0]
                df.to_csv(path_out)
             
    def plot(self):
        """

        :param title:
        :param xlabel:
        :param ylabel:
        :return:
        """
        from matplotlib import pyplot as plt
        from datetime import datetime
        colum = self.dataframe.columns
        if self.type_data == 'temperatura':
            y = self.dataframe[colum[1]]
            x = self.dataframe[colum[0]]
            temp = []
            for k in x:
                temp.append(datetime.strptime(k, '%Y-%m-%d'))
            x = temp
            plt.plot(x, y, linewidth=0.1)
            plt.show()

        elif self.type_data == 'precipitation':
            y = self.dataframe[colum[1]]
            x = self.dataframe[colum[0]]
            temp = []
            for k in x:
                temp.append(datetime.strptime(k, '%Y-%m-%d'))
            x = temp
            plt.bar(x, y)
            plt.tight_layout()

            plt.show()

    def get_year(self, year, with_x=False, return_x0=False):
        """
        From array muti-year, return a year specific
        :param year: can by a Int, or list of Int
        :param with_x:
        :param return_x0: Return the index init
        :return:
        """
        import pandas as pd
        self.format1()
        if isinstance(year, int):  # if is only a year
            try:
                a = pd.to_datetime(
                    self.dataframe[
                        'time']).dt.year.to_numpy() == year  # array with true or false if the year is that we want
            except:
                raise f"The Data don't have the year {year}"
            a = np.where(a == True)[0]  # Return array with index of True and correct the list format
            if with_x:
                return self.dataframe['time'][a], self.dataframe['pr'][a]
            elif return_x0:
                return a[0], self.dataframe['time'][a]
            return self.dataframe['pr'][a]
        else:  # is many years
            xf = pd.Series([])
            yf = np.array([])
            for i in year:
                try:
                    a = pd.to_datetime(
                        self.dataframe[
                            'time']).dt.year.to_numpy() == i  # array with true or false if the year is that we want
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
    def format1(self, comma_to_dot=True, grow=True, years=(0, 0)):
        """
        We change the file format to
        1) put date that can be jumped
        2) organize the file from to smaler to larger based in time 
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
        if self.type_data == 'precipitation':
            import datetime
            # if change to format1 and complete the years
            if self.type != 'format1' and years != (0, 0):
                from datetime import datetime

                # organize the file from smaller to larger
                df = self.dataframe
                df['Data'] = pd.to_datetime(df['Data'], format="%Y-%m-%d")
                df = df.drop_duplicates(subset='Data', keep="last")
                df = df.rename(columns={"Data": 'time'})

                if comma_to_dot:
                    df = df.replace({',': '.'}, regex=True)
                    df = df.reset_index()
                    df = df.drop(columns='index')
                    self.dataframe = df
                if not grow:
                    self.dataframe = df.sort_values(by=['time'], ascending=True)

                a = pd.date_range(start=datetime.date(self.startdate),
                                     end=self.enddate)
                a=a[:-1]
                data = pd.to_datetime(df["time"])
                pr = np.array(df['pr'])
                for i in range(len(a)):
                    if data[i] != a[i]:
                        t = pd.date_range(data[i - 1], data[i])[1:-1]
                        data = np.concatenate((data[:i], t, data[i:]))
                        pr = np.concatenate((pr[:i+1], (len(t)-2) * [np.NaN], pr[i-1:]))
                data = pd.date_range(start=datetime.date(self.startdate),
                                     end=self.enddate)  # change data to numpy datetime64
                del a

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


            elif self.type != 'format1':
                from datetime import datetime

                # organize the file from smaler to larger
                df = self.dataframe
                df['Data'] = pd.to_datetime(df['Data'], format="%Y-%m-%d")
                df = df.drop_duplicates(subset='Data', keep="last")
                df = df.rename(columns={"Data":'time'})
                if comma_to_dot:
                    df = df.replace({',': '.'}, regex=True)
                    df = df.reset_index()
                    df = df.drop(columns='index')
                    self.dataframe = df
                if not grow:
                    self.dataframe = df.sort_values(by=['time'], ascending=True)

                colum = self.dataframe.columns
                data = pd.to_datetime(self.dataframe[colum[0]])
                pr = self.dataframe[colum[1]].to_numpy()

                # chech if have date jump
                a = np.arange(self.startdate, self.enddate, timedelta(days=1)).astype(datetime)
                for i in range(len(a)):
                    if data[i] != a[i]:
                        t = pd.date_range(data[i - 1], data[i])[1:-1]
                        data = np.concatenate((data[:i], t, data[i:]))
                        pr = np.concatenate((pr[:i], len(t) * [np.NaN], pr[i:]))
                data = pd.date_range(start=datetime.date(self.startdate),
                                     end=self.enddate)  # change data to numpy datetime64

                df = pd.DataFrame(list(zip(data, pr)), columns=['time', 'pr'])
                self.dataframe = df

        elif self.type_data == 't_maxmin':
            from datetime import datetime

            # organize the date from smallest to bigest
            df = self.dataframe
            df['Data'] = pd.to_datetime(df['Data'], format="%Y-%m-%d")
            df = df.drop_duplicates(subset='Data', keep="last")

            # comma to point
            if comma_to_dot:
                df = df.replace({',': '.'}, regex=True)
                df = df.reset_index()
                df = df.drop(columns='index')
                df = df.rename(columns={"Data": 'time'})
                self.dataframe = df

            if not grow:
                df = df.rename(columns={'Data': 'Data'})
                self.dataframe = df.sort_values(by=['Data'], ascending=True)
                self.dataframe = self.dataframe.rename(columns={"Data": 'time'})
            # if change to format1 and complete the years
            if self.type != 'format1' and years != (0, 0):
                colum = self.dataframe.columns
                data = pd.to_datetime(self.dataframe[colum[0]])
                max = np.array(self.dataframe[colum[1]].to_numpy())
                min = np.array(self.dataframe[colum[2]].to_numpy())

                # chech if have date jump
                a = pd.date_range(datetime.date(self.startdate), self.enddate)

                # chech if have date jump
                for i in range(len(a)):
                    if data[i] != a[i]:
                        t = pd.date_range(data[i - 1], data[i])[1:-1]
                        data = np.concatenate((data[:i], t, data[i:]))
                        max = np.concatenate((max[:i], len(t) * [np.NaN], max[i:]))
                        min = np.concatenate((min[:i], len(t) * [np.NaN], min[i:]))

                a = pd.date_range(start=str(years[0]), end=str(years[1]), freq='D')
                a=a[:-1]
                max_def = np.full(len(a), np.nan)
                min_def = np.full(len(a), np.nan)
                for i in range(len(data)):
                    ind = np.argwhere(data[i] == a)
                    max_def[ind] = max[i]
                    min_def[ind] = min[i]
                # atualize the format and len
                self.dataframe = pd.DataFrame(list(zip(a, max, min)), columns=['time', 'max', "min"])
                self.type = "format1"
                self.len = len(self.dataframe)
                self.enddate = df.iloc[-1,0] 
                self.startdate = df.iloc[0, 0]

            elif self.type != "format1":
                colum = self.dataframe.columns
                data = pd.to_datetime(self.dataframe[colum[0]])
                max = self.dataframe[colum[1]].to_numpy()
                min = self.dataframe[colum[2]].to_numpy()
                a = pd.date_range(start=datetime.date(self.startdate),
                                     end=self.enddate)
                a=a[:-1]


                # chech if have date jump
                for i in range(len(a)):
                    if data[i] != a[i]:
                        t = pd.date_range(data[i - 1], data[i])[1:-1]
                        data = np.concatenate((data[:i], t, data[i:]))
                        max = np.concatenate((max[:i], len(t)*[np.NaN], max[i:]))
                        min = np.concatenate((min[:i], len(t)*[np.NaN], min[i:]))

                data = pd.date_range(start=datetime.date(self.startdate),
                                     end=self.enddate)  # change data to numpy datetime64

                # atualize the format and len
                self.type = "format1"
                self.len = len(self.dataframe)
                self.dataframe = pd.DataFrame(list(zip(data, max, min)), columns=['time', 'max', 'min'])
        elif self.type_data == 't_med':
            from datetime import datetime
        
            # Organizando o arquivo pela datas do menor até o maior
            df = self.dataframe
            df['Data'] = pd.to_datetime(df['Data'], format="%Y-%m-%d")
            df = df.drop_duplicates(subset='Data', keep="last")
            if comma_to_dot:
                df = df.replace({',': '.'}, regex=True)
                df = df.rename(columns={'Data': 'time'})
                df = df.reset_index()
                df = df.drop(columns='index')
                self.dataframe = df
            if not grow:
                df = df.rename(columns={'Data': 'time'})
                self.dataframe = df.sort_values(by=['time'], ascending=True)

            colum = self.dataframe.columns
            data = self.dataframe[colum[0]].to_numpy()
            med = self.dataframe[colum[1]].to_numpy()
            date = pd.date_range(start=datetime.date(self.startdate),
                                 end=self.enddate)  # change data to numpy datetime64
            # chech if have date jump
            for i in range(len(date)):
                try:
                    while np.datetime64(data[i]) != np.datetime64(date[i]):
                        data = np.insert(data, i, data[i - 1] + timedelta(days=1))
                        med = np.insert(med, i, np.NaN)
                except:
                    continue

            if self.type == "format1" and years != (0,0):
                self.dataframe = pd.DataFrame(list(zip(date, med)), columns=['time', "med"])

                # atualize the format and len
                self.len = len(self.dataframe)
            elif self.type == "format":
                self.dataframe = pd.DataFrame(list(zip(data, med)), columns=['time', 'med'])

                # atualize the format and len
                self.type = "format1"
                self.len = len(self.dataframe)

        self.type = 'format1'

    def get_month(self, month, year, with_x=False):
        """
        From array muti-year, return a month specific
        :param month: The month to select as Int, or list of month to get
        :param year: The year to select
        :with_x: return the data, True or Not
        :return: Array with data of month select
        """
        if self.type != "format1":
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
                return self.dataframe['time'][a], self.dataframe['pr'][a]
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

    #Convert to another version
    def to_netcdf4(self, local=''):
        import xarray as xr
        if self.type_data == 'precipitacao':
            self.format1(grow=False)
            df = self.dataframe

            df = df.rename(columns={'precipitação': 'pr'})  # verificar se é este o nome
            df = df.rename(columns={'Data': 'time'})

            # criando latitude e longitude com valor (0,0)
            lat = [float(self.lat)] * len(df['pr'])
            lon = [float(self.lon)] * len(df['pr'])
            df['lat'] = lat
            df['lon'] = lon
            # abrindo o df com o xarray
            ds = df.set_index(['time', 'lat', 'lon']).to_xarray()

            ds = xr.Dataset(ds)
            # add variable attribute metadata
            ds.attrs['lat'] = 'Units: °'
            ds.attrs['lon'] = 'Units: °'
            ds.attrs['time'] = 'Daily Data'

            return ds.to_netcdf(local+f'/Dados{self.codigo}_D_{self.startdate.year}_{self.enddate.year}.nc')

        elif self.type_data == 't_maxmin':
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

    def to_csv(self, local=""):
        self.dataframe.to_csv(local, index=False)

    def date(self, linha):

        """
                    Encontra a altura da estação no dataframe
                    """
        import datetime
        df = self.dataframe
        df = df.iloc[linha, 0]
        df = datetime.datetime.strptime(df, '%Y-%m-%d')
        return df

    def close(self):
        import gc
        gc.collect()

    def ByYear(self, year, var):
        """
        Of a dataframe, return a segment based in one year
        :param year: int, represent the year of segment
        :param var: str, is the name of variable you want data
        :return: array with variable data of one year
        """
        # research the year in file
        inicio, final = 0, 0
        for linha in range(self.len):
            l = linha
            if self.date(linha).year == year:
                inicio = linha  #start line
                while self.date(l).year == year and l < self.len-1:
                    l += 1
                final = l
                break
        return np.array(self.dataframe[f'{var}'][inicio:final])

    # Climate index
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
                    temp += float(ds.iloc[linha, 1])
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
                number_of_5day_heavy_precipitation_periods_per_time_period += 1

        if retornar == 'highest_five_day_precipitation_amount_per_time_period':
            return maior
        elif retornar == 'number_of_5day_heavy_precipitation_periods_per_time_period':
            return number_of_5day_heavy_precipitation_periods_per_time_period

    def tx(self, with_x=False):
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataframe)
        return ind.tx(with_x=with_x, type_data=self.type_data, var='max')

    def tn(self, with_x=False):
        from AgenciBr.indice import Indice
        ind = Indice(self.dataframe)
        return ind.tn(with_x=with_x, type_data=self.type_data)

    def tn90p(self, with_x=False):
        from AgenciBr.indice import Indice
        ind = Indice(self.dataframe)
        return ind.tn90p(with_x=with_x)

    def tx90p(self, with_x=False):
        from AgenciBr.indice import Indice
        ind = Indice(self.dataframe)
        ind = ind.tx90p(with_x=with_x, type_data=self.type_data)
        return ind

    #Download
    def download(self, path,  year_start=2000, year_end=datetime.now().year, file_save='zip', list_station='all'):
        """
        Download the data from site https://portal.inmet.gov.br/dadoshistoricos
        and change automatic to a model that you need

        :param path: The path to save the file
        :param year_start: The year that start the download
        :param year_end:
        :param file_save: The type of out file
        :param list_station: set a list of specify stations or all
        :return:
        """
        os.mkdir(f"{path}/tempo")
        for i in np.arange(year_start, year_end+1):  # list the years
            resposta = requests.get(f"https://portal.inmet.gov.br/uploads/dadoshistoricos/{i}.zip")
            # Acessa o conteúdo e salva em um arquivo
            if resposta.status_code == requests.codes.OK:
                with open(f"{path}/tempo/dadoshistóricos_{i}.zip", 'wb') as novo:
                    novo.write(resposta.content)
            else:
                resposta.raise_for_status()

        # if out file is zip file
        if file_save == 'zip':
            if list_station == 'all':
                for i in os.listdir(path+f'/tempo'):  # remove the temporary diretory and promove the files
                    shutil.move(path+f'/tempo/{i}', path+f"/{i}")
                os.rmdir(path+f"/tempo")
        # if out file is stract to directory
        if file_save == 'dir':
            if list_station == 'all':
                for i in os.listdir(path+f'/tempo'):  # remove the temporary diretory and promove the files
                    shutil.move(path+f'/tempo/{i}', path+f"/{i}")
                os.rmdir(path+f"/tempo")

                for k in os.listdir(path):
                    if int(k[-8:-4]) < 2020:
                        z = ZipFile(path+"/"+k, 'r')
                        z.extractall(path)
                        z.close()
                        os.remove(f"{path}/{k}")
                    else:
                        z = ZipFile(path + "/" + k, 'r')
                        os.mkdir(f"{path}/{k[-8:-4]}")
                        z.extractall(f"{path}/{k[-8:-4]}")
                        z.close()
                        os.remove(f"{path}/{k}")
            else: #is a city
                for i in os.listdir(path + f'/tempo'):  # remove the temporary diretory and promove the files
                    shutil.move(path + f'/tempo/{i}', path + f"/{i}")
                os.rmdir(path + f"/tempo")

                for k in os.listdir(path):
                    if int(k[-8:-4]) < 2020:
                        z = ZipFile(path + "/" + k, 'r')
                        z.extractall(path)
                        z.close()
                        os.remove(f"{path}/{k}")
                    else:
                        z = ZipFile(path + "/" + k, 'r')
                        os.mkdir(f"{path}/{k[-8:-4]}")
                        z.extractall(f"{path}/{k[-8:-4]}")
                        z.close()
                        os.remove(f"{path}/{k}")
                # remove the diferents
                for i in os.listdir(path):
                    city = list_station.upper()

                    for k in os.listdir(path+f"/{i}"):
                        if city not in k:
                            os.remove(f"{path}/{i}/{k}")

        # list functions

    def to_climatol(self, path, years, erro=10):
        import pandas as pd
        """
        :param path:
        :param years:
        :return:
        """
        if self.list == False:
            raise "This function need a list of stations, change list=True and see the documentation"
        else:
            import os
            posi = []
            data = np.array([])
            c = 0
            for i, k in enumerate(os.listdir(self.path)):
                    a = Inemet(self.path + "/" + k)
                    a.format1(years=years)
                    if a.empty_data()< erro:
                        if c == 0:
                            data = np.array([a.dataframe["pr"]])
                            posi.append([a.lat, a.lon, a.altitude, f"{a.code}", f"Ana-{a.code}"])
                            c+=1
                        else:
                            data = np.append(data, [a.dataframe["pr"]], axis=0)
                            posi.append([a.lat, a.lon, a.altitude, f"{a.code}", f"Inemet-{a.code}"])

            a = pd.DataFrame(np.transpose(data))
            b = pd.DataFrame(posi)

            # Before to save, climatol find empty place with some word in string "nan". Because this, we change to str
            a = a.astype(str)
            b = b.astype(str)
            a.to_csv(path + f"/pr_{years[0]}-{years[1]}.dat", index=False, header=False, sep=" ")
            b.to_csv(path + f"/pr_{years[0]}-{years[1]}.est", index=False, header=False, sep=" ")

        with open("inemet/climatol.r", "w") as climatol:
            climatol.write(f"""
            library(climatol)

            #------------------------------------------------------
            setwd("{self.path}")

            dat <- as.matrix(read.table("pr_{years[0]}-{years[1]}.dat"))
            write(dat, "Ttest_{years[0]}-{years[1]}.dat")

            homogen('pr', {years[0]}, {years[1]}, expl = TRUE)

            """)
            climatol.close()
        os.system("Rscript inemet/climatol.r")
