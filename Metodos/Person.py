import math
import random
from cryptoTools import *

class Person:
    messagePath = "messages/"

    def __init__(self,name, elgamalSecretKey, secretRSAP, secretRSAQ, secretEC):
        self.name = name
        self.elgamalSecretKey = elgamalSecretKey
        self.messageFile = self.generatePrivateMessage()
        self.secretRSAP = secretRSAP
        self.secretRSAQ = secretRSAQ
        self.RSAE = self.generateRSAE()
        self.RSAD = modInv(self.RSAE, (secretRSAP-1)*(secretRSAQ-1))
        self.RSAN = secretRSAP*secretRSAQ
        self.secretEC = secretEC

    def getPublicECDHE(self, EC):
        return EC.scalar(self.secretEC, EC.G)

    def sharedSecretECDHE(self, EC, PK): #PK=Other person's public key
        return EC.scalar(self.secretEC, PK)

    def getECElgamalPublicKey(self, EC):
        return EC.scalar(self.secretEC, EC.G)

    def getECElgamalCyphertext(self, EC):
        message = self.readUFile()
        k = random.randint(1, EC.n)
        c_1 = EC.scalar(k, EC.G)
        c_2 = []
        for m in message:
            #CONVERTIR UN NUMERO A UN PUNTO DE LA CURVA ELIPTICA ????
            pass

    def DHCalcPower(self,g,p): #g=generator, p=prime
        return bigPower(g,self.elgamalSecretKey,p)
        
    def generatePrivateMessage(self):
        createUNICODE("%s.txt"%(self.name), self.messagePath)
        return "messages/%s_U.txt"%(self.name)

    def getElgamalCyphertext(self, R, g, p): #R=Recipient's secret key, g = generator, p = prime
        
        message = self.readUFile()
        k = random.randint(1,p)
        c_1 = bigPower(g, k, p)
        c_2 = []
        for m in message:
            c2 = (m* bigPower(R, k, p) )%p
            c_2.append(c2)

        cyphertext = (c_1, c_2)
        return cyphertext

    def getElgamalPublicKey(self, g, p):
        return bigPower(g, self.elgamalSecretKey, p)

    def decryptElgamal(self, elgamalCyphertext, p):
        c_1Powera = bigPower(elgamalCyphertext[0],self.elgamalSecretKey,p)
        inv = modInv(c_1Powera,p)
        decrypted = []
        for m in elgamalCyphertext[1]:
            decrypted.append((inv*m)%p)

        decrypted = unicodeToString(decrypted)

        f = open("messages/%sElgamalDecrypted.txt"%(self.name), 'w')
        f.write(decrypted)
        f.close()

    def getRSAPublicKey(self):
        return (self.RSAN, self.RSAE)

    def generateRSAE(self):
        return findFirstCoprime((self.secretRSAP-1)*(self.secretRSAQ-1))

    def getRSACyphertext(self, recipientPublicKey):
        message = self.readUFile()
        cyphertext = []
        N = recipientPublicKey[0]
        E = recipientPublicKey[1]
        for m in message:
            c = bigPower(m, E, N)
            cyphertext.append(c)
        
        return cyphertext

    def decryptRSA(self, cyphertext):
        decrypted = []
        for c in cyphertext:
            m = bigPower(c, self.RSAD, self.RSAN)
            decrypted.append(m)

        decrypted = unicodeToString(decrypted)

        f = open("messages/%sRSADecrypted.txt"%(self.name), 'w')
        f.write(decrypted)
        f.close()

    

    def readUFile(self):
        text = open("messages/U%s.txt"%(self.name)).read().split(" ")
        for i in range(len(text)):
            text[i] = int(text[i])

        return text