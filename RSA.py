import random as ra

def primeNoGenerator(n):
    P=[True for _ in range(n)]
    P[0]=False
    P[1]=False
    for i in range(2,n):
        if P[i]==True:
            k=2*i
            while k<n:
                P[k]=False
                k+=i
    P=[i for i in range(n) if P[i]==True]
    P=P[-100:]
    return P

def gcd(a, b):
    if a % b == 0:
        return b
    else:
        return gcd(b, a%b)

def e_gcd(a, b):  
    if a%b == 0:
        return b, 0, 1
    hcf, x, y = e_gcd(b, a%b) 
    return hcf, y, x - (y * (a//b))

def ModInverse(m, mod_n):
    gcd, x, y = e_gcd(m%mod_n, mod_n)
    if gcd == 1:
        if x < 0:
            x += mod_n
        return x
    else:
        print('numbers are not co prime, modularinverse does not exist')

def RSAKeyGen(P):
    #Giving p and q Some Random Large Prime Values
    p,q=ra.randint(0,99),ra.randint(0,99)
    if p == q: q = p-1
    p, q = P[p], P[q]
    n = p * q

    #Generating Phi of p and q
    phi_n = (p-1) * (q-1)

    #Generating e
    for i in range(phi_n,0,-1):
        if gcd(phi_n,i)==1:
            e=i
            if ra.randint(0,3)==1:
                break

    #Generating d
    d=ModInverse(e,phi_n)

    z=pow(e,phi_n-1,n)
    """
    pub_key=(e,n)
    pri_key=(d,n)
    """
    return e, d, n

def pow(a,b,m):
    res=1
    while(b!=0):
        if b%2==1:
            res=(res*a)%m
        b//=2
        a=(a*a)%m
    return res

def RSAEncryption(e,n,m='abds \n bdfs'):
    m=[ord(i) for i in m]
    m=[str(pow(i,e,n)) for i in m]
    m=' '.join(m)
    return m

def RSADecryption(d,n,m='1 2 3 4 5 6'):
    m=list(map(int,m.split()))
    m=[pow(i,d,n) for i in m]
    m=[chr(i) for i in m]
    m=''.join(m)
    return m

