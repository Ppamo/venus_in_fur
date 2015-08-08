import pygame, termios, fcntl, sys, os, random, signal
from lib import config, audio_handler, button_handler, game_controller
from espeak import espeak
from threading import Timer

def signal_handler(signal, frame):
	print "signal handler"
	controller.looping = False

class scoreboard():
	def __init__(self):
		print "constructor"

	def terminate(self):
		self.ac.terminate()
		self.bc.terminate()

	def quit(self):
		print "quiting"
		self.looping = False

	def start_play(self):
		print "start play"
		while self.looping:
			print "loop"

	def run(self):
		print "running"
		try:
			self.start_play()
		finally:
			self.terminate()


signal.signal(signal.SIGTERM, signal_handler)
controller = scoreboard()
controller.run()


