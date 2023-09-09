import indice
import pandas as pd

df = pd.read_csv("/home/cpa/Documentos/ana_260009.csv")
i = indice.Indice(df.iloc[:,0], df.iloc[:,1])
print(i.tx(with_x=True))