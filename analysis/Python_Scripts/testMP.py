import multiprocessing
import time

def waitFive():
    time.sleep(5)
    print("5 seconds has passed since process 1 started")

def waitTen():
    time.sleep(10)
    print("10 seconds has passed since process 2 started")


print()
print("********** MP Tests **********")

print("Using a for loop simluation - .join() called directly after .start()")
start = time.time()
five = multiprocessing.Process(target=waitFive)
ten = multiprocessing.Process(target=waitTen)
five.start()
five.join()
ten.start()
ten.join()
end = time.time()

print('{:.4f}s total time'.format(end - start))
print()
print("No loop - both .start() called before .join()")
start = time.time()
five = multiprocessing.Process(target=waitFive)
ten = multiprocessing.Process(target=waitTen)
five.start()
ten.start()
five.join()
ten.join()
end = time.time()

print('{:.4f}s total time'.format(end - start))
print()

