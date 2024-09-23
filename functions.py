import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn

def calc_connection_time(df): #Calculate session time
    return (df.max() - df.min()).total_seconds()
