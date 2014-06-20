import random
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
		'ARBOK': None, 'PIKACHU': None, 'RAICHU': None, 'SANDSHREW': None, 'SANDSLASH': None, 'NIDORANF': None,
		'NIDORINA': None, 'NIDOQUEEN': None, 'NIDORANM': None, 'NIDORINO': None, 'NIDOKING': None, 'CLEAFAIRY': None,
		'CLEFABLE': None, 'VULPIX': None, 'NINETALES': None, 'JIGGLYPUFF': None, 'WIGGLYTUFF': None, 'ZUBAT': None,
		'GOLBAT': None, 'ODDISH': None, 'GLOOM': None, 'VILEPLUME': None, 'PARAS': None, 'PARASECT': None,
		'VENONAT': None, 'VENOMOTH': None, 'DIGLETT': None, 'DUGTRIO': None, 'MEOWTH': None, 'PERSIAN': None,
		'PSYDUCK': None, 'GOLDUCK': None, 'MANKEY': None, 'PRIMEAPE': None, 'GROWLITHE': None, 'ARCANINE': None,
		'POLIWAG': None, 'POLIWHIRL': None, 'ABRA': None, 'KADABRA': None, 'ALAKAZAM': None, 'MACHOP': None,
		'MACHOKE': None, 'MACHAMP': None, 'BELLSPROUT': None, 'WEEPINBELL': None, 'VICTREEBEL': None, 'TENTACOOL': None,
		'TENTACRUEL': None, 'GEODUDE': None, 'GRAVELER': None, 'GOLEM': None, 'PONYTA': None, 'RAPIDASH': None,
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


def evaluate_string(body):
	if str(type(body)) == "<class '_sre.SRE_Match'>":
		return evaluate_string(body.group(1))
	while "(-" in body and "-)" in body:
		body = re.sub('\(-([^\(\)-]+)-\)', evaluate_string, body)
	prog = re.match('(.+?) JOIN (.+)', body)
	if prog is not None:
		if re.match('["\'](.+?)["\']', prog.group(1)) is not None and re.match('["\'](.+?)["\']', prog.group(2)) is not None:
			body = prog.group(1) + prog.group(2)
			body = "\"" + body.replace("'","").replace("\"", "") + "\""
			return body
		else:
			body = evaluate_string(prog.group(1) + " JOIN " + evaluate_string(prog.group(2)))
	prog = re.match('([a-zA-Z]+)', body)
	if prog is not None:
		if prog.group(1).upper() in DECLARED:
			body = "\"" + VARS[prog.group(1).upper()] + "\""
	return str(body)


def finalize_string(x):
	return x[1:-1]


def evaluate_num(body):
	if str(type(body)) == "<class '_sre.SRE_Match'>":
		return evaluate_num(body.group(1))
	while "(-" in body and "-)" in body:
		body = re.sub('\(-([^\(\)-]+)-\)', evaluate_num, body)
	prog = re.match('(.+?) (BY|OVER) (.+)', body)
	if prog is not None:
		body = str(evaluate_num(prog.group(1))) + " " + prog.group(2) + " " + str(evaluate_num(prog.group(3)))
	prog = re.match('(.+?) (WITH|LESS) (.+)', body)
	if prog is not None:
		body = str(evaluate_num(prog.group(1))) + " " + prog.group(2) + " " + str(evaluate_num(prog.group(3)))
	prog = re.match('([a-zA-Z]+)', body)
	if prog is not None:
		name = prog.group(1).upper()
		if name in DECLARED:
			body = body.replace(name, str(VARS[name]))
		else:
			raise PokException("Attempt to evaluate undeclared species %s as a number." % prog.group(1))
	prog = re.match('(\d+\.?\d*) (BY|OVER) (\d+\.?\d*)', body)
	if prog is not None:
		if prog.group(2) == "BY":
			body = str(float(prog.group(1)) * float(prog.group(3)))
		else:
			body = str(float(prog.group(1)) / float(prog.group(3)))
	prog = re.match('(\d+\.?\d*) (WITH|LESS) (\d+\.?\d*)', body)
	if prog is not None:
		if prog.group(2) == "WITH":
			body = str(float(prog.group(1)) + float(prog.group(3)))
		else:
			body = str(float(prog.group(1)) - float(prog.group(3)))
	prog = re.match('(\d+\.?\d*)', body)
	if prog is not None:
		return body
	else:
		raise PokException("Unknown error attempting to evaluate num.")


def evaluate_bool(body):
	if str(type(body)) == "<class '_sre.SRE_Match'>":
		return evaluate_bool(body.group(1))
	while "(-" in body and "-)" in body:
		body = re.sub('\(-([^\(\)-]+)-\)', evaluate_bool, body)
	prog = re.match('(.+?) (AND|OR) (.+)', body)
	if prog is not None:
		body = str(evaluate_bool(prog.group(1))) + " " + prog.group(2) + " " + str(evaluate_bool(prog.group(3)))
	prog = re.match('NOT (.+)', body)
	if prog is not None:
		body = str(not finalize_bool(evaluate_bool(prog.group(1))))
	prog = re.match('(.+?) (SAME NAME AS|SAME LEVEL AS|STRONGER THAN|WEAKER THAN) (.+)', body)
	if prog is not None:
		if prog.group(2) == "SAME NAME AS":
			body = str(finalize_string(evaluate_string(prog.group(1))) == finalize_string(evaluate_string(prog.group(3))))
		elif prog.group(2) == "SAME LEVEL AS":
			body = str(float(evaluate_num(prog.group(1))) == float(evaluate_num(prog.group(3))))
		elif prog.group(2) == "STRONGER THAN":
			body = str(float(evaluate_num(prog.group(1))) > float(evaluate_num(prog.group(3))))
		else:
			body = str(float(evaluate_num(prog.group(1))) < float(evaluate_num(prog.group(3))))
	prog = re.match('(True|False) (AND|OR) (True|False)', body)
	if prog is not None:
		if prog.group(2) == "AND":
			body = str(True if prog.group(1) == "True" and prog.group(3) == "True" else False)
		else:
			body = str(True if prog.group(1) == "True" or prog.group(3) == "True" else False)
	prog = re.match('(True|False)', body)
	if prog is not None:
		return str(True if prog.group(1) == "True" else False)
	else:
		raise PokException("Unknown error attempting to evaluate bool.")


def finalize_bool(x):
	return True if x == "True" else False


def process(body):
	lines = body.split("\n")
	blocklvl = 0
	blockdata = []

	i = 0
	while i < len(lines):
		line = lines[i].strip()
		lineno = i + 1

		#COMMENTS AND BLANKS
		if line == "" or line[0] == "~":
			i += 1
			continue

		#DECLARATION
		prog = re.match('WILD ([a-zA-Z]+) APPEARED', line)
		if prog is not None:
			name = prog.group(1).upper()
			if name in VARS:
				if not name in DECLARED:
					DECLARED.append(name)
					i += 1
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
					i += 1
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
				i += 1
				continue
			else:
				raise PokException("Attempt to assign '%s' to undeclared species %s (line %d)" % (prog.group(2), prog.group(1), lineno))
		prog = re.match('LEVEL ([a-zA-Z]+) (\d+\.?\d*)', line)
		if prog is not None:
			name = prog.group(1).upper()
			if name in DECLARED:
				VARS[name] = float(prog.group(2))
				i += 1
				continue
			else:
				raise PokException("Attempt to assign %s to undeclared species %s (line %d)" % (prog.group(2), prog.group(1), lineno))

		#ADVANCED ASSIGNMENT
		prog = re.match('NAME ([a-zA-Z]+) LIKE (.+)', line)
		if prog is not None:
			name = prog.group(1).upper()
			if name in DECLARED:
				VARS[name] = finalize_string(evaluate_string(prog.group(2)))
				i += 1
				continue
			else:
				raise PokException("Attempt to assign to undeclared species %s (line %d)" % (prog.group(1), lineno))
		prog = re.match('LEVEL ([a-zA-Z]+) LIKE (.+)', line)
		if prog is not None:
			name = prog.group(1).upper()
			if name in DECLARED:
				VARS[name] = float(evaluate_num(prog.group(2)))
				i += 1
				continue
			else:
				raise PokException("Attempt to assign to undeclared species %s (line %d)" % (prog.group(1), lineno))

		#BLOCKS
		prog = re.match('IS (.+?)\?', line)
		if prog is not None:
			if finalize_bool(evaluate_bool(prog.group(1))):
				blockdata.append({"type": "IS", "val": i})
				blocklvl += 1
				i += 1
			else:
				while lines[i] != "OKAY":
					i += 1
			continue
		prog = re.match('BATTLE (.+)', line)
		if prog is not None:
			if finalize_bool(evaluate_bool(prog.group(1))):
				blockdata.append({"type": "BATTLE", "val": i})
				blocklvl += 1
			else:
				while lines[i] != "OKAY":
					i += 1
			i += 1
			continue
		if line == "OKAY":
			try:
				data = blockdata.pop()
				if data['type'] == "BATTLE":
					i = data.val
				else:
					i += 1
			except IndexError:
				i += 1
			blocklvl -= 1
			continue

		#FUNCTIONS
		prog = re.match('([a-zA-Z]+) USED ([A-Z]+)(?: ON (.+))?', line)
		if prog is not None:
			name = prog.group(1).upper()
			func = prog.group(2)
			if name not in DECLARED:
				raise PokException("Attempt to call function by undeclared species %s (line %d)" % (prog.group(1), lineno))
			if func == "CONVERSION":
				try:
					orig = prog.group(3)
				except IndexError:
					orig = prog.group(1)
				VARS[name] = float(finalize_string(evaluate_string(orig)))
				i += 1
				continue

			elif func == "TRANSFORM":
				try:
					orig = prog.group(3)
				except IndexError:
					orig = prog.group(1)
				VARS[name] = str(evaluate_num(orig))
				i += 1
				continue

			elif func == "GROWL":
				print(VARS[name])
				i += 1
				continue

			elif func == "SUBSTITUTE":
				VARS[name] = input(prog.group(1) + "?: ")
				i += 1
				continue

			elif func == "METRONOME":
				try:
					max = prog.group(3)
				except IndexError:
					raise PokException("METRONOME called with no max (line %d)" % lineno)
				VARS[name] = random.randint(0, int(float(evaluate_num(max))))
				i += 1
				continue

		raise PokException("Cannot interpret line %s (%d)" % (line, lineno))


if __name__ == "__main__":
	if len(sys.argv) == 2:
		f = open(sys.argv[1])
		process(f.read())
		f.close()
	else:
		print("ppl.py <filename>")
		sys.exit(1)