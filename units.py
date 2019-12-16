
from dice import *
from actions import attack
from printer import SHOULD_PRINT

flatten = lambda l: [item for sublist in l for item in sublist]

class StatMod(object):
	"""docstring for StatMod"""
	def __init__(self, attack = 0, power = 0, defence = 0, toughness = 0, morale = 0, multiplier = 1.0):
		super(StatMod, self).__init__()
		self.attack = attack
		self.power = power
		self.defence = defence
		self.toughness = toughness
		self.morale = morale
		self.multiplier = multiplier

class Ancestry(StatMod):
	"""docstring for Ancestry"""
	def __init__(self, attack, power, defence, toughness, morale, traits=[]):
		super(Ancestry, self).__init__(attack, power, defence, toughness, morale)
		self.traits = traits

	@property
	def cost(self):
		return sum((TraitList[x].cost for x in self.traits))

	def strTraits(self):
		return "\n\n".join(x+"\n"+TraitList[x].description for x in self.traits)

AncestryList = {
	"Bugbear" : Ancestry(2, 0, 0, 0, 1, ["Martial"]),
	"Dragonborn" : Ancestry(2, 2, 1, 1, 1, ["Courageous"]),
	"Dwarf" : Ancestry(3, 1, 1, 1, 2, ["Stalwart"]),
	"Elf" : Ancestry(2, 0, 0, 0, 1, ["Eternal"]),
	"Elf (Winged)" : Ancestry(1, 1, 0, 0, 1, ["Eternal"]),
	"Ghoul" : Ancestry(-1, 0, 2, 2, 0, ["Undead", "Horrify", "Ravenous"]),
	"Gnoll" : Ancestry(2, 0, 0, 0, 1, ["Frenzy"]),
	"Gnome" : Ancestry(1, -1, 1, -1, 1),
	"Goblin" : Ancestry(-1, -1, 1, -1, 0),
	"Hobgoblin" : Ancestry(2, 0, 0, 0, 1, ["Bred for War", "Martial"]),
	"Human" : Ancestry(2, 0, 0, 0, 1, ["Courageous"]),
	"Kobold" : Ancestry(-1, -1, 1, -1, -1),
	"Lizardfolk" : Ancestry(2, 1, -1, 1, 1, ["Amphibious"]),
	"Ogre" : Ancestry(0, 2, 0, 2, 1, ["Brutal"]),
	"Orc" : Ancestry(2, 1, 1, 1, 2, ["Savage"]),
	"Skeleton" : Ancestry(-2, -1, 1, 1, 1, ["Undead", "Mindless"]),
	"Treant" : Ancestry(0, 2, 0, 2, 0, ["Siege Engine", "Twisting Roots", "Hurl Rocks"]),
	"Troll" : Ancestry(0, 2, 0, 2, 0, ["Regenerate"]),
	"Zombie" : Ancestry(-2, 0, 2, 2, 2, ["Undead", "Mindless"]),
}

class Trait(object):
			"""docstring for Trait"""
			def __init__(self, cost, description):
				super(Trait, self).__init__()
				self.cost = cost
				self.description = description
						
TraitList = {
	"Amphibious": Trait(50, "This unit does not suffer terrain penalties for fighting in water or on land."),
	"Bred for War": Trait(100, "This unit cannot be diminished, and cannot have disadvantage on Morale checks."),
	"Brutal": Trait(200, "This unit inflicts 2 casualties on a successful Power check."),
	"Courageous": Trait(50, "Once per battle, this unit can choose to succeed on a Morale check it just failed."),
	"Eternal": Trait(50, "This unit cannot be horrified, and it always succeeds on Morale checks to attack undead and fiends."),
	"Frenzy": Trait(50, "If this unit diminishes an enemy unit, it immediately makes a free attack against that unit."),
	"Horrify": Trait(200, "If this unit inflicts a casualty on an enemy unit, that unit must make a DC 15 Morale check. Failure exhausts the unit."),
	"Martial": Trait(100, "If this unit succeeds on a Power check and its size is greater than the defending unit, it inflicts 2 casualties."),
	"Mindless": Trait(100, "This unit cannot fail Morale checks."),
	"Regenerate": Trait(200, "When this unit refreshes, increment its casualty die. This trait ceases to function if the unit suffers a casualty from battle magic."),
	"Ravenous": Trait(50, "While any enemy unit is diminished, this unit can spend a round feeding on the corpses to increment their casualty die."),
	"Hurl Rocks": Trait(250, "If this unit succeeds on an Attack check, it inflicts 2 casualties. against fortifications, it inflicts 1d6 casualties."),
	"Savage": Trait(50, "This unit has advantage on the first Attack check it makes each battle."),
	"Stalwart": Trait(50, "Enemy battle magic has disadvantage on Power checks against this unit."),
	"Twisting": Trait(200, "Roots As an action, this unit can sap the walls of a fortification. Siege units have advantage on Power checks against sapped fortifications."),
	"Undead": Trait(50, "Green and regular troops must pass a Morale check to attack this unit. Each enemy unit need only do this once."),
}


class Expirence(StatMod):
	"""docstring for Expirence"""
	def __init__(self, attack, toughness, morale):
		super(Expirence, self).__init__(attack, 0, 0, toughness, morale)

ExpirenceList = {
	"Levies": Expirence(0, 0, 0),
	"Green": Expirence(0, 0, 0),
	"Regular": Expirence(1, 1, 1),
	"Seasoned": Expirence(1, 1, 2),
	"Veteran": Expirence(1, 1, 3),
	"Elite": Expirence(2, 2, 4),
	"Super-elite": Expirence(2, 2, 5),
}


class Equipment(StatMod):
	"""docstring for Equipment"""
	def __init__(self, power, defence):
		super(Equipment, self).__init__(0, power, defence, 0, 0)

EquipmentList = {
	"Levies": Equipment(1, 1),
	"Light": Equipment(1, 1),
	"Medium": Equipment(2, 2),
	"Heavy": Equipment(4, 4),
	"Super-heavy": Equipment(6, 6),
}

class UnitType(StatMod):

	"""docstring for UnitType"""
	def __init__(self, attack, power, defence, toughness, morale, multiplier):
		super(UnitType, self).__init__(attack, power, defence, toughness, morale, multiplier)

UnitTypeList = {
	"Flying": UnitType(0, 0, 0, 0, 3, 2),
	"Archers": UnitType(0, 1, 0, 0, 1, 1.75),
	"Cavalry": UnitType(1, 1, 0, 0, 2, 1.5),
	"Levies": UnitType(0, 0, 0, 0, -1, 0.75),
	"Infantry": UnitType(0, 0, 1, 1, 0, 1),
	"Siege Engine": UnitType(1, 1, 0, 1, 0, 1.5),
}


class UnitSize(object):
	"""docstring for UnitSize"""
	def __init__(self, multiplier):
		super(UnitSize, self).__init__()
		self.multiplier = multiplier

UnitSizeList = {
	4: UnitSize(2/3),
	6: UnitSize(1),
	8: UnitSize(4/3),
	10: UnitSize(5/3),
	12: UnitSize(2),
}

def targetList(unit, army):
	if unit.engaged:
		return unit.engagedBy + ([unit.engaging] if unit.engaging else [])

	if unit.utype == "Infantry" or unit.utype == "Levies":
		if army.has("Levies"):
			return army.get("Levies")
		if army.has("Infantry"):
			return army.get("Infantry")

		return army.get("Archers")

	if unit.utype == "Archers" or unit.utype == "Flying":
		return army.get()

	if unit.utype == "Cavalry":
		return army.get("Levies") + army.get("Infantry") + army.get("Archers") + army.get("Cavalry")

	print("No Utype??")
	exit()

class Unit(object):
	"""docstring for Unit"""
	def __init__(self, size, ancestry, expirence, equipment="Levies", utype="Levies"):
		super(Unit, self).__init__()
		self.nameit()

		self.ancestry = ancestry
		self.expirence = expirence
		self.equipment = equipment
		self.utype = utype
		self.size = size

		self.health = size

		self.attack = self._attack()
		self.power = self._power()
		self.defenceBonus = self._defenceBonus()
		self.defence = self._defence()
		self.toughnessBonus = self._toughnessBonus()
		self.toughness = self._toughness()
		self.morale = self._morale()
		self.multiplier = self._multiplier()
		self.cost = self._cost()

		self.fresh = True

		self.battleRefresh()

	def nameit(self, name = ""):
		self.named = name

	def exhaust(self):
		self.fresh = False
		self.army.maybeRefresh()

	def canTarget(self, battle):
		return flatten(targetList(self, i) for i in (filter(lambda x: x is not self.army, battle.armies)))

	def refresh(self):
		self.fresh = True

		if self.hasTrait("Regenerate"):
			self.heal()

	def heal(self, amount = 1):
		self.health = self.health + amount
		if self.health > self.size:
			self.health = self.size

	def battleRefresh(self):
		self.couragousAvailible = self.hasTrait("Courageous")
		self.savageAvailible = self.hasTrait("Savage")
		self.engagedBy = []
		self.engaging = False
		self.undeadOvercome = False
		self.lastAttack = -2
		self.rallied = False

	@property
	def engaged(self):
		return self.engagedBy or self.engaging

	def moraleCheck(self, DC):
		if self.hasTrait("Mindless"):
			return True

		check = self.morale + self.army.commander_bonus + roll() >= DC

		# TODO CHOICE
		if not check and self.couragousAvailible:
			self.couragousAvailible = False
			return True

		return check

	def canAttack(self):
		if self.isCavalry and self.army.battle.round < self.lastAttack + 1:
			return False

		return True

	@property
	def isCavalry(self):
		return self.utype == "Cavalry"

	def getOrders(self, battle):

		options = []

		if self.canAttack():
			options.append("Attack")

		if self.canFeed():
			options.append("Feed")

		if self.isCavalry:
			if not self.engaging:
				options.append("Charge")
			else:
				options.append("Disengage")


		if not options:
			print("Somehow got no options")
			exit()

		return options

	def getOrderTargets(self, order, battle):
		if order == "Attack" or order == "Charge":
			return self.canTarget(battle)

		return [None]

	def attemptRally(self):
		self.rallied = True

		if self.moraleCheck(15):
			self.health = 1
			return True

		return False

	def canFeed(self):
		return self.hasTrait("Ravenous") and any(i.diminished for i in flatten((y.units for y in filter(lambda x: x is not self.army, self.army.battle.armies))))

	def order(self, order, order_vars = None):
		if order == "Attack":
			if not self.canAttack():
				print("Bad Attack order")
				exit()

			self.lastAttack = self.army.battle.round
			self.attackUnit(order_vars)

		elif order == "Feed":
			if self.hasTrait("Ravenous") and self.canFeed():
				self.heal()
			else:
				print("Bad Feed Order")
				exit()

		elif order == "Sap":
			if not self.hasTrait("Twisting Roots"):
				print("Bad Twisting Roots order")
				exit()

			#TODO safety that order_vars is correct type
			if order_vars.utype == "Fortification":
				#TODO sapping
				print("Not implented")
				exit()
		elif order == "Charge":
			attack(self, order_vars, True)
		elif order == "Disengage":
			if self.moraleCheck(13):
				self.disengages()
		elif order == "None":
			pass
		else:
			print("bad order")
			exit()

		self.exhaust()
		return

	def engages(self, target):
		target.engagedBy.append(self)
		self.engaging = target

	def disengages(self):
		if self.engaging:
			self.engaging.engagedBy.remove(self)
			self.engaging = False

	def cleanEngagement(self):
		self.disengages()

		for ele in self.engagedBy:
			ele.disengages()

	def attackUnit(self, unit):
		attack(self, unit)

	def _attack(self):
		return sum((AncestryList[self.ancestry].attack, ExpirenceList[self.expirence].attack, EquipmentList[self.equipment].attack, UnitTypeList[self.utype].attack))

	def _power(self):
		return sum((AncestryList[self.ancestry].power, ExpirenceList[self.expirence].power, EquipmentList[self.equipment].power, UnitTypeList[self.utype].power))

	def _defenceBonus(self):
		return sum((AncestryList[self.ancestry].defence, ExpirenceList[self.expirence].defence, EquipmentList[self.equipment].defence, UnitTypeList[self.utype].defence))

	def _defence(self):
		return self.defenceBonus + 10

	def _toughnessBonus(self):
		return sum((AncestryList[self.ancestry].toughness, ExpirenceList[self.expirence].toughness, EquipmentList[self.equipment].toughness, UnitTypeList[self.utype].toughness))

	def _toughness(self):
		return self.toughnessBonus + 10

	def _morale(self):
		return sum((AncestryList[self.ancestry].morale, ExpirenceList[self.expirence].morale, EquipmentList[self.equipment].morale, UnitTypeList[self.utype].morale))

	def _multiplier(self):
		return (UnitTypeList[self.utype].multiplier * UnitSizeList[self.size].multiplier)

	def _cost(self):
		return int(((self._attack() + self._power() + self._defenceBonus() + self._toughnessBonus() + (self._morale() * 2)) * self._multiplier()) * 10) + 30 + AncestryList[self.ancestry].cost

	@property
	def strType(self):
		if self.utype == "Levies":
			return self.ancestry + " " + self.expirence
		return self.ancestry + " " + self.expirence + " " + self.equipment + " " + self.utype

	@property
	def statsBlock(self):
		return "Cost: " + str(self.cost) + "\nAttack " + str(self.attack) + " Defence " + str(self.defence) + "\nPower "+str(self.power)+" Thoughness: "+str(self.toughness)+"\nMorale: "+str(self.morale)+" Size: 1d" + str(self.size)

	@property
	def shortName(self):
		if self.named != "":
			return self.named
		return self.strType

	def longName(self):
		return self.strType + "\n"+self.statsBlock+"\n"+AncestryList[self.ancestry].strTraits()+ "\nHP "+str(self.health)

	def __str__(self):
		return self.shortName

	def hasTrait(self, trait):
		return trait in AncestryList[self.ancestry].traits

	def damaged(self, amount):
		self.health -= amount

		if not self.alive:
			if not self.attemptRally():
				if SHOULD_PRINT():
					print(self.shortName, "rooted")
				self.army.maybeRefresh()
				self.cleanEngagement()
			else:
				if SHOULD_PRINT():
					print(self.shortName, "Rallied")

	@property
	def diminished(self):
		if self.hasTrait("Bred for War"):
			return False
		if self.utype == "Levies":
			return True;
		return self.health <= (self.size / 2)

	@property
	def alive(self):
		return self.health > 0

if __name__ == "__main__":

	u1 = Unit("Bugbear", "Green", "Light", "Infantry", 6)
	u2 = Unit("Bugbear", "Green", "Light", "Infantry", 4)
	u3 = Unit("Bugbear", "Green", "Light", "Archers", 4)

	print(u1)
	print(u2)
	print(u3)
