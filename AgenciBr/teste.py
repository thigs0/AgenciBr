import pandas as pd
from datetime import datetime
import numpy as np
from AgenciBr.Ana import Ana

path = "/home/thiagosilva/Downloads/teste"
df = Ana(path, list=True)
df.to_climatol(path, (2003, 2021))


