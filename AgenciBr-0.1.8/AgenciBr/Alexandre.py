import os
import xarray as xr
import numpy as np
import pandas as pd

class Alexandre:
    def __init__(self, path, var=None, lon=None, lat=None):
        def opening(path, var):
            if path[-3:] == '.nc': # se é um arquivo individual
                return xr.open_dataset(self.path)
            elif var != None: # A pessoa colocou uma variável para multi arquivos
                return xr.open_mfdataset(self.path + '/'+var + '*.nc')
        self.path = path
        self.var = var
        self.dataset = opening(self.path, var=var)
        self.lat = lat
        self.lon = lon

    def dowload_data(self):
        # ainda construir
        import requests
        def download_file(url, endereco, nome):
            # acessa o site
            resposta = requests.get(url)
            # Acessa o conteúdo e salva em um arquivo
            if resposta.status_code == requests.codes.OK:
                with open(endereco + f'/{nome}.grip2', 'wb') as novo:
                    novo.write(resposta.content)
            else:
                resposta.raise_for_status()

    def open_mfdataset(self, var):
        """
        Open many files .nc in one.
        :param var: string with name of variable
        :return:
        """
        self.dataset = xr.open_mfdataset(self.path + var + '*.nc')

    def open_dataset(self):
        """
        Open the dataset
        :return:
        """
        self.dataset = xr.open_dataset(self.path)

    def sum_month(self, v):
        # testar
        import datetime
        df = self.dataset
        mes = pd.to_datetime(df.time.values[0]).month  # primeiro mês
        soma = 0
        t = var = np.array([])
        size = len(df.time.values)
        ano = pd.to_datetime(df.time.values[0]).year
        for k in range(len(df.time.values)):
            if pd.to_datetime(df.time.values[k]).month != mes:
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
            soma += df[v].values.transpose()[0][k]
        return xr.DataArray(var,coords=[t], dims=["time"])

    def to_csv(self, name, var=None):
        """
        Convert the file in .csv files
        :param name:
        :param var:
        :return:
        """
        if var == None:
            raise "Digite a variável (var) que será usada quando abre o arquivo"
        if isinstance(var, list): # Se é uma lista de variáveis
            if self.lon and self.lat != None:
                for n, var_name2get in enumerate(var):
                    var2get_xr = xr.open_mfdataset(self.path + var_name2get + '*.nc')
                    # a = var2get_xr.to_dataframe()
                    if n == 0:
                        var_ar = var2get_xr[var_name2get].sel(longitude=self.lon,latitude=self.lat,method='nearest').values

                        var_ar = [var_ar.tolist()]
                        time = [var2get_xr.time.values]
                    else:

                        t = var2get_xr[var_name2get].sel(longitude=self.lon,latitude=self.lat,method='nearest').values
                        var_ar = var_ar.append(t.tolist())
                        del t
                for n in range(1):
                    file = var_ar
                    pd.DataFrame(file, index=time, columns=var).to_csv(name, float_format='%.1f')

        if self.lon== None and self.lat == None:
            c=0
            for lat in range(self.dataset.lat.values):
                for lon in range(self.dataset.lon.values):
                    if c==0: # Caso inicial
                        a = self.dataset[var].sel(longitude=xr.DataArray(lon, dims='z'),
                                                  latitude=xr.DataArray(lat, dims='z'),
                                                  method='nearest').values
                        final = np.array(a)
                        del a
                    else: # Casos seguintes
                        a = self.dataset[var].sel(longitude=xr.DataArray(lon, dims='z'),
                                      latitude=xr.DataArray(lat, dims='z'),
                              method='nearest').values
                        final = np.c_[final, a]
                        del a
            if ~np.isnan(final[:, 0]):
                file = final[:, 0]
                pd.DataFrame(file, index=time, columns=var).to_csv(name, float_format='%.1f')

        else:
            a = self.dataset[var].sel(longitude=xr.DataArray([self.lon], dims='z'),
                              latitude=xr.DataArray([self.lat], dims='z'),
                              method='nearest').values
            final= np.array(a)
            del a
            pd.DataFrame(list(zip(self.dataset.time.values,final[:,0])), columns=['time',var]).to_csv(name, index=False)
    def to_netcdf(self, path):
        if self.var == None:
            raise "Type a variable (var) that will be used when open the file"
        t = self.dataset[self.var].sel(longitude=xr.DataArray([self.lon], dims='z'),
                              latitude=xr.DataArray([self.lat], dims='z'),
                              method='nearest').to_netcdf(path)

    #Climate index
    def prcptot(self, with_x=False):
        import Indice
        if self.var != 'pr':
            raise "Is necessary to use the precipitation data (pr)"
        self.to_csv('temp.nc', var=self.var)
        a = indice.indice(pd.read_csv('temp.nc'))
        x,y = a.prcptot(with_x=with_x)
        os.remove('temp.nc')
        return x,y
    def cwd(self, with_x=False):
        import Indice
        if self.var != 'pr':
            raise "Is necessary to use the precipitation data (pr)"
        self.to_csv('temp.nc', var=self.var)
        a = indice.indice(pd.read_csv('temp.nc'))
        x, y = a.cwd(with_x=with_x)
        os.remove('temp.nc')
        return x, y
    def cdd(self, with_x=False):
        import Indice
        if self.var != 'pr':
            raise "Is necessary to use the precipitation data (pr)"
        self.to_csv('temp.nc', var=self.var)
        a = indice.indice(pd.read_csv('temp.nc'))
        x, y = a.cdd(with_x=with_x)
        os.remove('temp.nc')
        return x, y
    def rx5day(self, with_x=False, time='y'):
        import Indice
        if self.var != 'pr':
            raise "Is necessary to use the precipitation data (pr)"
        self.to_csv('temp.nc', var=self.var)
        a = indice.indice(pd.read_csv('temp.nc'))
        x, y = a.rx5day(with_x=with_x)
        os.remove('temp.nc')
        return x, y
    def tx(self, with_x=False):
        import Indice
        print(self.var)
        if self.var.lower in ['t_maxmin' ,'tmax']:
            raise "Is necessary to use the maximum temperature data (Tmax)"
        self.to_csv('temp.nc', var=self.var)
        a = indice.indice(pd.read_csv('temp.nc'))
        x, y = a.TX(with_x=with_x, var= self.var)
        os.remove('temp.nc')
        return x, y
    def tn(self, with_x=False):
        import Indice
        if self.var.lower in ['t_maxmin', 'tmin']:
            raise "Is necessary to use the minimum temperature data (Tmin)"
        self.to_csv('temp.nc', var=self.var)
        a = indice.indice(pd.read_csv('temp.nc'))

        x, y = a.TN(with_x=with_x, var=self.var)
        os.remove('temp.nc')
        return x, y
    def tx90p(self, with_x=False):
        import Indice
        if self.var.lower in ['t_maxmin', 'tmax']:
            raise "Is necessary to use the maximum temperature data (Tmax)"
        self.to_csv('temp.nc', var=self.var)
        a = indice.indice(pd.read_csv('temp.nc'))
        x, y = a.TX90p(with_x=with_x, var=self.var)
        os.remove('temp.nc')
        return x, y
    def tn90p(self, with_x=False):
        import Indice
        if self.var.lower in ['t_maxmin', 'tmax']:
            raise "Is necessary to use the maximum temperature data (Tmax)"
        self.to_csv('temp.nc', var=self.var)
        a = indice.indice(pd.read_csv('temp.nc'))
        x, y = a.TN90p(with_x=with_x, var=self.var)
        os.remove('temp.nc')
        return x, y

