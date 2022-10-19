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

from AgenciBR import .

_If the data are from Ana_ ➔ **Ana.Ana**
   
   **Example: A = Ana.Ana(file)**
   
   A.dataset # return the dataset
   
   A.code #Return the 
   
   A.startdate #return the first date from dataset
   
   A.enddate  #return the end date from dataset
   
   A.len #return the length from dataset
   
   A.type_data #return the data informations (precipitation, temperature, wind, ...)
   
   
_If the data are from Inemet_ ➔ **Inemet.Inemet** 

_If the data are from Alexandre_ ➔ **Alexandre.Alexandre** 


_If the data are from Merge_ ➔ **Merge.Merge** 


_If the data are from Ideam_ ➔ **Ideam.Ideam** 


 
 
