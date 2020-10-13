
import numpy as np
import random

from adev.cell import Cell
from adev.cell import UniCell

class Region(object):
	def __init__(self, region_id, width, height):
		self.region_id = region_id
		self.region_agents = []
		self.active_cells = []
		self.region_entry_points = {}
		self.region_exit_points = {}
		self.region_check_points = {}

	def __repr__(self):
		return repr(self.region)

	def get_region_id(self):
		return self.region_id

	def update_cell(self, ix, iy, cell_opt):
		self.region[iy, ix] = Cell(ix, iy, cell_opt)

	def get_shape(self):
		return self.region.shape

	def get_matrix(self):
		return self.region

	def add_entry_points(self, entry_id, coord_lst):
		self.region_entry_points[entry_id] = coord_lst
		return entry_id
	
	def get_entry_points(self):
		return self.region_entry_points

	def get_exit_points(self):
		return self.region_exit_points
	
	def add_exit_points(self, exit_id, coord_lst):
		self.region_exit_points[exit_id] = coord_lst 
		self.region_check_points[coord_lst] = exit_id
		return exit_id

	def add_agent(self, coord, agent):
		if agent not in self.region_agents: 
			self.region_agents.append(agent)
		agent.set_objective(list(self.region_exit_points.values()))
		self.update_agent(coord, agent)		

	def update_agent(self, coord, agent):
		self.region[coord[1], coord[0]].insert_agent(agent)

		if not self.region[coord[1], coord[0]] in self.active_cells:
			self.active_cells.append(self.region[coord[1], coord[0]])


	def remove_agent(self, coord, agent):
		self.region[coord[1], coord[0]].remove_agent(agent)

		if not self.region[coord[1], coord[0]].get_agents():
			self.active_cells.remove(self.region[coord[1], coord[0]])

	def reached_to_exit(self, agent):
		coord = agent.get_cell_idx()
		if coord in self.region_check_points.keys():
			return True
		else:
			return False

	def find_exit_port(self, coord):
		return f"agent_out[{self.region_check_points[coord]}]"

	def schedule(self, _mode = "NORMAL"):
		if self.active_cells:
			
			if _mode == "NORMAL":
				# random.shuffle(self.active_cells)
				agents_lst = []
				for cell in self.active_cells:
					agents = cell.get_active_agents()
					agents_lst.extend(agents)

				return agents_lst
		else:
			return list()

	def plot(self):
		print(self.region)

	def region_to_string(self):
		return self.region.__str__()

	def packing(self):
		ba = bytearray()
		ba.append(self.region.shape[0])
		ba.append(self.region.shape[1])

		for row in self.region:
			for column in row:
				ba.append(len(column.get_agents()))

		return ba

class CustomRegion(Region):
	def __init__(self, region_id, width, height, cell_opt):
		Region.__init__(self, region_id, width, height)
		obj_list = [[Cell(i, j, cell_opt) for i in range(0, width)] for j in range(0, height)]
		self.region = np.array(obj_list, dtype=object)
		pass

	def __repr__(self):
		return repr(self.region)

	def alter_cell(self, ix, iy, cell_opt):
		self.region[iy, ix] = Cell(ix, iy, cell_opt)

import functools
import operator
import re

class UniqueRegion(Region):
	def __init__(self, region_id, width, height):
		Region.__init__(self, region_id, width, height)
		obj_list = [[UniCell(i, j) for i in range(0, width)] for j in range(0, height)]
		self.region = np.array(obj_list, dtype=object)
		self.waiting_agents = []


	def __repr__(self):
		return repr(self.region)

	def alter_cell(self, ix, iy, cell_opt):
		self.region[iy, ix] = Cell(ix, iy, cell_opt)

	def add_agent(self, coord, agent):
		if agent not in self.region_agents: 
			self.region_agents.append(agent)
		agent.set_objective(list(self.region_exit_points.values()))
		self.update_agent(coord, agent)		

	def remove_agent(self, coord, agent):
		self.region[coord[1], coord[0]].remove_agent(agent)

		if not self.region[coord[1], coord[0]].get_agents():
			self.active_cells.remove(self.region[coord[1], coord[0]])
	
	def update_agent(self, coord, agent):
		if self.region[coord[1], coord[0]].get_cell_status() == 0:
			self.region[coord[1], coord[0]].insert_agent(agent)

			if not self.region[coord[1], coord[0]] in self.active_cells:
				self.active_cells.append(self.region[coord[1], coord[0]])
		else:
			agent.penalty()

	def reached_to_exit(self, agent):
		coord = agent.get_cell_idx()
		if coord in self.region_check_points.keys():
			return True
		else:
			return False

	def find_exit_port(self, coord):
		return f"agent_out[{self.region_check_points[coord]}]"

	def pre_execution(self):
		if self.active_cells:
			for cell in self.active_cells:
				agents = cell.get_active_agents()
				self.waiting_agents.extend(agents)
				
			random.shuffle(self.waiting_agents)
			return self.waiting_agents
		else:
			return None
	
	def execution(self):
		candidate_move = {}

		if self.waiting_agents:
			for agent in self.waiting_agents:
			# TODO call agent's perceive function
				perception = []
				ix, iy = agent.get_cell_idx()

				if ix > 0 and ix < self.region.shape[1]-1 and \
				iy > 0 and iy < self.region.shape[0]-1 :                   
					perception = functools.reduce(operator.iconcat, self.region[iy-1:iy+2, ix-1:ix+2].tolist(), [])
				elif ix == 0 and iy > 0 and iy < self.region.shape[0]-1 : 
					perception = functools.reduce(operator.iconcat, self.region[iy-1:iy+2, ix:ix+2].tolist(), [])
				elif iy == 0 and ix > 0 and ix < self.region.shape[1]-1 : 
					perception = functools.reduce(operator.iconcat, self.region[iy:3, ix-1:ix+1].tolist(), [])
				elif iy == 0 and ix == 0 : 
					perception = functools.reduce(operator.iconcat, self.region[iy:iy+2, ix:ix+2].tolist(), [])
				elif ix == self.region.shape[1]-1 and iy > 0 and iy < self.region.shape[0]-1 : 
					perception = functools.reduce(operator.iconcat, self.region[iy-1:iy+1, ix-1:ix+1].tolist(), [])
				elif iy == self.region.shape[0]-1 and ix > 0 and ix < self.region.shape[1]-1 : 
					perception = functools.reduce(operator.iconcat, self.region[iy-1:iy+1, ix-1:ix+1].tolist(), [])
				elif iy == self.region.shape[0]-1 and ix == self.region.shape[1]-1 : 
					perception = functools.reduce(operator.iconcat, self.region[iy-1:iy+1, ix-1:ix+1].tolist(), [])

				nx, ny = agent.move(perception)
				if not(nx == 0 and ny == 0): 
					if self.region[ny, nx].get_agents():
						agent.penalty()
					else:
						self.remove_agent((ix, iy), agent)
						self.update_agent((nx, ny), agent)
						agent.reset_schedule()

			self.waiting_agents.clear()
		pass
	
	def post_execution(self):
		exit_agent_lst = []
		for coord in self.region_check_points.keys():
			if self.region[coord[1], coord[0]].get_agents():
				exit_agent_lst.extend(self.region[coord[1], coord[0]].get_agents())
				for agent in self.region[coord[1], coord[0]].get_agents():
					self.remove_agent(coord, agent)
					self.region_agents.remove(agent)
		return exit_agent_lst

	def schedule(self, _mode = "NORMAL"):
		if self.active_cells:
			
			if _mode == "NORMAL":
				# random.shuffle(self.active_cells)
				agents_lst = []
				for cell in self.active_cells:
					agents = cell.get_active_agents()
					agents_lst.extend(agents)

				return agents_lst
		else:
			return list()

	def plot(self):
		print(self.region)

	def region_to_string(self):
		return self.region.__str__()

	def packing(self):
		ba = bytearray()
		ba.append(self.region.shape[0])
		ba.append(self.region.shape[1])

		for row in self.region:
			for column in row:
				ba.append(len(column.get_agents()))

		return ba
