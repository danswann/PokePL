import re
import sys


class PokException(Exception):
	def __init__(self, value):
		self.value = value


DECLARED = []
VARS = {'BULBASAUR': None, 'IVYSAUR': None, 'VENAUSAUR': None, 'CHARMANDER': None, 'CHARMELEON': None,
		'CHARIZARD': None, 'SQUIRTLE': None, 'WARTORTLE': None, 'BLASTOISE': None, 'CATERPIE': None, 'METAPOD': None,
		'BUTTERFREE': None, 'WEEDLE': None, 'KAKUNA': None, 'BEEDRILL': None, 'PIDGEY': None, 'PIDGEOTTO': None,
		'PIDGEOT': None, 'RATTATA': None, 'RATICATE': None, 'SPEAROW': None, 'FEAROW': None, 'EKANS': None,
		'ARBOK': None, 'PIKACHU': None, 'RAICHU': None, 'SANDSHREW': None, 'SANDSLASH': None, 'NIDORANM': None,
		'NIDORINA': None, 'NIDOQUEEN': None, 'NIDORANF': None, 'NIDORINO': None, 'NIDOKING': None, 'CLEAFAIRY': None,
		'CLEFABLE': None, 'VULPIX': None, 'NINETALES': None, 'JIGGLYPUFF': None, 'WIGGLYTUFF': None, 'ZUBAT': None,
		'GOLBAT': None, 'ODDISH': None, 'GLOOM': None, 'VILEPLUME': None, 'PARAS': None, 'PARASECT': None,
		'VENONAT': None, 'VENOMOTH': None, 'DIGLETT': None, 'DUGTRIO': None, 'MEOWTH': None, 'PERSIAN': None,
		'PSYDUCK': None, 'GOLDUCK': None, 'MANKEY': None, 'PRIMEAPE': None, 'GROWLITHE': None, 'ARCANINE': None,
		'POLIWAG': None, 'POLIWHIRL': None, 'ABRA': None, 'KADABRA': None, 'ALAKAZAM': None, 'MACHOP': None,
		'MACHOKE': None, 'MACHAMP': None, 'BELLSPROUT': None, 'WEEPINBELL': None, 'VICTREEBEL': None, 'TENTACOOL': None,
		'TENTACRUEL': None, 'GEODUDE': None, 'GRAVELER': None, 'GOLEN': None, 'PONYTA': None, 'RAPIDASH': None,
		'SLOWPOKE': None, 'SLOWBRO': None, 'MAGNEMITE': None, 'MAGNETON': None, 'FARFETCHD': None, 'DODUO': None,
		'DODRIO': None, 'SEEL': None, 'DEWGONG': None, 'GRIMER': None, 'MUK': None, 'SHELLDER': None, 'CLOYSTER': None,
		'GASTLY': None, 'HAUNTER': None, 'GENGAR': None, 'ONIX': None, 'DROWZEE': None, 'HYPNO': None, 'KRABBY': None,
		'KINGLER': None, 'VOLTORB': None, 'ELECTRODE': None, 'EXEGGCUTE': None, 'EXEGGUTOR': None, 'CUBONE': None,
		'MAROWAK': None, 'HITMONLEE': None, 'HITMONCHAN': None, 'LICKITUNG': None, 'KOFFING': None, 'WEEZING': None,
		'RHYHORN': None, 'RHYDON': None, 'CHANSEY': None, 'TANGELA': None, 'KANGASKHAN': None, 'HORSEA': None,
		'SEADRA': None, 'GOLDEEN': None, 'SEAKING': None, 'STARYU': None, 'STARMIE': None, 'MRMIME': None,
		'SCYTHER': None, 'JYNX': None, 'ELECTABUZZ': None, 'MAGMAR': None, 'PINSIR': None, 'TAUROS': None,
		'MAGIKARP': None, 'GYARADOS': None, 'LAPRAS': None, 'DITTO': None, 'EEVEE': None, 'VAPOREON': None,
		'JOLTEON': None, 'FLAREON': None, 'PORYGON': None, 'OMANYTE': None, 'OMASTAR': None, 'KABUTO': None,
		'KABUTOPS': None, 'AERODACTYL': None, 'SNORLAX': None, 'ARTICUNO': None, 'ZAPDOS': None, 'MOLTRES': None,
		'DRATINI': None, 'DRAGONAIR': None, 'DRAGONITE': None, 'MEWTWO': None, 'MEW': None}

def process(body):
	lines = body.split("\n")
	parenlvl = 0
	blocklvl = 0
	blockline = 0

	i = 0
	while i < len(lines):
		line = lines[i].strip()
		lineno = i + 1

		#DECLARATION
		prog = re.match('WILD ([a-zA-Z]+) APPEARED', line)
		if prog is not None:
			name = prog.group(1).upper()
			if name in VARS:
				if not name in DECLARED:
					DECLARED.append(name)
					continue
				else:
					raise PokException("Species %s has already been declared (line %d)." % (prog.group(1), lineno))
			else:
				raise PokException("Attempt to declare invalid species %s (line %d)." % (prog.group(1), lineno))

		#DESTRUCTION
		prog = re.match('WILD ([a-zA-Z]+) FAINTED', line)
		if prog is not None:
			name = prog.group(1).upper()
			if name in VARS:
				if name in DECLARED:
					DECLARED.remove(name)
					VARS[name] = None
					continue
				else:
					raise PokException("Attempt to delete undeclared species %s (line %d)." % (prog.group(1), lineno))
			else:
				raise PokException("Attempt to delete invalid species %s (line %d)." % (prog.group(1), lineno))

		#BASIC ASSIGNMENT
		prog = re.match('NAME ([a-zA-Z]+) [\'\"](.*?)[\'\"]', line)
		if prog is not None:
			name = prog.group(1).upper()
			if name in DECLARED:
				VARS[name] = prog.group(2)
				continue
			else:
				raise PokException("Attempt to assign '%s' to undeclared species %s (line %d)" % (prog.group(2), prog.group(1), lineno))
		prog = re.match('LEVEL ([a-zA-Z]+) (\d+\.?\d*)', line)
		if prog is not None:
			name = prog.group(1).upper()
			if name in DECLARED:
				VARS[name] = float(prog.group(2))
				continue
			else:
				raise PokException("Attempt to assign %s to undeclared species %s (line %d)" % (prog.group(2), prog.group(1), lineno))

		#


		i += 1