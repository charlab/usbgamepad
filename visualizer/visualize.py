#!/usr/bin/python

# By Josef Spjut
# October 2014

import pygame

class App:
	def __init__(self):
		self.ON = True
		self.bg_color = (30,30,30)
		off_color = (200,200,200)
		on_color = (170,120,200)
		other_color = (63,63,63)
		#for joystick sizing/location
		self.js_colors = (off_color,other_color,on_color)
		self.js_center = [[220,400],[420,400]]
		self.js_size = (25, 50)
		self.js_move = self.js_size[1] - self.js_size[0]
		# button size/location	x 		a 			b 		y 			l1 		r1 			l2 		r2 		select 		start	
		self.btn_center = ((450,250),(500,300),(550,250),(500,200),(200,150),(440,150),(200,100),(440,100),(280,200),(360,200))
		self.btn_colors = (off_color,on_color)
		# hat? d-pad?
		self.hat_center = ((90,250),(140,300),(190,250),(140,200))
		self.hat_colors = (off_color,on_color)

		pygame.init()

		pygame.display.set_caption("Joystick Visualizer")

		# set up screen
		self.screen = pygame.display.set_mode( (640, 480) )

		# Set up Joystick
		pygame.joystick.init()

		self.my_joystick = None
		self.joystick_names = []

		# Enumerate joysticks
		for i in range(0, pygame.joystick.get_count()):
			self.joystick_names.append(pygame.joystick.Joystick(i).get_name())

		print self.joystick_names

		# By default, load the first available joystick.
		if (len(self.joystick_names) > 0):
			self.my_joystick = pygame.joystick.Joystick(0)
			self.my_joystick.init()
			self.num_buttons = self.my_joystick.get_numbuttons()
		else:
			print 'No joystick detected.'
			self.quit()

	def quit(self):
		pygame.display.quit()
		self.ON = False

	def read_buttons(self):
		self.buttons = []
		for i in xrange(self.num_buttons):
			self.buttons.append(self.my_joystick.get_button(i))

	def read_hat(self):
		self.hat = self.my_joystick.get_hat(0)
		self.d_pad = [self.hat[0] == -1, self.hat[1] == -1, self.hat[0] == 1, self.hat[1] == 1]

	def run(self):
		while(self.ON):
			events = pygame.event.get()

			self.screen.fill(self.bg_color)

			# read current button state
			self.read_buttons()
			#stick buttons handled later
			for i in xrange(self.num_buttons-2): 
				btn_color = self.btn_colors[0]
				if self.buttons[i]: btn_color = self.btn_colors[1]
				pygame.draw.circle(self.screen, btn_color, self.btn_center[i], 20)

			# d-pad
			self.read_hat()
			for i in xrange(4):
				pad_color = self.hat_colors[0]
				if self.d_pad[i]: pad_color = self.hat_colors[1]
				pygame.draw.circle(self.screen, pad_color, self.hat_center[i], 20)

			# left stick
			ls_pressed = self.buttons[10]
			if ls_pressed: ls_color = self.js_colors[2]
			else: ls_color = self.js_colors[0]
			pygame.draw.circle(self.screen, ls_color, self.js_center[0], self.js_size[1])
			pygame.draw.circle(self.screen, self.js_colors[1], (self.js_center[0][0]+int(self.js_move * self.my_joystick.get_axis(0)), self.js_center[0][1]+int(self.js_move * self.my_joystick.get_axis(1))), self.js_size[0])
			
			# right stick
			rs_pressed = self.buttons[11]
			if rs_pressed: rs_color = self.js_colors[2]
			else: rs_color = self.js_colors[0]
			pygame.draw.circle(self.screen, rs_color, self.js_center[1], self.js_size[1])
			pygame.draw.circle(self.screen, self.js_colors[1], (self.js_center[1][0]+int(self.js_move * self.my_joystick.get_axis(2)), self.js_center[1][1]+int(self.js_move * self.my_joystick.get_axis(3))), self.js_size[0])
			
			# allow quitting
			for event in events:
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.quit()
				elif event.type == pygame.QUIT:
					self.quit()

			# prevent drawing when the app quits
			if self.ON:
				pygame.display.flip()


if __name__ == '__main__':
	app = App()
	app.run()
