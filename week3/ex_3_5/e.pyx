def f(rep):
	i=0
	while (i<=rep):
		summ=0.
		l=1
		while l<=10000:
			summ += 1. / l ** 2
			l += 1
		i += 1
	return summ
