import multiprocessing
import time

def waitFive():
    time.sleep(5)
    print("5 Seconds has passed since process 1 started")

def waitTen():
    time.sleep(10)
    print("10 seconds has passed since process 2 started")


five = multiprocessing.Process(target=waitFive())
ten = multiprocessing.Process(target=waitTen())

print("Using a for loop - .join() called directly after .start()")

processes = [five, ten]
start = time.time()
for pr in processes:
    pr.start()
    pr.join()
end = time.time()

print('{:.4f} s total time'.format(end - start))

print("No loop - both .start() called before .join()")
start = time.time()
five.start()
ten.start()
five.join()
ten.join()
end = time.time()

print('{:.4f} s total time'.format(end - start))


