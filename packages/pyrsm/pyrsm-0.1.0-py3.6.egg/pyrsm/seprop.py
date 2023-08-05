import numpy as np
from math import sqrt


def seprop(x):
    """Caculate the standard error for a proportion"""
    p = np.nanmean(x)
    varprop = p * (1 - p)
    return sqrt(varprop / len(x))

