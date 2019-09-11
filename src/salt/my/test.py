import time
from timeout import timeout

@timeout(500)
def long_running_function1():
    time.sleep(21)
    print('Hello')


long_running_function1()