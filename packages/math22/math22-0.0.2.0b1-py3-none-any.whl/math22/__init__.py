from time import sleep
def isprime(num):
    if(num<0):
        raise Exception("must be a positive number")
    try:
        if(num==1 or num==0):
            return "not a prime number or a composite number"
        srnum=int(num**0.5+1)
        tem=srnum
        for i in range(srnum):
            if((num%tem) == 0):break
            tem-=1
        if(tem==1):return True
        else:return False
    except:
        raise Exception("unknown error")
def issquare(num):
    try:
        if(abs(num**0.5-int(num**0.5))<10**-10):return True
        else:return False
    except(TypeError):
        return "not an integer"
if __name__ == '__main__' :
    a=issquare(-1)
    print(a)


