
from units import Unit
from actions import attack
from functools import reduce
from Choosers import *

from printer import SHOULD_PRINT

class Army(object):
	"""docstring for Army"""
	def __init__(self, units, commander_bonus, chooser = First()):
		super(Army, self).__init__()
		self.commander_bonus = commander_bonus
		self.chooser = chooser
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

		availible = self.getFresh()

		#TODO choices
		unit = self.chooser.chooseUnit(availible, battle)
		orders = unit.getOrders(battle)
		order = self.chooser.chooseOrder(orders, battle)
		targets = unit.getOrderTargets(order, battle)

		target = self.chooser.chooseTarget(targets, battle)

		if SHOULD_PRINT:
			print(unit.shortName, order, target)

		unit.order(order, target)


	@property
	def alive(self):
		return any((u.alive for u in self.get("Infantry")))

	def __str__(self):
		return "\n\n".join((u.longName() for u in self.units))

class Battle(object):
	"""docstring for Battle"""
	def __init__(self, armies, turnsPerRound = 4):
		super(Battle, self).__init__()
		self.armies = armies
		for army in self.armies: army.battle = self
		self.turnNumber = 0
		#player count
		self.turnsPerRound = turnsPerRound

	def fight(self):
		while not self.over:
			self.turn()

	def turn(self):
		if SHOULD_PRINT:
			print("New Turn\n")
		self.turnNumber += 1
		for army in self.armies:
			#TODO change turn order
			army.takeTurn(self)

	@property
	def over(self):
		#last man standing
		return reduce(lambda x, y: x + 1 if y.alive else x, self.armies, 0) <= 1

	@property
	def round(self):
		return int(self.turnNumber / self.turnsPerRound)

def test_targeting():
	a1 = Army([Unit(8, "Elf", "Veteran", "Heavy", "Flying")])
	a2 = Army([Unit(6, "Bugbear", "Green", "Light", "Infantry"), Unit(4, "Human", "Levies")])

	# for x in targetList(a1.units[0], a2): print(x)

def army_v_army():

	a = 0
	b = 0
	for x in range(1):
	
		a1 = Army([Unit(6, "Human", "Veteran", "Heavy", "Cavalry")], 0, RandomChoice())
		a2 = Army([Unit(6, "Bugbear", "Green", "Light", "Infantry"), Unit(6, "Bugbear", "Green", "Light", "Archers"), Unit(4, "Human", "Levies")], 0, UserChoice())

		battle = Battle([a1, a2])

		battle.fight()

		if SHOULD_PRINT:
			for i in battle.armies:
				print(i)
				print()

		if a1.alive:
			print(a1)
			a += 1

		if a2.alive:
			print(a2)
			b += 1

	print(a)
	print(b)

def army_test():

	a1 = Army([Unit(6, "Ghoul", "Veteran", "Light", "Cavalry")], 0)
	a2 = Army([Unit(6, "Bugbear", "Green", "Heavy", "Infantry"), Unit(4, "Human", "Archers")], 0)

	battle = Battle([a1, a2])

	print(a2.units[0].getOrders(battle))

	# battle.fight()

	if SHOULD_PRINT:
		for i in battle.armies:
			print(i)
			print()


def army_v_army_2():

	a = 0
	b = 0
	turns = 0
	Iterations = 1000
	for x in range(Iterations):
	
		u1 = Unit(6, "Orc", "Veteran", "Light", "Flying")
		u2 = Unit(6, "Human", "Regular", "Medium", "Cavalry")
		u3 = Unit(6, "Dwarf", "Seasoned", "Heavy", "Infantry")
		u4 = Unit(6, "Dragonborn", "Seasoned", "Medium", "Infantry")

		u5 = Unit(6, "Human", "Veteran", "Heavy", "Infantry")
		u6 = Unit(12, "Human", "Levies")
		u7 = Unit(6, "Elf", "Seasoned", "Light", "Archers")
		u8 = Unit(6, "Gnome", "Veteran", "Medium", "Cavalry")

		a1 = Army([u1, u2, u3, u4], 0)#, UserChoice())
		a2 = Army([u5, u6, u7, u8], 0)#, UserChoice())

		battle = Battle([a1, a2])

		battle.fight()

		turns += battle.turnNumber

		if SHOULD_PRINT:
			for i in battle.armies:
				print(i)
				print()

		if a1.alive:
			if SHOULD_PRINT:
				print(a1)
			a += 1

		if a2.alive:
			if SHOULD_PRINT:
				print(a2)
			b += 1

	print(turns/Iterations)
	print(a)
	print(b)

def army_v_army_test():

	u1 = Unit(12, "Human", "Regular", "Medium", "Cavalry")
	u2 = Unit(12, "Dwarf", "Seasoned", "Heavy", "Infantry")

	u3 = Unit(12, "Dwarf", "Seasoned", "Heavy", "Infantry")
	u4 = Unit(12, "Gnome", "Veteran", "Medium", "Cavalry")

	a1 = Army([u1, u2], 0, UserChoice())
	a2 = Army([u3, u4], 0, UserChoice())

	battle = Battle([a1, a2])

	battle.fight()

	if SHOULD_PRINT:
		for i in battle.armies:
			print(i)
			print()


# u1 = Unit(8, "Elf", "Veteran", "Heavy", "Flying")
# print(u1)
# u2 = Unit(8, "Elf", "Veteran", "Light", "Infantry")
# print(u2)

# attack(u1, u2)

army_v_army_2()

# army_v_army_test()

# slug_fest()

# print(u1)
# print(u2)
# print(u3)
# print(u4)

