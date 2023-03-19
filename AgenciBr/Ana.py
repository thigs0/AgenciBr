import datetime
import geopandas as gpd
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Ana:
    def __init__(self, arquivo, sep=';', index_col=False, list=False, encoding='latin-1',
                 on_bad_lines='skip', comma_to_dot=True, lat=None, lon=None):
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

        def dataframe(path):
            df = pd.read_csv(path, skiprows=linha_inicio_df(path), sep=sep, encoding=encoding,
                             index_col=index_col, on_bad_lines=on_bad_lines)
            if comma_to_dot:
                temp = []
                for k in df['Data']:
                    temp.append(datetime.datetime.strptime(k, '%d/%m/%Y'))
                df['Data'] = temp.copy()
                df = df.sort_values(by='Data')
                df = df.reset_index()
                return df.replace({',': '.'}, regex=True)
            else:
                temp = []
                for k in df['Data']:
                    temp.append(datetime.datetime.strptime(k, '%d/%m/%Y'))
                df['Data'] = temp.copy()
                df = df.sort_values(by='Data')
                df = df.reset_index()

                return df

        def altitude():
            return 10
        def get_startdata():
            if self.type == "format1":
                return self.dataframe["time"][0]
            return self.dataframe['Data'][0]
        def get_enddate():
            if self.type == "format1":
                return self.dataframe["time"][-1]

            if (self.dataframe['Data'][len(self.dataframe) - 1] + datetime.timedelta(days=30)).month == (self.dataframe['Data'][len(self.dataframe) - 1]).month:
                return self.dataframe['Data'][len(self.dataframe) - 1] + datetime.timedelta(days=30)
            return self.dataframe['Data'][len(self.dataframe) - 1] + datetime.timedelta(days=29)
        if not list:
            self.dataframe = dataframe(arquivo)
            self.type = "original"
            self.code = find_cod(pd.read_csv(arquivo, nrows=50, index_col=False,
                                               on_bad_lines='skip', encoding='latin-1'))
            self.fonte = pd.read_csv(arquivo, nrows=2, index_col=False,
                                     on_bad_lines='skip', encoding='latin-1')
            self.startdate = get_startdata()
            self.enddate = get_enddate()
            self.len = len(self.dataframe)
            self.type_data = 'pr'
            self.lat = lat
            self.lon = lon
            self.alt = altitude()
            self.status = None
            self.city = None
            self.state = None
            self.list = list

        else:
            self.path = arquivo
            self.list = arquivo

    # internal functions
    def positions(self):
        if self.list == False:
            raise "This function exists only to list of stations"
        
        lat = np.array([])
        lon = np.array([])
        code = np.array([])
        for i in os.listdir(self.path):
            df = Ana(f"{self.path}/{i}")
            df.get_lonlat()
            lat = np.append(lat, df.lat)
            lon = np.append(lon, df.lon)
            code = np.append(code, df.code)

        df = pd.DataFrame({"code":code, "lat":lat, "lon":lon})
        return df
    def only_mondata(self, list=False):
        """
        Remove all columns that is not referent of month precipitation and day, in original data from Agenci

        :param list:
        :return:
        """

        from datetime import datetime

        if list:
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

        elif list == False:
            df = self.dataframe
            lista_meses = ['Data']
            # adicionamos as colunas dos dados

            for k in range(32):
                'The precipitation data have the name "Chuva" or "Clima", in the row data from month'
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
            self.type_data = "only_mondata"
            self.dataframe = df.drop_duplicates(subset=["Data"])

        else:
            return 'List is only True or False'

    def format1(self, comma_to_dot=True, grow=True, years=(0,0)):
        """
        We change the file format to
        1) put date that can be junped
        2) organize the file from to smaler to larger based in time
        3) Chenge the ',' to '.'
        4) Remove same values from file
        5) Change the name of time variable to time
        6) padronize a file to work with Ana, Inemet, Merge and etc
        7) have option to select a series of year start and year end. The date that not exist, are created and set NaN

        :param comma_to_dot: If the person forgot converto comma to point, can do it now
        :param grow: if want the data with the lower in top and greater in end
        :return: Return to self.dataframe the data reorganized by form:

         Data      dia1     dia2    dia3    dia4    dia5    dia6    dia7 ...
                 1993     0.1      0.3     0.7     0.8     0.6     0.4     0.1
                 1993     0.2      0.9     0.5     0.2     0.1     1.9     9.1
                 1993     0.7      0.2     0.9     0.8     0.7     0.4     0.1
                 .
                 .
                 .

                we change to:

                time        pr
                1997-07-01  0.1
                1997-07-02  0.3
                ....
                ...
                ...
                2020-01-01  0.3
                2020-01-02  0.0

        """

        import pandas as pd
        from datetime import timedelta

        if years != (0,0) and self.type != "format1":
            # Organize the file by date, the lower to greater
            df_ordenado = self.dataframe
            df_ordenado['Data'] = pd.to_datetime(df_ordenado['Data'], format="%d/%m/%Y")
            df_ordenado = df_ordenado.drop_duplicates(subset='Data')

            if comma_to_dot:
                df_ordenado = df_ordenado.replace({',': '.'}, regex=True)
                df_ordenado = df_ordenado.reset_index()
                df_ordenado = df_ordenado.drop(columns='index')
                self.dataframe = df_ordenado
            if not grow:
                self.daframe = df_ordenado.sort_values(by=['Data'], ascending=True)

            data = np.array([])
            pr = np.array([])
            self.only_mondata()

            # remove data that don't exits
            colum = self.dataframe.columns
            n=0
            for linha in range(len(self.dataframe)):
                for dia in range(1, 32):
                    try:
                        temp = self.dataframe[colum[0]][linha]
                        data = np.append(data, datetime.date(temp.year, temp.month, dia))  # check if the date is real
                        pr = np.append(pr, float(self.dataframe[colum[dia]][linha]))
                    except:
                        n+= 0

            # chech if have date jump

            a = pd.date_range(start=self.startdate, end=self.enddate)

            for i in range(len(a)):
                try:
                    while np.datetime64(data[i]) != np.datetime64(a[i]):
                        data = np.insert(data, i, data[i-1]+timedelta(days=1))
                        pr = np.insert(pr, i, 0)
                        pr[i] = np.NaN
                except:
                    continue
            data = pd.date_range(start=data[0], end=data[len(data)-1]) # change data to numpy datetime64
            # select the year series
            if (float(years[0]) in pd.DatetimeIndex(data).year) and (float(years[1]) not in pd.DatetimeIndex(data).year): # The first date is in array and end date not
                if self.startdate != datetime(self.startdate.year, 1,1): # complete missing days start, if don't start in 1/1
                    data = np.concatenate((pd.date_range(start=f"1/1/{int(self.startdate.year)}", end=self.startdate).to_numpy(), data[1:]))
                    a = np.ones(np.size(pd.date_range(start=f"1/1/{int(years[0])}", end=self.startdate).to_numpy()))
                    a[:] = np.nan
                    pr = np.concatenate((a[:-1], pr))
                date = pd.date_range(start=f"01/01/{int(years[0])}", end=f"31/12/{int(years[1])}").to_numpy()

                i = np.where(date[0] == data)[0][0]
                t = np.empty(np.size(date))
                t[:] = np.nan
                t[:len(pr[i:])] = pr[i:]
                pr = t

            elif  float(years[1]) in pd.DatetimeIndex(data).year and float(years[0]) not in pd.DatetimeIndex(data).year: # The end date is in array and first date not
                # complete end date to 31/12 if don't go
                if self.enddate != datetime(self.enddate.year, 12, 31):
                    t = np.empty((datetime(self.enddate.year, 12, 31)-self.enddate).days)
                    t[:] = np.nan
                    pr = np.concatenate((pr, t))
                    data = np.concatenate((data, pd.date_range(start=data[-1], end=f"31/12/{int(self.enddate.year)}")))
                date = pd.date_range(start=f"01/01/{int(years[0])}", end=f"31/12/{int(years[1])}").to_numpy()

                # The index where is the end date
                f = np.where(date[-1] == data)[0][0]

                t = np.empty(len(date))
                t[:] = np.nan
                t[-len(data[:f]):] = pr[:f]
                pr = t

            elif float(years[1]) not in pd.DatetimeIndex(data).year and float(years[0]) not in pd.DatetimeIndex(data).year: # The end date is not in array and first date not in
                date = pd.date_range(start=f"01/01/{int(years[0])}", end=f"31/12/{int(years[1])}").to_numpy()

                # The index of dates that we have data
                i = np.where(data[0]== date)[0][0]
                f = np.where(data[-1] == date)[0][0]
                t = np.empty(np.size(date)) # will be precipitation data
                t[:] = np.nan
                # armazene the data
                date[i:f] = data[:-1]
                t[i:f] = pr[:-1]

                # Change the variable name
                pr = t

            else: # both dates are in array

                if self.startdate.date != datetime.date(self.enddate.year, 1,1): # complete missing days start, if don't start in 1/1
                    data = np.concatenate([pd.date_range(start=f"1/1/{self.startdate.year}", end=self.startdate).to_numpy(), data[1:]])
                    a = np.ones(np.size(pd.date_range(start=f"1/1/{self.startdate.year}", end=self.startdate).to_numpy()))
                    a[:] = np.nan
                    pr = np.concatenate([a[:-1], pr])

                if self.enddate.date != datetime.date(self.enddate.year, 12, 31):
                    t = np.empty(len(pd.date_range(start=data[-1], end=f"31/12/{self.enddate.year}")[1:]))
                    t[:] = np.nan
                    pr = np.concatenate((pr, t))
                    data = np.concatenate((data[:], pd.date_range(start=data[-1], end=f"31/12/{self.enddate.year}")[1:]))
                date = pd.date_range(start=f"01/01/{int(years[0])}", end=f"31/12/{int(years[1])}").to_numpy()

                i = np.where(date[0] == data)[0][0]
                f = np.where(date[-1] == data)[0][0]

                date = data[i:f]
                pr = pr[i:f]

            self.dataframe = pd.DataFrame(list(zip(date, pr)), columns=['time', 'pr'])

            # atualize the format and len
            self.type = "format1"
            self.len = len(self.dataframe)
        elif self.type != 'format1': # If the data is not the format1
            # Organize the file by date, the lower to greater
            df_ordenado = self.dataframe
            df_ordenado['Data'] = pd.to_datetime(df_ordenado['Data'], format="%d/%m/%Y")
            df_ordenado = df_ordenado.drop_duplicates(subset='Data')

            if comma_to_dot:
                df_ordenado = df_ordenado.replace({',': '.'}, regex=True)
                df_ordenado = df_ordenado.reset_index()
                df_ordenado = df_ordenado.drop(columns='index')
                self.dataframe = df_ordenado
            if grow:
                self.daframe = df_ordenado.sort_values(by=['Data'], ascending=True)

            data = np.array([])
            pr = np.array([])
            self.only_mondata()

            # indução
            colum = self.dataframe.columns
            for linha in range(len(self.dataframe)):
                for dia in range(1, 32):
                    try:
                        temp = self.dataframe[colum[0]][linha]
                        data = np.append(data, datetime.datetime(temp.year, temp.month, dia)) # check if the date is real
                        pr = np.append(pr, float(self.dataframe[colum[dia]][linha]))
                    except:
                        continue

            # chech if have date jump
            a = pd.date_range(start=self.startdate, end=self.enddate)

            for i in range(len(a)):
                try:
                    while np.datetime64(data[i]) != np.datetime64(a[i]):
                        data = np.insert(data, i, data[i - 1] + timedelta(days=1))
                        pr = np.insert(pr, i, 0)
                        pr[i] = np.NaN
                except:
                    continue
            data = pd.date_range(start=self.startdate, end=self.enddate)  # change data to numpy datetime64
            self.dataframe = pd.DataFrame(list(zip(data, pr)), columns=['time', 'pr'])
            # atualize the format and len
            self.type = "format1"
            self.len = len(self.dataframe)

    def date(self, line):
        """
        This function get a especific date in a line
        :param linha:
        :return:
        """

        from datetime import datetime
        if self.type_data in ["original", "only_mondata"]:
            return self.dataframe["Data"][line]
        else:
            return self.dataframe['time'][line]
    def where(self, date):
        """
        Return the index where is the date
        :param date: date in datetime.datetime format
        :return:
        """
        self.format1()
        return np.where(self.dataframe()['time'] == date)
    def empty_data(self, type='relative'):
        if self.type_data == "format1":
            t = np.sum(np.isnan(self.dataframe['pr'].to_numpy("float32")))
            return (t/self.len)*100
        else:
            self.only_mondata()
            s = 0
            for i,c in enumerate(self.dataframe.columns):
                if c!="Data" and c!= "Chuva31" and c!= "Chuva30" and c!= "Chuva29":
                    s += np.sum(np.isnan(self.dataframe[f'{c}'].to_numpy("float32")))
            print("You are using the original data and this is a estimative, use format1 before to be precise")
            if type == "relative":
                return s
            return (s/(self.enddate-self.startdate).days)*100

    # select data or return a data
    def get_year(self,year, with_x=False, return_x0=False):
        """
        From array muti-year, return a year specific
        :param year: can by a Int, or list of Int
        :param with_x:
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
        From array muti-year, return a month specific
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
    def get_lonlat(self, by="Código"):
        """
        The data was get by web http://telemetriaws1.ana.gov.br/EstacoesTelemetricas.aspx in oct 2022
        and is save with name "estacoes.csv"
        and save in self.lat and self.lon, that before are None
        :param by: what will be used to find latitude and longitude
        :return:
        """
        if by=="Código":
            data = pd.read_csv("ana/estacoes.csv")
            data = data.query(f"Código=={self.code}")
            self.lat = float(data["Y"])
            self.lon = float(data["X"])
            self.city = data["Município"]
            self.state = data["Estado"]
            self.status = data["Operando"]

    #Save
    def to_netcdf4(self, path):
        import xarray as xr
        self.format1()

        # pr to float
        df = self.dataframe
        df["pr"] = np.array(df['pr']).astype(float)

        # Run to get lat and lon, create the array of position
        self.get_lonlat()
        lat = [self.lat] * self.len
        lon = [self.lon] * self.len
        df['lat'] = lat
        df['lon'] = lon

        # opening the df with xarray
        ds = df.set_index(['time', 'lat', 'lon']).to_xarray()

        ds = xr.Dataset(ds)
        # add variable attribute metadata
        ds.attrs['lat'] = 'Units: °'
        ds.attrs['lon'] = 'Units: °'
        ds.attrs['time'] = 'daily data of time'

        ds.to_netcdf(path)

    def to_csv(self, pasta, sep=';', index=False, var="all"):
        if var=="all":
            self.dataframe.to_csv(pasta, sep=sep, index=index)
        else:
            a = self.dataframe[f"{var}"].to_csv(pasta, sep=sep, index=index)

    def haversine(self, lon1, lat1):
        """
        Calculate the great circle distance in kilometers between a point and the stations self
        on the earth (specified in decimal degrees)
        
        :param lon1: float, position longitude
        :param lat1: float, position latitude
        """

        lon2, lat2 = self.lon, self.lat 
        from math import cos, sin, asin, sqrt, radians
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a3 = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a3))
        r = 6371  # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
        return c * r

    def plot(self, title='', xlabel='', ylabel=''):
        """
        This function help with fast plot, to more detalhe use the matplotlib
        :param title:
        :param xlabel:
        :param ylabel:
        :return: Return the graphic of data saved in self.dataframe
        """

        import matplotlib.pyplot as plt
        if self.list == False:
            from matplotlib import pyplot as plt
            if self.type != "format1":
                self.format1()

            y = self.dataframe.iloc[:,1]
            x = self.dataframe.iloc[:,0]
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.tight_layout()
            plt.plot(x, y)
            plt.show()

        else:
            df = self.positions() # will return a dataframe with code, latitude, longitude
            gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.lon, df.lat))
            
            world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
            ax = world[world.continent == 'South America'].plot(
    color='white', edgecolor='black')

            # We can now plot our ``GeoDataFrame``.
            gdf.plot(ax=ax, color='red')

            plt.show()


    def mean(self, with_x=False, retornar=True):
        """
        Calculate the media when the 'arquivo' is a list of many Ana file
        :param with_x:
        :param retornar:
        :return:
        """
        import os
        from AgenciBr.Ana import Ana
        li = os.listdir(self.path)
        start=datetime.date(2090,12,2)
        end=datetime.date(1902,12,2)
        size=0
        for i in li: # get the size of array
            a = Ana(self.path+'/'+i)
            if a.startdate< start:
                start = a.startdate
            if a.enddate > end:
                end = a.enddate

        x = np.arange(start, end, np.timedelta64(1, "D")) # the time array
        y = np.zeros(x.size)
        d = np.zeros(x.size)

        for i in li:  # get the size of array
            a = Ana(self.path + '/' + i)
            a.format1()
            k2= 0
            for i2, k in enumerate(x):
                if pd.to_datetime(k) == a.dataset['time'][k2]:  # se encontramos o intervalo que é idêntico
                    y[i2] += a.dataset['pr'][k2]
                    d[i2] += 1
                    k2 +=1

        # divide by d
        for k in range(size):

            y[k] = y[k]/d[k]
        if retornar:
            if with_x:
                return x, y
            return y
        print(x.size, y.size)
        self.dataframe = pd.DataFrame(zip(x.tolist(), y.tolist()), columns=['time', 'pr'])
        print(self.dataframe)
        self.type_data = 'format1'

    # Download data
    def download(self,codigo="NaN", format='csv', dir='', tipo_especifico=False, save_zip=False,
                 state="NaN", city="Nan"):
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
        if codigo != "NaN":
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
                params = {'tipo': 3, 'documentos': codigo}
                r = requests.get(BASE_URL, params=params)
            elif format == 'txt':
                params = {'tipo': 2, 'documentos': codigo}
                r = requests.get(BASE_URL, params=params)
            elif format == 'mdb':
                params = {'tipo': 1, 'documentos': codigo}
                r = requests.get(BASE_URL, params=params)
            else:
                raise "the data format is not csv , mdb or txt"

            # Check if the code exist in Ana file
            if not isinstance(r.content, bytes):
                print(f'Arquivo {codigo} inválído')
                return

            # if save_zip is true, save zip
            if save_zip:
                print(f'Salvando dados {codigo} como zip')
                with open(f'{dir}estacao_{codigo}.zip', 'wb') as f:
                    f.write(r.content)
            # else, unpack each zip file
            else:
                print(f'Extraindo dados da estação {codigo} do zip')
                unzip_station_data(r.content, dir, tipo_especifico)
        else: # we download a list of data
            if state != "NaN":
                estado = f"-{state.upper()}"
                df = pd.read_html("ana/EstacoesTelemetricas_Todas_19_10_2022.xls")
                df = df[0]
                df = df[df["Municipio-UF"].str.contains(estado, na=False)]
                codes = df["CodEstacao"].to_numpy()
                # for each code in list, we download
                for i in codes:
                    a = Ana(self.path, list=True)
                    a.download(codigo=i, format=format, dir=dir,tipo_especifico=False, save_zip=False)
            elif city != "NaN":
                cidade = f"{city.upper()}"
                df = pd.read_html("ana/EstacoesTelemetricas_Todas_19_10_2022.xls")
                df = df[0]
                if state != "NaN":
                    df = df[df["Municipio-UF"].str.contains(f"-{state}", na=False)]
                df = df[df["Municipio-UF"].str.contains(cidade, na=False)]
                codes = df["CodEstacao"].to_numpy()
                # for each code in list, we download
                for i in codes:
                    a = Ana(self.path, list=True)
                    a.download(codigo=i, format=format, dir=dir, tipo_especifico=False, save_zip=False)

    # Extreme index
    def rx5day(self, with_x=False, retornar='number_of_5day_heavy_precipitation_periods_per_time_period'):
        from AgenciBr.indice import Indice
        if self.list:
            fazer=0
        if self.type_data != 'format1':
            self.format1()

        ind = Indice(self.dataframe)
        ind = ind.rx5day(with_x=with_x, retornar=retornar)
        return ind
    def cdd(self, with_x=False):
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataframe)
        ind = ind.cdd(with_x=with_x)
        return ind
    def cwd(self, with_x=False):
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataframe)
        ind = ind.cwd(with_x=with_x)
        return ind
    def prcptot(self, with_x=False):
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataframe)
        ind = ind.prcptot(with_x=with_x)
        return ind
    def prcptot_monthly(self, with_x=False):
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataframe)
        ind = ind.prcptot_monthly(with_x=with_x)
        return ind
    def r99p(self, with_x=False):
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataframe)
        ind = ind.r99p(with_x=with_x)
        return ind
    def rnnmm(self, number, with_x=False):
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataframe)
        ind = ind.rnnmm(number=number, with_x=with_x)
        return ind
    def r10mm(self, with_x=False):
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataframe)
        ind = ind.r10mm(with_x=with_x)
        return ind
    def r20mm(self, with_x=False):
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataframe)
        ind = ind.r20mm(with_x=with_x)
        return ind
    def r99ptot(self, with_x=False):
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataframe)
        ind = ind.r99pTOT(with_x=with_x)
        return ind
    def rx1day_anual(self, with_x=False):
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataframe)
        ind = ind.rx1day_anual(with_x=with_x)
        return ind
    def rx1day_monthly(self, with_x=False):
        from AgenciBr.indice import Indice
        self.format1()
        ind = Indice(self.dataframe)
        ind = ind.rx1day_monthly(with_x=with_x)
        return ind

    #list functions
    def to_climatol(self, path, years):
        """
        homogen('pr', 2003, 2021, expl = TRUE)
        :param path: path to file to save
        :param years: tuple with start year and end year
        :return:
        """
        if self.list == False:
            raise "This function need a list of stations, change list=True and see the documentation"
        else:
            import os
            posi = []
            for i, k in enumerate(os.listdir(self.path)):
                if i == 0:
                    a = Ana(self.path + "/" + k)
                    a.format1(years=years)
                    a.get_lonlat()
                    data = np.array([a.dataframe["pr"]])
                    posi.append([a.lat, a.lon, a.alt, f"{a.code}", f"Ana-{a.code}"])
                else:
                    a = Ana(self.path+"/"+k)
                    a.format1(years=years)
                    a.get_lonlat()
                    # This condiction is to correct a error
                    if len(a.dataframe["pr"]) > len(data[0]) and np.isnan(a.dataframe["pr"][a.len-1]):
                        data = np.append(data, [a.dataframe["pr"][:-1]], axis=0)
                        posi.append([a.lat, a.lon, a.alt, f"{a.code}", f"Ana-{a.code}"])
                    else:
                        data = np.append(data, [a.dataframe["pr"]], axis=0)
                        posi.append([a.lat, a.lon, a.alt, f"{a.code}", f"Ana-{a.code}"])


            a = pd.DataFrame(np.transpose(data))
            b = pd.DataFrame(posi)

            #Before to save, climatol find empty place with some word in string "nan". Because this, we change to str
            a = a.astype(str)
            b = b.astype(str)
            a.to_csv(path+f"/Ttest_{years[0]}-{years[1]}.dat", index=False, header=False, sep=" ")
            a.to_csv(path + f"/pr_{years[0]}-{years[1]}.dat", index=False, header=False, sep=" ")
            b.to_csv(path+f"/pr_{years[0]}-{years[1]}.est", index=False, header=False, sep=" ")

        with open("ana/climatol.r", "w") as climatol:
            climatol.write(f"""
            library(climatol)

            #------------------------------------------------------
            setwd("{self.path}")
            
            dat <- as.matrix(read.table("pr_{years[0]}-{years[1]}.dat"))
            write(dat, "Ttest_{years[0]}-{years[1]}.dat")
            
            homogen('pr', {years[0]}, {years[1]}, expl = TRUE)

            """)
            climatol.close()
        os.system("Rscript ana/climatol.r")

def dist(x1,x2):
    return x1.heaversine(x2.lon, x2.lat)

