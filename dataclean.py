import numpy as np
import pandas as pd

dt = pd.read_csv(r"/home/arshad-ahmed/Documents/dataextraction/sample_music.csv")
print(dt.columns)
dt.drop('id',axis=1)
print(dt.columns)
dt.drop('uri',axis=1)
