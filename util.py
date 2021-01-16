import numpy as np
from itertools import chain


def get_features(prev_flow, flow):
    return list(chain(*[mag(flow), div_curl(prev_flow, flow)]))


def mag(flow):
    mag, mag_c = [0, 0, 0, 0], [0, 0, 0, 0]
    for row in flow:
        for f in row:
            x, y = int(f[0] < 0), int(f[1] < 0) + 2
            mag[x] += abs(f[0])
            mag_c[x] += 1
            mag[y] += abs(f[1])
            mag_c[y] += 1

    return [i/j if j != 0 else 0 for i, j in zip(mag, mag_c)]


def div_curl(prev_flow, flow):
    dc, dc_c = [0, 0, 0, 0], [0, 0, 0, 0]
    for x, row in enumerate(prev_flow):
        for y, v in enumerate(row):
            try:
                d = np.dot(v, flow[int(x+v[0]), int(y+v[1])])
                c = np.cross(v, flow[int(x+v[0]), int(y+v[1])])
            except Exception:
                d = 0
                c = 0
            i, j = int(d < 0), int(c < 0) + 2
            dc[i] += abs(d)
            dc_c[i] += 1
            dc[j] += abs(c)
            dc_c[j] += 1
    return [i/j if j != 0 else 0 for i, j in zip(dc, dc_c)]
