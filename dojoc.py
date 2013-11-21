#!/usr/bin/python
# Author: Gustavo Brito (GustavoKatel)

import sys, os, re, subprocess

from dojoc_test import DojoCTest

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'

class DojoC:

	types    = { "%s":"char *", "%d":"int", "%c":"char", "%f":"float" }
	default_values = { "%s":"\"None\"", "%d":"0", "%c":"0", "%f":"0f" }

	return_type = "" # must be in types
	params = [] # each element must be in types

	test_cases = []

	def __init__(self, unit, debugMode):
		self.unit = unit
		self.testfile = unit+".test"
		if not os.path.exists(self.testfile):
			print self.testfile+" not found!"
			sys.exit(1)
		self.sys_dir = os.path.dirname(os.path.realpath(__file__))

		self.debugMode = debugMode	
	
		self.processTestFile()

	def new(self):
		# create initial file
		ufile = open(self.sys_dir+ os.sep + "unit.c.model")
		unitfile = "".join(ufile.readlines())
		ufile.close()

		unitfile = unitfile.replace("%unit%", self.unit)
		unitfile = unitfile.replace("%return_type%", self.types[self.return_type] )
		unitfile = unitfile.replace("%default_ret%", self.default_values[self.return_type] )
		
		plist = ""
		for i in range(len(self.params)):
			plist = plist + self.types[self.params[i]] + " p"+str(i)
			if i<len(self.params)-1:
				plist = plist+", "

		unitfile = unitfile.replace("%params%", plist)
		
		ufile = open(self.unit+".c", "w")
		ufile.write(unitfile)
		ufile.close()
		

	def test(self):
		# create Makefile
		mfile = open(self.sys_dir+ os.sep + "Makefile.model" )
		makefile = "".join(mfile.readlines())
		mfile.close()
	
		makefile = makefile.replace("%unit%", self.unit)

		mfile = open("Makefile", "w")
		mfile.write(makefile)
		mfile.close()
		
		# create compilable file
		cfile = open(self.unit+".c")
		content = "".join(cfile.readlines())
		cfile.close()
		
		content = content+ "\nint main(int argc, char **argv)\n{\n\n%test%\n\n\treturn 0;\n}\n"

		# inject the test cases
		teststr = ""
		for test in self.test_cases:
			fn = test.getTestFunc()
			fn = "printf(\""+self.return_type+"\\n\", "+fn+");\n"
			teststr = teststr + fn
		content = content.replace("%test%", teststr)
		
		cfile = open("."+self.unit+".c", "w")
		cfile.write(content)
		cfile.close()

		# compile
		ret = os.system("make")
		if ret>0:
			print bcolors.FAIL+ "NOT PASS" + bcolors.ENDC
			sys.exit(1)

		# execute
		output = subprocess.check_output("./"+self.unit)
		lines = output.split("\n")
		for i in range(len(lines)):
			val = lines[i]
			if val=="" or val=="\n":
				continue
			print "\n" + bcolors.HEADER  + "Test #"+str(i) + bcolors.ENDC
			print self.test_cases[i].toString()
			if self.test_cases[i].test(val)==True:
				print "Result: "+ bcolors.OKGREEN +"PASS" + bcolors.ENDC
			else:
				print "Result: "+ bcolors.FAIL + "NOT PASS" + bcolors.ENDC
				print "Expected: "+str(self.test_cases[i].getReturnVal())
				print "Received: "+str(val)
				sys.exit(1)
			print "----------------------------------------"
		if not self.debugMode:
			subprocess.check_output("make clean-no-exe", shell=True)

	def _getline(self, tfile):
		line = tfile.readline()
		# remove comments
		if line.find("#")>=0:
			line = line[:line.find("#")]
		return line


	def processTestFile(self):
		# process the mask pattern
		tfile = open(self.testfile)
		pattern_types = self._getline(tfile) # tfile.readline()

		regex = "((%[a-z]),)*(%[a-z])=(%[a-z])"
		pattern_types = pattern_types.replace(" ", "")
		m = re.match(regex, pattern_types)
		items = m.groups()
		for i in range(len(items)-1):
			if i==0 or items[i]==None:
				continue
			self.params.append(items[i])
		self.return_type = items[i+1]
	
		# process the test cases
		line = "ignore me!"
		while not line=="":
			line = self._getline(tfile) # tfile.readline()
			if line.strip()=="":
				continue

			line = "(["+line[:-1]+")"
			line = line.replace("=", "],")
			line = "(params, return_val) = "+line
			exec(line)
			self.test_cases.append(DojoCTest(self.unit, params,return_val))
	

		tfile.close()


if __name__=="__main__":
	if len(sys.argv)>=3:
		operador = sys.argv[1]
		unidade  = sys.argv[2]
		
		debug = False
		if len(sys.argv)>=4:
			if sys.argv[3]=="debug":
				debug = True

		dojoc = DojoC(unidade, debug)

		if operador=="new":
			dojoc.new()
		elif operador=="test":
			dojoc.test()
	else:
		print "python dojoc.py [new|test] unitName"
