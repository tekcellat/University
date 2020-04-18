##########  Kirius-Bek cut  ##########
# 0 - вырожденный
# -1 - невыпуклый
# 1 - выпуклый
def check_convex(polygon):
    n = len(polygon)
    if n < 3:
        return 0

    flag = 0
    for i in range(n):
        j = (i + 1) % n
        k = (i + 2) % n
        z = ((polygon[j][0] - polygon[i][0]) *
             (polygon[k][1] - polygon[j][1]))
        z -= ((polygon[j][1] - polygon[i][1]) *
              (polygon[k][0] - polygon[j][0]))
        if z < 0:
            flag |= 1
        elif z > 0:
            flag |= 2

        if flag == 3:
            return -1

    if flag != 0:
        return 1
    else:
        return 0


def mul_vec(a,b):
    res = [0, 0, 0]
    res[0] = a[1]*b[2] - b[1]*a[2]
    res[1] = b[0]*a[2] - a[0]*b[2]
    res[2] = a[0]*b[1] - a[1]*b[0]
    return res


def diff_vec(p1, p2):
    return [p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2]]


def mul_scalar(a,b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]


def P(t, p1, p2):
    tmp = [0,0,0]
    tmp[0] = p1[0] + round((p2[0]-p1[0])*t)
    tmp[1] = p1[1] + round((p2[1]-p1[1])*t)
    tmp[2] = p1[2] + round((p2[2]-p1[2])*t)
    return tmp


def norm_vecs(res, pol, direction):
    n = len(pol) - 1
    b = [0,0,0]
    for i in range(n):
        b = diff_vec(pol[i+1], pol[i])
        if direction == -1:
            res.append([b[1], -b[0], 0])
        else:
            res.append([-b[1], b[0], 0])


def cut_line(pol, normVect, p1, p2, visible):
    visible = False
    n = len(pol) - 1
    D = diff_vec(p2, p1)
    tbot = 0
    ttop = 1
    for i in range(n):
        W = diff_vec(p1, pol[i])
        Dsk = mul_scalar(D, normVect[i])
        Wsk = mul_scalar(W, normVect[i])
        if Dsk == 0:
            if Wsk < 0:
                return visible, p1, p2
        else:
            t = -Wsk / Dsk
            if Dsk > 0:
                if t > 1:
                    return visible, p1, p2
                else:
                    tbot = max(tbot, t)
            else:
                if t < 0:
                    return visible, p1, p2
                else:
                    ttop = min(ttop, t)
                    
    if tbot <= ttop:
        tmp = P(tbot, p1, p2)
        p2 = P(ttop, p1, p2)
        p1 = tmp
        visible = True

    return visible, p1, p2


def sign(x):
    return int((x > 0) - (x < 0))


def get_direction(pol):
    a = diff_vec(pol[1], pol[0])
    b = [0,0,0]
    n = len(pol)
    tmp = [0,0,0]
    res = 0
    for i in range(1, n-1, 1):
        b = diff_vec(pol[i+1], pol[i])
        tmp = mul_vec(a,b)
        if res == 0:
            res = sign(tmp[2])
        if tmp[2] and res != sign(tmp[2]):
            return 0
        a = b
        
    return res
