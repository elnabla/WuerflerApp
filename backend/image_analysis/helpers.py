import numpy as np


def running_median(x, stride):
    if stride % 2 == 0:
        raise ValueError("Stride w must be uneven")
    windows = [x[i:(i + stride)] for i in range(len(x) - stride + 1)]
    initial_pad = [x[:stride] for _ in range(stride // 2)]
    end_pad = [x[-stride:] for _ in range(stride // 2)]
    windows = initial_pad + windows + end_pad
    return np.array(list(map(np.median, windows)))
