# AgenciBr

> The objective is create a package that help to usa data of **Agencia Nacional de Águas (ANA)**, **Instituto Nacional de Meteorologia (INEMET)**, **Merge**, **Brazilian Daily Weather Gridded Data (BR-DWGD)** and **Instituto de Hidrología, Meteorología y Estudios Ambientales (IDEAM)**. All the data above is from Brazil, minus the **IDEAM** that is from Colombia.
 
 - **ANA** [https://www.gov.br/ana/pt-br] or [https://www.snirh.gov.br/hidroweb/apresentacao]
 - **INEMET** [https://portal.inmet.gov.br]
 - **MERGE** [http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/DAILY/]
   
   More:
    http://ftp.cptec.inpe.br/modelos/tempo/MERGE/rozante_et.al.2010.pdf
 - **BR-DWGD** [https://github.com/AlexandreCandidoXavier/BR-DWGD]
 - **IDEAM** [http://www.ideam.gov.co]

**Usage**
> pip install AgenciBr  

In python:

**Import Ana**
```python
from AgenciBr import Ana
data = Ana('path file')

```

**Import Inemet**

```python
from AgenciBr import Inemet

data = Inemet('path file')
```

   **Import Merge**
 ```python
 from AgenciBr import Merge

data = Merge('path file')
 ```
 
 **Import Alexandre**
 ```python
 from AgenciBr import Alexandre

data = Alexandre('path file')
 ```
 
**Import Ideam**

```python
from AgenciBr import Ideam

data = Ideam('path file')
```


 
 
