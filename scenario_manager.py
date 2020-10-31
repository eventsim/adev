import yaml

class ScenarioManager(object):
	def __init__(self, _path=None):
		if _path:
			self.load(_path)

	def load(self, _path):
		self.scenario_path = _path
		with open(_path) as f:
			self.scenario = yaml.load(f.read(), Loader=yaml.CLoader)
			

	def save(self):
		with open(self.scenario_path, 'w') as f:
			yaml.dump(self.scenario, f)

	def get_regions(self):
		return self.scenario['scenario']['regions']

	def get_agents(self):
		return self.scenario['scenario']['agents']

	def get_config(self):
		return self.scenario['config']

	def get_example_scenario(self):
		self.scenario = {'sceVersion': 'sce/v1',\
						 'sceType': 'EvacSim',\
						 'scenario':{\
						 	'regions':[\
						 			{\
							 			'rid':0,\
							 			'regionSize':[5, 5],\
							 			'entries':[{'en_id':0, 'coord':[4, 4]}],\
							 			'exits' :[{'ex_id':0, 'coord':[0, 4]}], \
						 			},\
						 		],\
						 	'agents':[\
						 				{'rid':0, 'aid':0, "coord":[0, 0], "type":"Normal", "strategy":"OBJ_SMART"},\
						 				{'rid':0, 'aid':1, "coord":[0, 0], "type":"Normal", "strategy":"OBJ_GREED"}
						 			],\
						 	},\
						 'config':{\
						 		'simName':'evacuation',\
						 		'engineName':'sname',\
					 			'instance_time':0, \
					 			'destroy_time':30,\
						 	}
						 }
						 
		return yaml.dump(self.scenario)


if __name__ == "__main__":
	scenario = ScenarioManager().get_example_scenario()
	print(scenario)