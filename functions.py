import math
import random
# A module containing functions in the game

def coord_add(p1, p2):
	return ((p1[0] + p2[0]), (p1[1] + p2[1]))


def coord_subtract(p1, p2):
	return ((p1[0] - p2[0]), (p1[1] - p2[1]))


def distance (p1, p2):
    return math.sqrt(coord_subtract(p1, p2)[0]**2 + coord_subtract(p1, p2)[1]**2)

# Returns the qudrant p2 is w.r.t p1
def quadrant (p1, p2):
	dx = p2[0] - p1[0]
	dy = p2[1] - p1[1]

	if dx >= 0:
		if dy >= 0:
			return 1
		else:
			return 4
	else:
		if dy >= 0:
			return 2
		else:
			return 3
# Quadratic formula
# 1st element for + root
# 2nd element for - root
def quadratic_formula (a, b, c):
	if a == 0:
		return False
	else:
		dis = b**2 - 4.0 * a * c
		if dis < 0:
			return ("No real roots")
		else:
			x1 = (-b + math.sqrt(dis)) / (2.0 * a)
			x2 = (-b - math.sqrt(dis)) / (2.0 * a)
			return (x1, x2)

