# utilities

import math

def arrmult(a,b):
	assert (len(a) == len(b))
	return [a[i]*b[i] for i in range(0,len(a))]

def lincomb(a,b):
	assert (len(a) == len(b))
	s = 0
	for i in range(0, len(a)):
		s += a[i]*b[i]
	return s
