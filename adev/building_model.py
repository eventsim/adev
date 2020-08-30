from adev.region_models import RegionModel
from evsim.structural_model import StructuralModel

class BuildingModel(StructuralModel):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        StructuralModel.__init__(self, name)
    
    def add_region_model(self, region_model):
    	self.insert_model(region_model)

    def connect_regions(self, _from, exit_id, _to, entry_id):
    	self.insert_internal_coupling(_from, f"agent_out[{exit_id}]", _to, f"agent_in[{entry_id}]")
