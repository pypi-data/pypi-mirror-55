from AOPWorker import AOPWorker
from AOPRunner import AOPRunner
from AOPException import AOPException

def add(x):
    print(x)
    return x+1

def dec(x):
    print(x)
    return x-1

def dou(x):
    print(x)
    return x*2

def error(x):
    return x/0

a = AOPWorker(add)
d = AOPWorker(dec)
doub = AOPWorker(dou)
err = AOPWorker(error)
r = AOPRunner([a,a,err,d,doub,d,d])
try:
    r.run(1)
except AOPException as e:
    print(e)