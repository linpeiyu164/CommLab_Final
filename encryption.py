def bin_to_int_key(bin_key):
    # transform binary key shared by alice and trent into KAT(integer based key)
    n = len(bin_key)
    int_key = []
    zero = []
    one = []
    for i in range(0,n):
        if not bin_key[i]:
            zero.append(i)
        else:
            one.append(i)
    int_key = zero + one
    return int_key

def chained_cnot(n, KAT, qc):
    # n = len(P)
    for i in range(0,n):
        if i != KAT[i]:
            qc.cnot(i, KAT[i])

def qotp(n, KAT_2n, qc):
    # n = len(P)
    # KAT has length 2n
    for i in range(0,n):
        if KAT_2n[2*i]:
            qc.x(i)
        if KAT_2n[2*i+1]:
            qc.z(i)