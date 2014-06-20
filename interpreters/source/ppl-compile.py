import re
import sys


def convert(text):
	lines = text.split("\n")
	out = []
	indentlevel = 0
	for line in lines:
		indentnext = False

		line = line.strip()
		line = line.replace("~", "#")
		line = re.sub("WILD ([a-zA-Z]+) APPEARED", "\\1 = None", line)
		line = re.sub("WILD ([a-zA-Z]+) FAINTED", "del \\1", line)
		line = re.sub("NAME ([a-zA-Z]+) ([\"\'].*?[\"\'])", "\\1 = \\2", line)
		line = re.sub("LEVEL ([a-zA-Z]+) (\d+?\.?\d*)", "\\1 = \\2", line)
		line = re.sub("NAME ([a-zA-Z]+) LIKE", "\\1 =", line)
		line = re.sub("LEVEL ([a-zA-Z]+) LIKE", "\\1 =", line)
		line = line.replace("WITH", "+")
		line = line.replace(" LESS ", " - ")
		line = line.replace(" BY ", " * ")
		line = line.replace(" OVER ", " / ")
		line = line.replace("LEVELED UP", "+= 1")
		line = line.replace(" JOIN ", " + ")
		line = line.replace("NOT ", "not ")
		line = line.replace(" AND ", " and ")
		line = line.replace(" OR ", " or ")
		line = line.replace("SAME AS", "==")
		line = line.replace("STRONGER THAN", ">")
		line = line.replace("WEAKER THAN", "<")
		if line[:3] == "IS ":
			line = line.replace("IS", "if")
			line = line.replace("?", ":")
			indentnext = True
		if line[:6] == "BATTLE":
			line = line.replace("BATTLE", "while")
			line += ":"
			indentnext = True
		if line[:4] == "OKAY":
			line = line.replace("OKAY", "")
			indentlevel -= 1

		if "USED" in line:
			prog = re.match("([a-zA-Z]+) USED ([a-zA-Z]+)(?: ON ([a-zA-Z0-9]+))?", line)
			if prog is not None:
				if prog.group(2) == "GROWL":
					line = "print(%s)" % prog.group(1)
				elif prog.group(2) == "SUBSTITUTE":
					line = "%s = input('%s?: ')" % (prog.group(1), prog.group(1))

		for i in range(indentlevel):
			line = "\t"+line
		if indentnext:
			indentlevel += 1

		out.append(line)

	return "\n".join(out)


if __name__ == "__main__":
	if len(sys.argv) == 2:
		f = open(sys.argv[1])
		d = f.read()
		f.close()
		exec(convert(d))
	else:
		print("ppl-compile.py <filename>")
		sys.exit(1)