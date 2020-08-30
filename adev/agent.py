
import random
import math
import struct

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

class Agent(object):
	def __init__(self, opt):
		self.ix = -1
		self.iy = -1
		self.cx = -1
		self.cy = -1
		
		self.opt = opt
		pass

	def __str__(self):
		return f"{self.opt.aid}|"

	def move(self, perception):
		next_coord = (0, 0)
		if self.opt.get_mode() == "RANDOM":
			next_coord = self.random_move()
		elif self.opt.get_mode() == "OBJ_GREED":
			next_coord = self.objective_move(perception)
		else:
			pass
		
		return next_coord

	def random_move(self, perception):
		selected_cell = random.choice(perception)
		return selected_cell.get_cell_idx()

	def set_objective(self, object_map):
		self.objective = object_map
		self.coordX, self.coordY = random.choice(self.objective)

	def objective_move(self, perception):
		if self.objective == None:
			return self.random_move()
		else:
			
			'''
			double rad = Math.Atan2((targetPosition.Y - _currentPosition.Y), (targetPosition.X - _currentPosition.X));

            double dx = AgentSpeed * time * Math.Cos(rad);
            double dy = AgentSpeed * time * Math.Sin(rad);
            _currentPosition.X += dx;
            _currentPosition.Y += dy;
			'''
			#for cell in perception:
			perception = sorted(perception, key=lambda cell:cell.get_cell_status())
			
			rad = math.atan2((self.coordY - self.iy), (self.coordX - self.ix))
			dx = math.cos(rad)
			dy = math.sin(rad)

			self.ix += dx;
			self.iy += dy;

#			print((int(self.ix), int(self.iy)), (dx, dy))
#			print(self.opt.aid, (self.cx - int(self.ix), self.cy - int(self.iy)))
			return (int(self.ix - self.cx), int(self.iy - self.cy))

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