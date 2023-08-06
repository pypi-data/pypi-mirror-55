# _*_ encoding=utf-8 _*_
#!/usr/bin/env python3

import math
from random import random
import numpy as np

def interval_map(start_in, end_in, start_out, end_out, value_in):
	assert(start_in<end_in and start_out<end_out)
	return ( end_out - start_out ) / ( end_in - start_in ) * ( value_in - start_in) + start_out;


#分段随机函数
def piecewise_random(piece, min, max, ratio):
	assert(piece!=0 and min<max and min>0 and ratio>0 and ratio<1)
	r = random()
	i = 0
	step = float(max-min)/piece
	while 1:
		i += 1
		#输出区间
		start_out = step*(i-1)+min
		end_out = step*i+min
		#输入区间
		start = 1.0-math.pow(1.0-ratio, i-1)
		end = 1.0 - math.pow(1.0-ratio, i)
		print( i,  start, end, start_out, end_out)
		if r > start and r <= end:
			return interval_map(start, end, start_out, end_out, r)

#正态分布随机函数
def normal_distribution_random(min, max):
	r = np.abs(np.random.normal())
	return interval_map(0, 4, min, max, r)

if __name__ == '__main__':
	i = 0
	for i in range(1000):
		#print(piecewise_random(3, 1, 30, 0.9))
		d = normal_distribution_random(1, 30)
		print(d)
		if d < 2:
			i+=1;
			print(i)

