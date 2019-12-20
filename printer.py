
from units import Unit

import console
from console.utils import cls
from console.screen import sc

def printCard(unit, x, y):
	with sc.location(x, y):
		print(u.shortName)

	with sc.location(x, y+2):
		print(u.shortName)

if __name__ == "__main__":
	cls()

	u = Unit(4, "Human", "Regular", "Medium", "Cavalry")

	printCard(u, 0, 0)
