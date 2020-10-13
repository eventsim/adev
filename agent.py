
import random
import math
import struct
import numpy as np

class AgentOpt(object):
	def __init__(self, region, aid, mode):
		'''
		mode: Objective, Random

		'''
		self.region = region
		self.aid = aid
		self.mode = mode
		self.objective = None
		pass

	def get_mode(self):
		return self.mode

	def decrease(self):
		return -1

class Agent(object):
	def __init__(self, opt):
		self.ix = -1
		self.iy = -1
		self.cx = -1
		self.cy = -1
		
		self.opt = opt

		self.schedule_t = 1
		pass

	def __str__(self):
		return f"{self.opt.aid}|"

	def get_id(self):
		return self.opt.aid

	def move(self, perception):
		next_coord = (0, 0)
		if self.opt.get_mode() == "RANDOM":
			next_coord = self.random_move()
		elif self.opt.get_mode() == "OBJ_GREED":
			next_coord = self.objective_move(perception)
		elif self.opt.get_mode() == "OBJ_SMART":
			next_coord = self.smart_move(perception)
		else:
			pass
		
		return next_coord

	def random_move(self, perception):
		selected_cell = random.choice(perception)
		return selected_cell.get_cell_idx()

	def set_objective(self, object_map):
		self.objective = object_map
		self.coordX, self.coordY = random.choice(self.objective)

	'''
	def objective_move(self, perception):
		if self.objective == None:
			return self.random_move()
		else:
			#for cell in perception:
			perception = sorted(perception, key=lambda cell:cell.get_cell_status())
			
			rad = math.atan2((self.coordY - self.iy), (self.coordX - self.ix))
			dx = math.cos(rad)
			dy = math.sin(rad)

			self.ix += dx;
			self.iy += dy;

			return (int(self.ix - self.cx), int(self.iy - self.cy))
	'''

	def objective_move(self, perception):
		if self.objective == None:
			return self.random_move()
		else:
			basis = self.cal_weight((self.coordX, self.coordY), (self.ix, self.iy))

			next_move = None
			for cell in perception:
				if basis >= self.cal_weight((self.coordX, self.coordY), cell.get_cell_idx()):
					basis = self.cal_weight((self.coordX, self.coordY), cell.get_cell_idx())
					next_move = cell.get_cell_idx()

			if next_move:
				return next_move
			else:
				return (0, 0)

	def cal_weight(self, coord1, coord2):
		return pow((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2, 0.5) 

	def smart_move(self, perception):
		if self.objective == None:
			return self.random_move()
		else:
			#for cell in perception:
			# find nearest exit
			'''
			basis = self.cal_weight((self.coordX, self.coordY), (self.ix, self.iy))
			'''
			exit_coord = self.objective[0]
			basis = self.cal_weight(self.objective[0], (self.ix, self.iy))
			
			for exit in self.objective:
				if basis >= self.cal_weight(exit, (self.ix, self.iy)):
					basis = self.cal_weight(exit, (self.ix, self.iy))
					exit_coord = exit
					
			filtered = list(filter(lambda x: len(x.get_agents()) == 0, perception))

			next_move = None
			for cell in filtered:
				if basis >= self.cal_weight(exit_coord, cell.get_cell_idx()):
					basis = self.cal_weight(exit_coord, cell.get_cell_idx())
					next_move = cell.get_cell_idx()

			if next_move:
				return next_move
			else:
				return (0, 0)

	def register_cell(self, ix, iy):
		self.ix = ix
		self.iy = iy
		self.cx = ix
		self.cy = iy

	def get_cell_idx(self):
		return (self.cx, self.cy)

	def packing(self):
		ba = bytearray()
		ba.extend(struct.pack("i", self.opt.aid))
		
		return ba

	def penalty(self):
		self.schedule_t += 5		
		#print(f"[P]ID:{self.opt.aid}, Time:{self.schedule_t}")


	def is_schedule(self):
		self.schedule_t += self.opt.decrease()
		#print(f"[S]ID:{self.opt.aid}, Time:{self.schedule_t}")
		return self.schedule_t <= 0

	def reset_schedule(self):
		self.schedule_t = 1
		#print(f"[R]ID:{self.opt.aid}, Time:{self.schedule_t}")
