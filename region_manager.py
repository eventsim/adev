
from adev.region import Region, UniqueRegion
from adev.region_models import RegionModel
from adev.building_model import BuildingModel
from adev.cell import CellOpt

from config import *

class RegionManager(object):
	def __init__(self):
		self.regions = {}
		self.connection_info = []
		pass

	def add_region_to_building(self, region_id, region_size, default_cell_opt):
		self.regions[region_id] = Region(region_id, region_size[0], region_size[1], CellOpt(default_cell_opt))
		pass

	def add_agent_to_region(self, region_id, coord, agent):
		self.regions[region_id].add_agent(coord, agent)

	def get_region(self, region_id):
		return self.regions[region_id]

	def add_entry_point_to_region(self, region_id, point_id, coord):
		return self.regions[region_id].add_entry_points(point_id, coord)

	def add_exit_point_to_region(self, region_id, point_id, coord):
		return self.regions[region_id].add_exit_points(point_id, coord)

	def connect_region(self, from_id, exit_id, to_id, entry_id):
		self.connection_info.append((from_id, exit_id, to_id, entry_id))

	def get_building(self, instance_time, destruction_time, model_name, engine_name):
		building = BuildingModel(instance_time, destruction_time, model_name, engine_name)

		# Added RegionModel
		region_models = {}
		for _id, region in self.regions.items():
			region_models[_id] = RegionModel(instance_time, destruction_time, f"Region[{_id:03}]", engine_name, region)
			building.add_region_model(region_models[_id])

		# Connect Region
		for c in self.connection_info:
			building.connect_regions(region_models[c[0]], \
									c[1], \
									region_models[c[2]],\
									c[3])
		if REPORT_FLAG:
			from adev.region_models import RegionsReportModel
			report = RegionsReportModel(instance_time, destruction_time, model_name, engine_name, self.regions)
			building.insert_model(report)

		return building

class UniRegionManager(RegionManager):
	def __init__(self):
		RegionManager.__init__(self)
		pass

	def add_region_to_building(self, region_id, region_size):
		self.regions[region_id] = UniqueRegion(region_id, region_size[0], region_size[1])
		pass

	def add_agent_to_region(self, region_id, coord, agent):
		self.regions[region_id].add_agent(coord, agent)

	def get_region(self, region_id):
		return self.regions[region_id]

	def add_entry_point_to_region(self, region_id, point_id, coord):
		return self.regions[region_id].add_entry_points(point_id, coord)

	def add_exit_point_to_region(self, region_id, point_id, coord):
		return self.regions[region_id].add_exit_points(point_id, coord)

	def connect_region(self, from_id, exit_id, to_id, entry_id):
		self.connection_info.append((from_id, exit_id, to_id, entry_id))

	def get_building(self, instance_time, destruction_time, model_name, engine_name):
		building = BuildingModel(instance_time, destruction_time, model_name, engine_name)

		# Added RegionModel
		region_models = {}
		for _id, region in self.regions.items():
			region_models[_id] = RegionModel(instance_time, destruction_time, f"Region[{_id:03}]", engine_name, region)
			building.add_region_model(region_models[_id])

		# Connect Region
		for c in self.connection_info:
			building.connect_regions(region_models[c[0]], \
									c[1], \
									region_models[c[2]],\
									c[3])
		if REPORT_FLAG:
			from adev.region_models import RegionsReportModel
			report = RegionsReportModel(instance_time, destruction_time, model_name, engine_name, self.regions)
			building.insert_model(report)

		return building
