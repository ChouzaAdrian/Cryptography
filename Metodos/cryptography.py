from cryptoTools import *
from Person import Person
from EllipticCurve import *
import time
import decimal

def elgamalCryptosystem(sender, recipient, g, p):
    recipientPublicKey = recipient.getElgamalPublicKey(g,p)

    cyphertext = sender.getElgamalCyphertext(recipientPublicKey, g, p)

    recipient.decryptElgamal(cyphertext, p)

def diffieHellman(A, B, g, p):
    gb = B.DHCalcPower(g,p)
    gab = A.DHCalcPower(gb,p)

    return gab

def ECDHE(EC, A, B):
    gb = B.getPublicECDHE(EC)
    gab = A.sharedSecretECDHE(EC, gb)

    return gab

def RSA(sender, recipient):
    recipientPublicKey = recipient.getRSAPublicKey()

    cyphertext = sender.getRSACyphertext(recipientPublicKey)

    recipient.decryptRSA(cyphertext)

def MAIN():
    p = 105239 #prime
    g = 84623
    a = 42682 #Alice's secret
    b = 48631 #Bob's secret
    AliceP = 105239
    AliceQ = 109391
    BobP = 112807
    BobQ = 101533

    Alice = Person("Alice",a, AliceP, AliceQ, 32)
    Bob = Person("Bob", b, BobP, BobQ, 54)


    #ELGAMAL: BOB TO ALICE
    elgamalCryptosystem(Bob, Alice, g, p)

    #ELGAMAL: ALICE TO BOB
    elgamalCryptosystem(Alice, Bob, g, p)

    #RSA: BOB TO ALICE
    RSA(Bob, Alice)

    #RSA: ALICE TO BOB
    RSA(Alice, Bob)


    #CURVAS ELIPTICAS
    EC_A = 3
    EC_B = 7
    EC_P = 97
    EC_G = Point(3,6)
    EC_n = 5
    EC_h = 20
    smallEC = EllipticCurve(EC_A, EC_B, EC_P,EC_n,EC_h,EC_G)
    bigEC = EllipticCurve.sampleEC()


    t0 = time.time()
    smallECsharedKey = ECDHE(smallEC, Alice, Bob)
    t1 = time.time()
    print("Time taken by small ECDHE: %s" %(str(t1-t0)))

    t0 = time.time()
    bigECsharedKey = ECDHE(bigEC, Alice, Bob)
    t1 = time.time()
    print("Time taken by big ECDHE: %s" %(str(t1-t0)))
    
    #COMPARANDO CON DHE SIN EC

    t0 = time.time()
    smallSharedKey = diffieHellman(Alice, Bob, 3, 97)
    t1 = time.time()
    print("Time taken by small DHE: %s" %(str(t1-t0)))

    t0 = time.time()
    bigSharedKey = diffieHellman(Alice, Bob, bigEC.G.x, bigEC.primeField)
    t1 = time.time()
    print("Time taken by big DHE: %s" %(str(t1-t0)))
    pass
MAIN()