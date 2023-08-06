# -*- coding: UTF-8 -*-
# vim: noet tabstop=4 shiftwidth=4

'''Timestamp enumerator 

Count timestamps with different step sizes. A reference time is used to add/
subtract an offset to enumerate the timestamps. To format the timestamp
strftime formating style is used.
'''

__version__     = '1.0.1'
__author__      = 'Alexander Böhm'
__email__		= 'alxndr.boehm@gmail.com'
__license__		= 'GPLv2+'

from datetime import datetime, timedelta

STEP_WEEK		= "week"
STEP_DAY		= "day"
STEP_HOUR		= "hour"
STEP_MINUTE		= "minute"
STEP_SECOND		= "second"

def enumerate_times(cur_time: datetime, offset: int, count: int, step: str, pattern: str) -> list:
	'''
	Count a number of timestamps from a specific time at a given offset. Timestamps
	are formated with strftime.

	Parameters:
		cur_time (datetime): Reference time

		offset (int): Offset added/subtracted in given unit from refrence time

		count (int): Timestamps to count in given unit

		step (str): Step size counting in. Allow values are
					- STEP_WEEK
					- STEP_DAY
					- STEP_HOUR
					- STEP_MINUTE
					- STEP_SECOND

		pattern (str): Timestamp pattern in strftime format

	Returns
		list: A list of enumarted timestamps as strings
	'''

	cur = cur_time
	r = []

	l_count = (count < 0)*count
	h_count = (count >= 0)*count

	if step == STEP_WEEK:
		for i in range(l_count, h_count):
			t = cur+timedelta(weeks=(i+offset))
			r += [t.strftime(pattern)]

	elif step == STEP_DAY:
		for i in range(l_count, h_count):
			t = cur+timedelta(days=(i+offset))
			r += [t.strftime(pattern)]

	elif step == STEP_HOUR:
		for i in range(l_count, h_count):
			t = cur+timedelta(hours=(i+offset))
			r += [t.strftime(pattern)]

	elif step == STEP_MINUTE:
		for i in range(l_count, h_count):
			t = cur+timedelta(minutes=(i+offset))
			r += [t.strftime(pattern)]

	elif step == STEP_SECOND:
		for i in range(l_count, h_count):
			t = cur+timedelta(seconds=(i+offset))
			r += [t.strftime(pattern)]

	else:
		raise Exception('Stepsize %s is not defined' % (step))

	return r

