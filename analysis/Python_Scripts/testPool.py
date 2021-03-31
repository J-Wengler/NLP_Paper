from multiprocessing import Pool
import datetime

def double(n):
    return(n*n)

nums=[2,3,6,8,10]
#pool=Pool(processes=3)
print(pool.map(double,nums))
