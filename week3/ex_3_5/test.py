import datetime
import pyximport;

pyximport.install()


def f_py(rep):
    summ = 0
    i = 1
    while i <= rep:
        summ = 0.
        l = 1
        while l <= 10000:
            summ += 1. / l ** 2
            l += 1
        i += 1
    return summ

old_time = datetime.datetime.now()
print "result: ", (f_py(500))
print "time delta for py: ", datetime.datetime.now() - old_time

import e
old_time_cy = datetime.datetime.now()
e.f(500)
print "time delta for cy:", datetime.datetime.now() - old_time_cy
