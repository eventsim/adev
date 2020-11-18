import yaml

class ScenarioManager(object):
	def __init__(self, _path=None):
		self.scenario = None
		
		if _path:
			self.load(_path)

	def load(self, _path):
		self.scenario_path = _path
		with open(_path) as f:
			self.scenario = yaml.load(f.read(), Loader=yaml.CLoader)
			

	def save(self, _path):
		with open(_path, 'w') as f:
			if not self.scenario:
				self.get_example_scenario()

			yaml.dump(self.scenario, f)

	def get_regions(self):
		return self.scenario['scenario']['regions']

	def get_agents(self):
		return self.scenario['scenario']['agents']

	def get_config(self):
		return self.scenario['config']

	def get_building_exits(self):
		return self.scenario['scenario']['building']['exits']

	def get_example_scenario(self):
		self.scenario = {'sceVersion': 'sce/v1',\
						 'sceType': 'EvacSim',\
						 'scenario':{\
						 	'regions':[\
						 			{\
							 			'rid':0,\
							 			'regionSize':[10, 10],\
							 			'entries':[{'en_id':0, 'coord':[4, 4]}],\
							 			'exits' :[{'ex_id':0, 'coord':[0, 4]}], \
						 			},\
						 		],\
						 	'building':{\
						 	'exits':[{'rid':0, 'eid':0}],\
						 	},\
						 	'agents':[\
						 				 {'rid':0, 'aid':0, 'coord':[1, 9], 'type':'Normal', 'strategy':'OBJ_SMART'},              
										 {'rid':0, 'aid':1, 'coord':[7, 5], 'type':'Normal', 'strategy':'OBJ_SMART'},              
										 {'rid':0, 'aid':2, 'coord':[7, 7], 'type':'Normal', 'strategy':'OBJ_SMART'},              
										 {'rid':0, 'aid':3, 'coord':[3, 9], 'type':'Normal', 'strategy':'OBJ_SMART'},              
										 {'rid':0, 'aid':4, 'coord':[3, 2], 'type':'Normal', 'strategy':'OBJ_SMART'},              
										 {'rid':0, 'aid':5, 'coord':[7, 0], 'type':'Normal', 'strategy':'OBJ_SMART'},              
										 {'rid':0, 'aid':6, 'coord':[1, 8], 'type':'Normal', 'strategy':'OBJ_SMART'},              
										 {'rid':0, 'aid':7, 'coord':[2, 6], 'type':'Normal', 'strategy':'OBJ_SMART'},              
										 {'rid':0, 'aid':8, 'coord':[8, 3], 'type':'Normal', 'strategy':'OBJ_SMART'},              
										 {'rid':0, 'aid':9, 'coord':[1, 6], 'type':'Normal', 'strategy':'OBJ_SMART'},              
										{'rid':0, 'aid':10, 'coord':[3, 4], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':11, 'coord':[6, 2], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':12, 'coord':[1, 0], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':13, 'coord':[1, 4], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':14, 'coord':[6, 6], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':15, 'coord':[4, 4], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':16, 'coord':[7, 4], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':17, 'coord':[3, 5], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':18, 'coord':[8, 6], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':19, 'coord':[0, 1], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':20, 'coord':[2, 2], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':21, 'coord':[7, 2], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':22, 'coord':[5, 6], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':23, 'coord':[5, 4], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':24, 'coord':[3, 0], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':25, 'coord':[3, 6], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':26, 'coord':[6, 7], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':27, 'coord':[4, 8], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':28, 'coord':[0, 4], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':29, 'coord':[7, 3], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':30, 'coord':[0, 6], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':31, 'coord':[6, 1], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':32, 'coord':[9, 0], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':33, 'coord':[5, 8], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':34, 'coord':[6, 9], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':35, 'coord':[4, 2], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':36, 'coord':[7, 6], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':37, 'coord':[8, 9], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':38, 'coord':[8, 1], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':39, 'coord':[1, 1], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':40, 'coord':[5, 2], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':41, 'coord':[4, 1], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':42, 'coord':[2, 1], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':43, 'coord':[1, 3], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':44, 'coord':[3, 3], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':45, 'coord':[0, 8], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':46, 'coord':[6, 8], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':47, 'coord':[9, 1], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':48, 'coord':[4, 7], 'type':'Normal', 'strategy':'OBJ_SMART'},             
										{'rid':0, 'aid':49, 'coord':[2, 7], 'type':'Normal', 'strategy':'OBJ_SMART'} 
						 			],\
						 	},\
						 'config':{\
						 		'simName':'evacuation',\
						 		'engineName':'sname',\
					 			'instance_time':0, \
					 			'destroy_time':30,\
					 			'rand_seed':1,
						 	}
						 }
						 
		return yaml.dump(self.scenario)


if __name__ == "__main__":
	scenario = ScenarioManager().get_example_scenario()
	print(scenario)