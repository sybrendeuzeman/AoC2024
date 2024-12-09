import time

def fib(untill):
    fib_prev = 1
    fib_curr = 1
    for i in range(untill):
        fib_new =  fib_prev + fib_curr
        fib_prev = fib_curr
        fib_curr = fib_new
      
def time_fib(untill):
    t0 = time.time()
    fib(untill)
    t1 = time.time()

    print(untill, ':', (t1-t0) / untill * 1000000)

time_fib(10)
time_fib(100)
time_fib(1000)
time_fib(2000)
time_fib(3000)
time_fib(4000)
time_fib(5000)
time_fib(6000)
time_fib(7000)
time_fib(8000)
time_fib(9000)
time_fib(10000)
time_fib(20000)
time_fib(30000)
time_fib(40000)
time_fib(50000)
time_fib(60000)
time_fib(70000)
time_fib(80000)
time_fib(90000)
time_fib(100000)
time_fib(200000)
time_fib(300000)
time_fib(400000)
time_fib(500000)
time_fib(600000)
time_fib(700000)
time_fib(800000)
time_fib(900000)
time_fib(1000000)




