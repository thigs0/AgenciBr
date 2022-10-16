class Trat_Netcdf: ''


def __init__(self, dataset=0):
    self.dataset = dataset
    self.show = print(self.dataset)


'''def netcdf_to_txt(self, output_loc, Have_bnds=True, remove_bnds=True, to_mm=True):

    Aqui temos o modo como converteremos netcdf para txt.

    Leremos o arquivo para uma latitude e longitude, criaremos um txt com os dados.
    Para as latitudes e longitudes diferentes, vamos somando ao txt criado

    import numpy as np
    import pandas as pd
    ds = self.dataset
    cont = 0
    tempo = []
    precipitacao = []

    for k in (ds.time.values):
        k = str(k)
        tempo.append(k[0:10])

    if Have_bnds == True:
        if remove_bnds == True:
            ds = ds.drop_dims('bnds')
        else:
            '#do nothing'

    for a in range(len(ds.lat.values)):  # percorre a latitude
        for b in range(len(ds.lon.values)):  # percorre a longitude:
            lat_temp = ds.lat.values[a]
            lon_temp = ds.lon.values[b]

            for l in range(len(tempo)):
                if to_mm == True:
                    k = (ds.pr.isel(lat=a, lon=b, time=l).values) * 24 * 60 * 60
                    k = np.around(k)
                    precipitacao.append(k)
                else:
                    k = ds.pr.isel(lat=a, lon=b, time=l).values
                    precipitacao.append(k)

            temp = ds.isel(lat=a, lon=b).to_dataframe()
            temp = pd.DataFrame(temp)
            lon = [lon_temp] * len(tempo)
            lat = [lat_temp] * len(tempo)

            k = pd.DataFrame(list(zip(tempo, lat, lon, precipitacao)),
                             columns=['tempo', 'Latitude', 'Longitude', 'precipitação'])
            # print(k)
            temp = k.to_csv(sep='\t', index=False)
            if cont == 0:
                text = open(f'{output_loc}.txt', 'w', newline='')
                text.write(f'{temp}')
                text.close()
            else:
                text = open(f'{output_loc}.txt', 'a', newline='')
                text.write(f'{temp}')
                text.close()
            cont += 1
'''


def Slice(self, output_archive, name_out):
    ds = self.dataset
    lats = ds.lat.values
    lons = ds.lon.values
    times = ds.time.values
    cont = 0
    ds = ds.drop_vars('time_bnds')
    ds = ds.drop_vars('lat_bnds')
    ds = ds.drop_vars('lon_bnds')

    # separa o arquivo histórico em menores
    for a in range(lats.size):
        for b in range(lons.size):
            temp = ds.isel(lat=a, lon=b)
            temp.to_netcdf(f'{output_archive}/{name_out}_{cont}.nc')
            cont += 1


def plot_pr(self):
    from matplotlib import pyplot as plt
    time = self.dataset.time.values

    pr = []
    for k in self.dataset.pr.values:
        pr.append(float(k))

    plt.plot(time, pr)
    plt.show()


def plot_temp(self):
    from matplotlib import pyplot as plt
    time = self.dataset.time.values

    tas = []
    for k in self.dataset.tas.values:
        tas.append(float(k))

    plt.plot(time, tas)
    plt.show()


def corelation_pre_temp(self):
    print(5)


def get_point(self, lat_ind, lon_ind):
    self.dataset = self.dataset.isel(lat=lat_ind, lon=lon_ind)


def aglutinar(self, path, saida, arredondar=3):
    import os
    import xarray as xr
    import pandas as pd
    import numpy as np
    lat_f = []
    lon_f = []
    prec_f = []
    time_f = []
    for k in os.listdir(path):
        print(k[-2:])
        if k[-2:] == 'nc':
            ds = xr.open_dataset(f'{path}/{k}')
            time_temp = []
            prec_temp = []
            for k in range(ds.time.values.size):
                time_temp.append(str(ds.time.values[k])[:7])
            lat_temp = [np.round(ds.lat.values, 2)] * (len(time_temp))
            lon_temp = [ds.lon.values] * (len(time_temp))

            for k in range(ds.pr.values.size):
                prec_temp.append(round(float(ds.pr.values[k]) * 86400, arredondar))
            lat_f += lat_temp.copy()
            lon_f += lon_temp.copy()
            time_f += time_temp.copy()
            prec_f += prec_temp.copy()
    df = pd.DataFrame(list(zip(time_f, lat_f, lon_f, prec_f)),
                      columns=['Tempo(ano-mês)', 'Latitude', 'Longitude', 'Precipitação (mm)'])

    df.to_csv(f'{path}/{saida}.txt', sep='\t', index=False)


def to_txt(self, path, out, arredondar=3, var='prec'):
    import os
    import xarray as xr
    import pandas as pd
    import numpy as np
    if var == 'prec':

        list_temp = []
        cont_ext = 0
        #
        for k in os.listdir(path):
            if k[-2:] == 'nc':
                ds = xr.open_dataset(f'{path}/{k}')
                lats = ds.lat.values
                lons = ds.lon.values
                times = ds.time.values
                cont = 0
                ds = ds.drop_vars('time_bnds')
                ds = ds.drop_vars('lat_bnds')
                ds = ds.drop_vars('lon_bnds')

                # separa o arquivo histórico em menores
                for a in range(lats.size):
                    for b in range(lons.size):
                        temp = ds.isel(lat=a, lon=b)
                        temp.to_netcdf(f'{path}/TXT_{cont_ext}_{cont}.nc')
                        list_temp.append(f'{path}/TXT_{cont_ext}_{cont}.nc')
                        cont += 1
            cont_ext += 1
        # Aglutina
        lat_f = []
        lon_f = []
        prec_f = []
        time_f = []
        for k in os.listdir(path):
            if k[-2:] == 'nc' and k[0:3] == 'TXT':
                ds = xr.open_dataset(f'{path}/{k}')
                time_temp = []
                prec_temp = []
                for k in range(ds.time.values.size):
                    time_temp.append(str(ds.time.values[k])[:7])
                lat_temp = [np.round(ds.lat.values, 2)] * (len(time_temp))
                lon_temp = [ds.lon.values] * (len(time_temp))

                for k in range(ds.pr.values.size):
                    prec_temp.append(round(float(ds.pr.values[k]) * 86400, arredondar))
                lat_f += lat_temp.copy()
                lon_f += lon_temp.copy()
                time_f += time_temp.copy()
                prec_f += prec_temp.copy()
        df = pd.DataFrame(list(zip(time_f, lat_f, lon_f, prec_f)),
                          columns=['Tempo(ano-mês)', 'Latitude', 'Longitude', 'Precipitação (mm)'])

        df.to_csv(f'{path}/{out}.txt', sep='\t', index=False)
        ########
        for k in list_temp:
            os.remove(k)
    elif var == 'temp':
        lat = []
        lon = []
        time = []
        tas = []
        for k in os.listdir(path):
            if k[-2:] == 'nc':
                a = xr.open_dataset(
                    f'{path}/{k}')
                a = a.to_dataframe()
                a = pd.DataFrame(a)
                a = a.reset_index()
                a = a.drop(columns=['lon_bnds', 'lat_bnds', 'time_bnds', 'height', 'bnds'])
                a = a.drop_duplicates()
                a = a.sort_values(by=['lat', 'lon', 'time'])
                print(a)
                for k2 in a.time:
                    time.append(str(k2)[:7])
                for k2 in a.tas:
                    tas.append(round(k2 - 273, 2))
                for k2 in a.lat:
                    lat.append(round(k2, 2))
                for k2 in a.lon:
                    lon.append(round(k2, 2))
        a = pd.DataFrame(list(zip(time, lat, lon, tas)), columns=['time(ano-mês)',
                                                                  'lat',
                                                                  'lon',
                                                                  'tas(ºC)'])
        a.to_csv(f'{path}/{out}', sep='\t', index=False)


def clean(self):
    import gc
    gc.collect(generation=2)


def save(self, local):
    self.dataset.to_netcdf(local)


path = '/home/thigs/Downloads/ests/INEMET/Dados_INEMET_Convencionais/Precipitação/Benjamin_constant'

from Python.AgenciBr.Trat_ANA import TratAna

a = TratAna(f'/home/thigs/Downloads/ests/ANA/Medicoes_convencionais_Manaus_ANA', skiprows=10, encoding='latin-1')
a.only_MonData()
a.show()
a.dados_to_padrao(virgula_para_ponto=True, crescente=False)
print(a.station_distance(a))
