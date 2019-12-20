from random import choice
import msvcrt as m

from DEBUG import SetPrint

class ChoiceMachine(object):
	"""docstring for ChoiceMachine"""
	def __init__(self):
		super(ChoiceMachine, self).__init__()

	def chooseUnit(self, possible, battle):
		print("NOT IMPLEMENTED")
		exit()

	def chooseOrder(self, possible, battle):
		print("NOT IMPLEMENTED")
		exit()

	def chooseTarget(self, possible, battle):
		print("NOT IMPLEMENTED")
		exit()

	def resetChoices():
		print("NOT IMPLEMENTED")
		exit()

class First(ChoiceMachine):
	"""docstring for Simple"""
	def __init__(self):
		super(First, self).__init__()

	def chooseUnit(self, possible, battle):
		return possible[0]

	def chooseOrder(self, possible, battle):
		return possible[0]

	def chooseTarget(self, possible, battle):
		return possible[0]

class RandomChoice(ChoiceMachine):
	"""docstring for Simple"""
	def __init__(self):
		super(ChoiceMachine, self).__init__()

	def chooseUnit(self, possible, battle):
		return choice(possible)

	def chooseOrder(self, possible, battle):
		return choice(possible)

	def chooseTarget(self, possible, battle):
		return choice(possible)

def wait():
	value = m.getch()
	if value == b'\x1b':
		exit()

	if b'0' <= value and value <= b'9':
		return int(value)

	return False

def userInput(possible):
	i = 1
	for p in possible:
		print(i, p)
		i = i + 1

	x = wait()
	while x == False or x > len(possible):
		x = wait()

	return possible[x - 1]

class UserChoice(ChoiceMachine):
	"""docstring for Simple"""
	def __init__(self):
		super(ChoiceMachine, self).__init__()
		SetPrint()

	def chooseUnit(self, possible, battle):
		# if len(possible) == 1:
		# 	return possible[0]
		return userInput(possible)

	def chooseOrder(self, possible, battle):
		# if len(possible) == 1:
		# 	return possible[0]
		return userInput(possible)

	def chooseTarget(self, possible, battle):
		# if len(possible) == 1:
		# 	return possible[0]
		return userInput(possible)
