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
print "result for py: ", (f_py(500))
print "time delta for py: ", datetime.datetime.now() - old_time

import e
old_time_cy = datetime.datetime.now()
print "result for cy: ", e.f(500)
print "time delta for cy:", datetime.datetime.now() - old_time_cy

# no types decalred:
# time delta for py:  0:00:05.696566
# time delta for cy: 0:00:03.277645

# with types declared:
# time delta for py:  0:00:00.661372
# time delta for cy: 0:00:00.024943