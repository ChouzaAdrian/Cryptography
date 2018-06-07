import math
import random

def bigPower(a, b, p): #(a^b) mod p
    binary = bin(b)
    result = 1
    aPowerOf2 = a % p
    for bit in range(len(binary)-1,1,-1):
        if(binary[bit]=="1"):
            result = (result*aPowerOf2) % p
        aPowerOf2 = (aPowerOf2*aPowerOf2) % p
    return result


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b%a,a)
    return (g, x - (b//a) * y, y)

def modInv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x%m

def findFirstCoprime(N):
    for i in range(2,N):
        if egcd(i,N)[0] == 1:
            return i

def unicodeToString(unicodeArray):
    for i in range(len(unicodeArray)):
        unicodeArray[i] = chr(unicodeArray[i])

    decrypted = "".join(unicodeArray)
    return decrypted

def createUNICODE(fileName, path):
    f = open(path + fileName)
    text = f.read()
    f.close()
    characters = []
    for i in range(len(text)):
        characters.append(text[i])
        characters[i] = str(ord(characters[i]))

    newText = " ".join(characters)
    newFile = open("messages/U%s"%(fileName), 'w')
    newFile.write(newText)
    newFile.close()
    




