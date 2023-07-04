# AgenciBr

> The objective is create a package that help to usa data of **Agencia Nacional de Águas (ANA)**, **Instituto Nacional de Meteorologia (INEMET)**, **Merge**, **Brazilian Daily Weather Gridded Data (BR-DWGD)** and **Instituto de Hidrología, Meteorología y Estudios Ambientales (IDEAM)**. All the data above is from Brazil, minus the **IDEAM** that is from Colombia.
 
 - **ANA** [https://www.gov.br/ana/pt-br] or [https://www.snirh.gov.br/hidroweb/apresentacao]
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
data.dataset # return the dataset

data.code #Return the 

data.startdate #return the first date from dataset

data.enddate  #return the end date from dataset

data.len #return the length from dataset

data.type_data #return the data informations (precipitation, temperature, t_maxmin, wind, ...)

data.type #return if data is original, format1, format2 ...
```

**Import Inemet**

```python
from AgenciBr import Inemet

data = Inemet.Inemet('path file')
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

**Suported functions**

|Agenci| Precipitacion | vazão | Temperature(mean) | Temperature (minimun, maximum)|
|------|---------------|-------|-------------------|-------------------------------|
| Ana  | [x]           |[ ]    |      [ ]          |            [ ]                |
|Inemet|      [x]      |       |      [x]          |                               |
|Merge |   [ ]         | [ ]   |      [ ]          |            [ ]                |
|Alexandre|  [ ]       |  [ ]  |       [ ]         |     [ ]                       |
| Ideam|  [ ]          | [ ]   |        [ ]        |        [ ]                    |
 

From internal function we construct function1, functon2

  
 
 
### Internal functions

## Format1
We work with distints data and dataframe models, bacause this, was create the function format1 in each agenci.
This function have three param:
- **Comma_to_dot**: change the comma of all file to dot and to float number
- **grow**: Change the dataframe from de lower to larger
- **years**: is a vector of two numbers (year1, year2) that you wish be the start and end, the year can be the future

**The principal objective of this function is**
1) put date that can be jumped
2) organize the file from to smaler to larger based in time 
3) Change the ',' to '.'
4) Remove same values from file
5) Change the name of time variable to time
6) padronize a file to work with Ana, Inemet, Merge and etc
7) have option to select a series of year start and year end. The date that not exist, are created and set NaN

**The outfile have format precipitation**
```python
                         time        pr
                        1997-07-01  0.1
                        1997-07-02  0.3
                        ....
                        ...
                        ...
                        2020-01-01  0.3
                        2020-01-02  0.0

```
**The outfile have format temperature**
```python
                                time   max   min
                    0     1961-01-01   NaN   NaN
                    1     1961-01-02   NaN   NaN
                    2     1961-01-03   NaN   NaN
                    3     1961-01-04   NaN   NaN
                    4     1961-01-05   NaN   NaN
                    ...          ...   ...   ...
                    22276 2021-12-28  28.7  21.6
                    22277 2021-12-29  29.3  21.6
                    22278 2021-12-30  26.9  21.8
                    22279 2021-12-31  32.3  21.6
                    22280 2022-01-01  27.6  23.8
                    
                    [22281 rows x 3 columns]
```
## Format2
We work with datasets, to padronize, we create the function format2 that exists only when you are working with dataset files.

### Climate Indices

| Indices | Ana | Inemet | Xavier | Merge | IDEAM |
| ------- | --- | ------ | ------ | ----- | ----- |
| TXX     |     | [X]    |        |       |    [X]   |
| TNX     |     | [X]    |        |       | [X]      |
| TX90P   |     | [X]    |        |       |     [X]  |
| TN90P   |     | [X]    |        |       |     [X]  |
| CDD     | [X] |        |        |       |       |
| CWD     | [X] |        |        |       |      |
| PRCPTOT | [X] |        |        |       |     [X]  |
| RX5DAY  | [X] |        |        |       |   [X]    |
| TN10P   |     |        |        |       |       |
| FD      |     |        |        |       |       |
| SU      |     |        |        |       |       |
| ETR     |     |        |        |       |       |
| RNNMM   |     |        |        |       |       |
| R99P    |     |        |        |       |       |
| R95P    |     |        |        |       |       |
| R10MM   |     |        |        |       |       |
| R20MM   |     |        |        |       |       |
| R99PTOT |     |        |        |       |       |


