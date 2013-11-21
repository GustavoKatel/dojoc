#!/usr/bin/python

import sys, os, time

sys_dir = os.path.dirname(os.path.realpath(__file__))

class Timer:

	timerout_text = ""

	def __init__(self):
		f = open(sys_dir+os.sep+ "timerout.txt")
		self.timerout_text = "".join(f.readlines())
		f.close()

	def start(self, seconds):
		print "Timer started!"
		print "\"python "+sys_dir+os.sep+"dojoc_timer.py stop\" to kill"
		pid = os.fork()
		if pid==0:
			while True:
				time.sleep(seconds)
				print self.timerout_text
		else:
			print "Timer pid: "+str(pid)
			f = open(sys_dir+os.sep+ "timer.pid", "w")
			f.write(str(pid))
			f.close()


if __name__=="__main__":
	if len(sys.argv)==2:
		arg = sys.argv[1]

		if arg=="stop":
			f = open(sys_dir+os.sep+"timer.pid")
			pid = f.readline()
			f.close()
			os.system("kill "+pid)
		else:
			timer = Timer()
			timer.start(arg)


