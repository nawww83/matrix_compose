def compose(m1, m2):
    res = dict()    
    indices = m1.keys() | m2.keys()
    rmax, cmax = 0, 0
    for i in indices:
        r, c = i

        if r > rmax: rmax = r
        if c > cmax: cmax = c

    for c in range(0, cmax + 1):
        for r in range(0, rmax + 1):

            m1_itm = m2_itm = (0, 0, 0)

            if (r, c) in m1: m1_itm = m1[r, c]

            if (r, c) in m2: m2_itm = m2[r, c]

            bc = (m1_itm[0] + m2_itm[0]) % 256
            gc = (m1_itm[1] + m2_itm[1]) % 256
            rc = (m1_itm[2] + m2_itm[2]) % 256

            res[r, c] = (bc, gc, rc)

    return res

if __name__ == "__main__":
    pass
