import math
# A module containing functions in the game

def coord_add(p1, p2):
	return ((p1[0] + p2[0]), (p1[1] + p2[1]))


def coord_subtract(p1, p2):
	return ((p1[0] - p2[0]), (p1[1] - p2[1]))


def distance (p1, p2):
    return math.sqrt(coord_subtract(p1, p2)[0]**2 + coord_subtract(p1, p2)[1]**2)
