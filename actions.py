
from dice import *

DEBUG = False

def attack(attacker, defender, isCharge=False):

	if not attacker.undeadOvercome and defender.hasTrait("Undead"):
		if (attacker.expirence == "Levies" or attacker.expirence == "Green" or attacker.expirence == "Regular"):
			if not attacker.moraleCheck(15):
				if DEBUG:
					print(attacker.shortName,"horrified")
				return

		if DEBUG:
			print(attacker.shortName,"overcame")
		attacker.undeadOvercome = True

	rollAtAdvantage = False
	if attacker.savageAvailible:
		attacker.savageAvailible = False
		rollAtAdvantage = True

	rollAtDisadvantage = False
	if attacker.utype == "Archers" and defender.utype == "Cavalry":
		rollAtDisadvantage = True

	if rollAtAdvantage and not rollAtDisadvantage:
		if DEBUG:
			print("Advantage Roll")
		r = rollAdvantage()
	elif not rollAtAdvantage and rollAtDisadvantage:
		if DEBUG:
			print("Disadvantage Roll")
		r = rollDisadvantage()
	else:
		if DEBUG:
			print("Normal Roll")
		r = roll()

	if DEBUG:
		print(attacker.shortName,"rolled", r)
	if r != 20 and r + attacker.attack < defender.defence:
		if DEBUG:
			print(attacker.shortName, "miss")
		return

	if DEBUG:
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
	if DEBUG:
		print("power check", r)
	if r + attacker.power < defender.toughness:
		if DEBUG:
			print(attacker.shortName, "failed")
		return

	if DEBUG:
		print(defender.shortName, "casualty")

	diminished = defender.diminished
	if attacker.hasTrait("Brutal"):
		defender.damaged(1)

	if attacker.hasTrait("Martial") and attacker.health > defender.health:
		if DEBUG:
			print(attacker.shortName, "triggered Martial")
		defender.damaged(1)

	if isCharge:
		if DEBUG:
			print("Charge started Damage")
		attacker.engages(defender)
		defender.damaged(1)

	defender.damaged(1)

	if attacker.hasTrait("Horrify") and not defender.hasTrait("Eternal") and not defender.moraleCheck(15):
		print(attacker.shortName,"Horrified")
		defender.exhaust()

	if not diminished and defender.diminished and attacker.hasTrait("Frenzy"):
		if DEBUG:
			print(attacker.shortName, "triggered Frenzy")
		attack(attacker, defender)

	if diminished:
		if not defender.moraleCheck(15):
			if DEBUG:
				print(defender.shortName, "damaged by moral")
			defender.damaged(1)


