
import random

def roll(d = 20):
	return random.randint(1,d)

def rollAdvantage():
	return max((roll(), roll()))

def rollDisadvantage():
	return min((roll(), roll()))
