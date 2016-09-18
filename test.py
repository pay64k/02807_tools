import datetime
import pyximport; pyximport.install()
print datetime.datetime.now()
i=1
summ=0.
def f(rep):
	i=1
	while (i<=rep):
		summ=0.
		l=1
		while (l<=10000):
			summ=summ+(1./l**2)
			l=l+1
		i=i+1	
	return summ
print (f(5000))
print datetime.datetime.now()
import e
print datetime.datetime.now()
