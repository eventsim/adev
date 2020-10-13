import yaml

class ScenarioManager(object):
	def __init__(self, _path=None):
		if _path:
			self.load(_path)

	def load(self, _path):
		self.scenario_path = _path

	def save(self):
		with open(self.scenario_path, 'w') as f:
			yaml.dump(self.scenario, f)

	def get_example_scenario(self):
		self.scenario = {'sceVersion': 'sce/v1',\
						 'sceType': 'EvacSim',\
						 'scenario':{\
						 	'regions':[\
						 			{\
							 			'rid':0,\
							 			'regionInfo'  :{\
							 			'regionSize':[5, 5],\
							 			'entry_points':{0:[4, 2]},\
							 			'exit_points':{0:[0, 4]},}, \
							 			'modelName':'Region01',\
							 			'engineName':'sname',\
							 			'instance_time':0, \
							 			'destroy_time':30,\
						 			},\
						 		],\
						 	'agents':[\
						 				{'region_id':0, 'agent_id':0, "agent_pos":[0, 0], "agent_type":"Normal"},\
						 				{'region_id':0, 'agent_id':1, "agent_pos":[0, 0], "agent_type":"Normal"}
						 			],\
						 	},\
						 }
						 
		return yaml.dump(self.scenario)


if __name__ == "__main__":
	scenario = ScenarioManager().get_example_scenario()
	print(scenario)