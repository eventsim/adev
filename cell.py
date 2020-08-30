class CellOpt(object):
	def __init__(self, capacity=2):
		self.capacity = capacity
		self.congestion_mid = 0.33
		self.congestion_high = 0.66
		pass

	def set_threshold(self, thres_lst):
		self.congestion_mid = thres_lst[0]
		self.congestion_high = thres_lst[1]

	def print_threshold(self):
		print("MID:", self.congestion_mid)
		print("HIGH:", self.congestion_high)


class Cell(object):
	def __init__(self, ix, iy, cell_opt):
		self.ix = ix
		self.iy = iy
		self.opt = cell_opt
		self.agent_lst = []
		pass

	def __repr__(self):
		return f"{len(self.agent_lst)/self.opt.capacity}"

	def get_cell_idx(self):
		return (self.ix, self.iy)

	def plot(self):
		return (f"Cell({self.ix}, {self.iy})")

	def insert_agent(self, agent):
		self.agent_lst.append(agent)
		agent.register_cell(self.ix, self.iy)

	def remove_agent(self, agent):
		self.agent_lst.remove(agent)

	def get_cell_status(self):
		agent_cnt = len(self.agent_lst)
		if self.opt.capacity < 0:
			return 3 # Unavailable
		else:
			ratio = agent_cnt / float(self.opt.capacity)
			if ratio < self.opt.congestion_mid:
				return 0 # Congestion: Low
			elif ratio > self.opt.congestion_high:
				return 2 # Congestion: High
			else:
				return 1 # Congestion: MID

	def get_agents(self):
		return self.agent_lst

	def get_active_agents(self):
		_status = self.get_cell_status()
		if _status > 2:
			return list()
		elif _status == 0:
			return self.agent_lst
		elif _status == 2:
			return [self.agent_lst[0]]
		else:
			return self.agent_lst[0:int(self.opt.capacity/2)]
