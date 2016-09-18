def f(rep):
	cdef int i, l
	cdef float summ
	i = 0
	while (i<=rep):
		summ=0.
		l=1
		while l<=10000:
			summ += 1. / l ** 2
			l += 1
		i += 1
	return summ
