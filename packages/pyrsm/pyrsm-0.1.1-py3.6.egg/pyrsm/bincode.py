# Source for R's .bincode function can be found here:
# https://github.com/SurajGupta/r-source/blob/a28e609e72ed7c47f6ddfbb86c85279a0750f0b7/src/main/util.c
import numpy as np
import sys


def bincode(x, breaks, rev, right=True, include_lowest=True):
    """Port of R's .bincode function"""
    n = len(x)
    code = np.array([0] * n)
    nb = len(breaks)
    nb1 = nb - 1
    lft = right is False

    # check if breaks are sorted
    try:
        if sum(breaks[1:] > breaks[-1]) > 0:
            raise ValueError
    except ValueError:
        print("Error: Breaks are not sorted")
        sys.exit(1)

    for i in range(n):
        if np.isnan(x[i]):
            code[i] = np.where(rev, 999 + nb, -999)
            print("One or more entries contain missing values. Code set to -999")
        else:
            lo = 0
            hi = nb1
            if (
                x[i] < breaks[lo]
                or breaks[hi] < x[i]
                or (x[i] == breaks[np.where(lft, hi, lo)] and include_lowest is False)
            ):
                next
            else:
                while hi - lo >= 2:
                    new = int(round((hi + lo) / 2, 0))
                    if x[i] > breaks[new] or (lft and x[i] == breaks[new]):
                        lo = new
                    else:
                        hi = new
                code[i] = lo + 1

    return code
