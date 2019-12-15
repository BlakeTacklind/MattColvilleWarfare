
from units import Unit
from actions import attack
from functools import reduce

DEBUG = False

class First(object):
	"""docstring for Simple"""
	def __init__(self, arg):
		super(Simple, self).__init__()

	def chooseUnit(self, possible, battle):
		return possible[0]

	def chooseOrder(self, possible, battle):
		return possible[0]

	def chooseTarget(self, possible, battle):
		return possible[0]

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

class Army(object):
	"""docstring for Army"""
	def __init__(self, units, commander_bonus):
		super(Army, self).__init__()
		self.commander_bonus = commander_bonus
		self.units = units
		for x in self.units: x.army = self

	def has(self, utype):
		return any((x.utype == utype and x.alive for x in self.units))

	def get(self, utype="all"):
		return list(filter(lambda x : (utype == "all" or x.utype == utype) and x.alive, self.units))

	def getFresh(self):
		return list(filter(lambda x : x.fresh and x.alive, self.units))

	def maybeRefresh(self):
		if not self.getFresh():
			for x in self.get(): x.refresh()

	def takeTurn(self, battle):
		if not self.alive:
			return

		#rare cases this is necessary
		self.maybeRefresh()
		availible = self.getFresh()

		#TODO choices
		unit = availible[0]
		orders = unit.getOrders(battle)
		order = orders[0]
		targets = unit.getOrderTargets(order, battle)

		# targets = targetList(availible[0], enemies[0])
		if DEBUG:
			print("ORDER:", orders[0])

		if targets:
			target = targets[0]
			unit.order(orders[0], target)
		else:	
			unit.order(orders[0])
		

		#Useally refreshes here
		self.maybeRefresh()

	@property
	def alive(self):
		return any((u.alive for u in self.units))

	def __str__(self):
		return "\n\n".join((u.__str__() for u in self.units))

class Battle(object):
	"""docstring for Battle"""
	def __init__(self, armies):
		super(Battle, self).__init__()
		self.armies = armies

	def fight(self):
		while not self.over:
			self.turn()

	def turn(self):
		if DEBUG:
			print("New Turn\n")
		for army in self.armies:
			#TODO change turn order
			army.takeTurn(self)
	
	@property
	def over(self):
		#last man standing
		return reduce(lambda x, y: x + 1 if y.alive else x, self.armies, 0) <= 1

def test_targeting():
	a1 = Army([Unit(8, "Elf", "Veteran", "Heavy", "Flying")])
	a2 = Army([Unit(6, "Bugbear", "Green", "Light", "Infantry"), Unit(4, "Human", "Levies")])

	# for x in targetList(a1.units[0], a2): print(x)

def army_v_army():

	a = 0
	b = 0
	for x in range(1000):
		a1 = Army([Unit(6, "Human", "Veteran", "Heavy", "Infantry")], 0)
		a2 = Army([Unit(6, "Bugbear", "Green", "Light", "Infantry"), Unit(4, "Human", "Levies")], 0)

		battle = Battle([a1, a2])

		battle.fight()

		if DEBUG:
			for i in battle.armies:
				print(i)
				print()

		if a1.alive:
			# print("a1")
			a = a + 1

		if a2.alive:
			# print("a2")
			b = b + 1

	print(a)
	print(b)

def army_test():

	a1 = Army([Unit(6, "Ghoul", "Veteran", "Heavy", "Cavalry")], 0)
	a2 = Army([Unit(6, "Bugbear", "Green", "Light", "Infantry"), Unit(4, "Human", "Levies")], 0)

	battle = Battle([a1, a2])

	print(a1.units[0].getOrders(battle))

	# battle.fight()

	if DEBUG:
		for i in battle.armies:
			print(i)
			print()


# u1 = Unit(8, "Elf", "Veteran", "Heavy", "Flying")
# print(u1)
# u2 = Unit(8, "Elf", "Veteran", "Light", "Infantry")
# print(u2)

# attack(u1, u2)

# army_test()

army_v_army()

# slug_fest()

# print(u1)
# print(u2)
# print(u3)
# print(u4)

