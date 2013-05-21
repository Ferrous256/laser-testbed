#!/usr/bin/env python

from lib import dac
from lib.common import *

import math
import random
import itertools
import sys

import thread
import time

MAX_X = 20000
MIN_X = -20000
MAX_Y = 20000
MIN_Y = -20000

RADIUS = 2000

# Lower the laser power
COLOR_DENOM = 1.0

class PointStream(object):
	def __init__(self):
		self.called = False
		self.stream = self.produce()

	def produce(self):
		while True: 
			yield (0, 0, 0, 0, 0) 

	def read(self, n):
		d = [self.stream.next() for i in xrange(n)]
		return d


class Ball(PointStream):
	def __init__(self, x, y, radius = 1200):
		super(Ball, self).__init__()
		self.x = x
		self.y = y
		self.radius = radius

	def produce(self):
		while True: 
			for i in xrange(0, 40, 1):
				i = float(i) / 40 * 2 * math.pi
				x = int(math.cos(i) * self.radius) + self.x
				y = int(math.sin(i) * self.radius) + self.y
				yield (x, y, 0, 0, int(CMAX/COLOR_DENOM))

			# This, by itself, works
			#self.x = (self.x + 10) % 10000
			#self.y = (self.y + 10) % 10000

"""
Main Program
"""

ps = Ball(0, 0, RADIUS)

def dac_thread():
	while True:
		try:
			d = dac.DAC(dac.find_first_dac())
			d.play_stream(ps)
			print "Testing"
		except:
			pass

def move_thread():
	global MAX_X, MAX_Y, MIN_X, MIN_Y

	xDirec = 0
	yDirec = 0

	xAdd = 500
	yAdd = 500

	while True:
		if ps.x > MAX_X:
			xDirec = 0
			xAdd = random.randint(100, 1000)
		elif ps.x < MIN_X:
			xDirec = 1
			xAdd = random.randint(100, 1000)
		if ps.y > MAX_Y:
			yDirec = 0
			yAdd = random.randint(100, 1000)
		elif ps.y < MIN_Y:
			yDirec = 1
			yAdd = random.randint(100, 1000)

		if xDirec:
			ps.x += xAdd
		else:
			ps.x -= xAdd

		if yDirec:
			ps.y += yAdd
		else:
			ps.y -= yAdd

		time.sleep(0.020)


thread.start_new_thread(dac_thread, ())
thread.start_new_thread(move_thread, ())

while True:
	time.sleep(2)


