
from dice import *
from printer import SHOULD_PRINT

def attack(attacker, defender, isCharge=False):

	if not attacker.undeadOvercome and defender.hasTrait("Undead"):
		if (attacker.expirence == "Levies" or attacker.expirence == "Green" or attacker.expirence == "Regular"):
			if not attacker.moraleCheck(15):
				if SHOULD_PRINT():
					print(attacker.shortName,"horrified")
				return

		if SHOULD_PRINT():
			print(attacker.shortName,"overcame")
		attacker.undeadOvercome = True

	rollAtAdvantage = False
	if attacker.savageAvailible:
		attacker.savageAvailible = False
		rollAtAdvantage = True

	if isCharge:
		rollAtAdvantage = True

	rollAtDisadvantage = False
	if attacker.utype == "Archers" and defender.utype == "Cavalry":
		rollAtDisadvantage = True

	if rollAtAdvantage and not rollAtDisadvantage:
		if SHOULD_PRINT():
			print("Advantage Roll")
		r = rollAdvantage()
	elif not rollAtAdvantage and rollAtDisadvantage:
		if SHOULD_PRINT():
			print("Disadvantage Roll")
		r = rollDisadvantage()
	else:
		if SHOULD_PRINT():
			print("Normal Roll")
		r = roll()

	if SHOULD_PRINT():
		print(attacker.shortName,"rolled", r)
	if r != 20 and r + attacker.attack < defender.defence:
		if SHOULD_PRINT():
			print(attacker.shortName, "miss")
		return

	if SHOULD_PRINT():
		print("hit", defender.shortName)

	if attacker.hasTrait("Rock Hurler"):
		if defender.utype == "Fortification":
			defender.damaged(roll(6))
		else:
			defender.damaged(2)
		return

	powerCheck(attacker, defender, isCharge)
	if r == 20:
		powerCheck(attacker, defender, isCharge)

def powerCheck(attacker, defender, isCharge):
	r = roll()
	if SHOULD_PRINT():
		print("power check", r)
	if r + attacker.power < defender.toughness:
		if SHOULD_PRINT():
			print(attacker.shortName, "failed")
		return

	if SHOULD_PRINT():
		print(defender.shortName, "casualty")

	damage = 1

	if attacker.hasTrait("Brutal"):
		damage += 1

	if attacker.hasTrait("Martial") and attacker.health > defender.health:
		if SHOULD_PRINT():
			print(attacker.shortName, "triggered Martial")
		damage += 1

	if isCharge:
		if SHOULD_PRINT():
			print(attacker.shortName, "engages", defender.shortName)
		attacker.engages(defender)
		damage += 1

	if attacker.hasTrait("Horrify") and not defender.hasTrait("Eternal") and not defender.moraleCheck(15):
		print(attacker.shortName,"Horrified")
		defender.exhaust()


	if defender.diminished:
		if not defender.moraleCheck(15):
			if SHOULD_PRINT():
				print(defender.shortName, "moral casualty")
			damage += 1

	diminished = defender.diminished
	defender.damaged(damage)

	if not diminished and defender.diminished and attacker.hasTrait("Frenzy"):
		if SHOULD_PRINT():
			print(attacker.shortName, "triggered Frenzy")
		attack(attacker, defender)

