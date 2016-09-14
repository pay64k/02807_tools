#!/usr/bin/python
import sys
import scipy
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate


filename = sys.argv[1]

with open(filename, 'r') as f:
    data = f.read().split("\n")

x = [float(row.split(' ')[0]) for row in data]
y = [float(row.split(' ')[1]) for row in data]

x = np.array(x)
y = np.array(y)

tck = interpolate.splrep(x, y, s=0)



print interpolate.sproot(tck)

xnew = np.arange(x[0],x[ len(x) -1 ])
ynew = interpolate.splev(xnew, tck, der=0)
print ynew
plt.figure()
plt.plot(xnew, ynew)
# plt.legend(['Linear', 'Cubic Spline', 'True'])
# plt.axis([-0.05, 6.33, -1.05, 1.05])
plt.title('Cubic-spline interpolation')
plt.show()


# f = interpolate.interp1d(x, y)
#
# xnew = np.arange(x[0],x[ len(x) -1 ]  )
# ynew = f(xnew)
# ynew = interpolate.splev(xnew, tck, der=0)
#
# fig = plt.figure()
# ax1 = fig.add_subplot(111)
#
# ax1.set_title("Plot B vs H")
# ax1.set_xlabel('B')
# ax1.set_ylabel('H')
#
# ax1.plot(x,y, c='r', label='the data')
# ax1.plot(xnew, ynew, 'o', label='the interpolation')
#
# leg = ax1.legend()
# plt.show()
