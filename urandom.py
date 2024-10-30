import random as rd

def random():
    return rd.random()

def randint(a, b):
    return rd.randint(a, b)

def choice(seq):
    return seq[rd.randint(0, len(seq) - 1)]