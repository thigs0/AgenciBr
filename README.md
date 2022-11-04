# AgenciBr

> The objective is create a package that help to usa data of **Agencia Nacional de Águas (ANA)**, **Instituto Nacional de Meteorologia (INEMET)**, **Merge**, **Brazilian Daily Weather Gridded Data (BR-DWGD)** and **Instituto de Hidrología, Meteorología y Estudios Ambientales (IDEAM)**. All the data above is from Brazil, minus the **IDEAM** that is from Colombia.
 
 - **ANA** [https://www.gov.br/ana/pt-br]
 - **INEMET** [https://portal.inmet.gov.br]
 - **MERGE** [http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/DAILY/]
 - **BR-DWGD** [https://github.com/AlexandreCandidoXavier/BR-DWGD]
 - **IDEAM** [http://www.ideam.gov.co]

**Usage**
> pip install AgenciBr  

In python:

**Import Ana**
```python
from AgenciBr import Ana.Ana
data = Ana.Ana('path file')

""" Properties """
A.dataset # return the dataset

A.code #Return the 

A.startdate #return the first date from dataset

A.enddate  #return the end date from dataset

A.len #return the length from dataset

A.type_data #return the data informations (precipitation, temperature, wind, ...)
```

**Import Inemet**

```python
from AgenciBr import Inemet

a = Inemet.Inemet('path file')
```

   **Import Merge**
 ```python
 from AgenciBr import Merge

data = Merge.Merge('path file')
 ```
 
 **Import Alexandre**
 ```python
 from AgenciBr import Alexandre

data = Alexandre.Alexandre('path file')
 ```
 
**Import Ideam**

```python
from AgenciBr import Ideam

data = Ideam.Ideam('path file')
```


 
 
