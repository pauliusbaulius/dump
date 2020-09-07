import os
import time


def hello(string):
    while True:
        print(string)
        time.sleep(2)


pid = os.fork()
if pid == 0:
    print("I'm {}, a newborn that knows to write to the terminal!".format(os.getpid()))
    hello("child")
else:
    print("I'm the dad of {}, and he knows to use the terminal!".format(pid))
    hello("parent")
    os.waitpid(pid, 0)