import pygame, termios, fcntl, sys, os, random, signal, time
from random import randint
from threading import Timer

def signal_handler(signal, frame):
	print "signal handler"
	self.looping = False

class venus():

	def __init__(self):
		print "constructor"
		pygame.mixer.pre_init(44100, -16, 2, 2048)
		pygame.init()
		pygame.mixer.set_num_channels(12)
		self.keyboard_handlers = { 	'q': self.quit,
						't': self.test_mode,
						'n': self.normal_mode }
		self.looping = True;
		self.current_play = []
		self.current_play_len = -1
		self.current_fade = -1
		self.next_play = []
		self.next_play_len = -1
		self.next_fade = -1
		self.timer_len = 2
		self.dice_roller = self.random_dice_roller
		self.timer = Timer(self.timer_len, self.tick)

	def terminate(self):
		print "terminate"
		pygame.mixer.quit()

	def quit(self):
		print "quiting"
		self.looping = False

	def tick(self):
		if (not self.looping):
			return False
		print "tic play = {} fade = {}".format(self.current_play_len, self.current_fade)
		if self.current_play_len > 0:
			if self.current_play_len < self.current_fade:
				step = float(self.current_fade - self.current_play_len) / self.current_fade
				print "set next_play volume to {}".format(step)
				for channel in self.next_play:
					self.channels[channel].set_volume(step)
				print "set current_play volume to {}".format(1 - step)
				for channel in self.current_play:
					self.channels[channel].set_volume(1 - step)
			if self.current_play_len == self.current_fade:
				print "fading into {}".format("".join(str(self.next_play)))
		if self.current_play_len == 0:
			print "change tracks"
			for channel in self.next_play:
				self.channels[channel].set_volume(1)
			for channel in self.current_play:
				self.channels[channel].set_volume(0)
			self.current_play = self.next_play
			self.current_play_len = self.next_play_len
			self.current_fade = self.next_fade
			self.dice_roller()
		self.current_play_len-=1
		self.timer = Timer(self.timer_len, self.tick)
		self.timer.start()

	def start_play(self):
		print "start play"
		self.load_audios()
		self.play_audios()
		self.dice_roller()
		self.current_fade = 20
		self.current_play_len = self.current_fade - 1
		self.timer.start()

	def test_mode(self):
		print "running test plan"
		self.dice_roller = self.test_dice_roller
		self.next_play = [0]
		self.next_play_len = 20
		self.next_fade = 5
		print "the dice says {}".format("".join(str(self.next_play)))

	def normal_mode(self):
		print "running randomic mode"
		self.dice_roller = self.random_dice_roller
		self.dice_roller()

	def test_dice_roller(self):
		print "test plan"
		self.next_play_len = 20
		self.next_fade = 5
		next_track = (self.next_play[0] + 1) % self.files_count
		self.next_play = [next_track]
		print "the dice says {}".format("".join(str(self.next_play)))

	def random_dice_roller(self):
		print "roll the dice"
		self.next_play_len = randint(60, 180)
		self.next_fade = randint(2, self.next_play_len)
		q = randint(1, 6)
		self.next_play = []
		for i in range(q):
			self.next_play.append(randint(0, self.files_count - 1))
		print "the dice says {}".format("".join(str(self.next_play)))

	def play_audios(self):
		print "playing files"
		for i in range(self.files_count):
			self.channels[i].play(self.sounds[i], -1)

	def load_audios(self):
		print "load_audios"
		self.files = [	'audio/v1.2/Track 1.ogg',
				'audio/v1.2/Track 2.ogg',
				'audio/v1.2/Track 3.ogg',
				'audio/v1.2/Track 4.ogg',
				'audio/v1.2/Track 6.ogg',
				'audio/v1.2/Track 8.ogg',
				'audio/v1.2/Track 9.ogg',
				'audio/v1.2/Track 11.ogg' ]
		self.files_count = len(self.files)
		self.channels = {}
		self.sounds = {}
		for i in range(self.files_count):
			print "loading file {}".format(i)
			self.sounds.update({i: pygame.mixer.Sound(self.files[i])})
			self.channels.update({i: pygame.mixer.Channel(i)})
			self.channels[i].set_volume(0.0)

	def run(self):
		print "running"
		try:
			self.start_play()
			while self.looping:
				try:
					print "reading keyboard"
					c = sys.stdin.read(1)
					if c in self.keyboard_handlers:
						self.keyboard_handlers[c]()
				except IOError: pass
		finally:
			self.terminate()


signal.signal(signal.SIGTERM, signal_handler)
controller = venus()
controller.run()


