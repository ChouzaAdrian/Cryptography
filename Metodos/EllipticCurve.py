from cryptoTools import *

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class EllipticCurve:
    def __init__(self, A, B, p, n, h, G):
        if(4*A*A*A+27*B*B==0):
            raise Exception("Non-valid elliptic curve. 4A^3+27B^2 = 0")
        self.A = A
        self.B = B
        self.primeField = p
        self.n = n
        self.h = h
        self.G = G

    @staticmethod
    def sampleEC():
        EC = EllipticCurve(0,7,0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141, 1, Point(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8) )
        return EC

    def copyPoint(self, P):
        if P is None:
            return None
        Q = Point(P.x, P.y)
        return Q

    def negPoint(self, P):
        if P is None:
            return P
        newP = self.copyPoint(P)
        newP.y = self.primeField - newP.y
        return newP

    def contains(self, P):
        if ((P.y*P.y)%self.primeField == (P.x*P.x*P.x + self.A * P.x + self.B)%self.primeField):
            return True
        False

    def areEqual(self, P,Q):
        if P is None and Q is None:
            return True
        elif P is None or Q is None:
            return False
        else:
            if P.x == Q.x and P.y == Q.y:
                return True
            return False

    def scalar(self, n, P):
        newP = self.copyPoint(P)
        binary = bin(n)
        result = None
        for bit in range(len(binary)-1,1,-1):
            if(binary[bit]=="1"):
                result = self.sumPoints(result, newP)
            newP = self.sumPoints(newP, newP)

        return result 

    def sumPoints(self, P, Q):
        if P is None:
            return Q
        elif Q is None:
            return P
        elif self.areEqual(P, self.negPoint(Q)):
            return None
        else:
            a = 0
            if self.areEqual(P, Q):
                n = (3*P.x*P.x+self.A) % self.primeField
                d = (2*P.y) % self.primeField
                if(d==0):
                    return None
                dInv = modInv(d,self.primeField)
                a = n*dInv % self.primeField
            else:
                n = (Q.y - P.y) % self.primeField
                d = (Q.x-P.x) % self.primeField
                if(d == 0):
                    return None
                dInv = modInv(d, self.primeField)
                a = n*dInv % self.primeField
            newX = (a*a-P.x-Q.x) % self.primeField
            newY = (a*(P.x - newX) - P.y) % self.primeField

            return Point(newX, newY)



