
import numpy as np
import random

from adev.cell import Cell

class Region(object):
	def __init__(self, region_id, width, height, cell_opt):
		self.region_id = region_id
		obj_list = [[Cell(i, j, cell_opt) for i in range(0, width)] for j in range(0, height)]
		self.region = np.array(obj_list, dtype=object)
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
