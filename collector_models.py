from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.structural_model import StructuralModel
from evsim.system_message import SysMessage
from evsim.definition import *
from config import *

class CollectorModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        # Open CSV
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("PROCESS", 0)

        self.prev_state = "IDLE"
        self.agents_to_process = []


    def ext_trans(self,port, msg):
        if port == "agent_in":
            self._cur_state = "PROCESS"
            data = msg.retrieve()
            self.agents_to_process.append((data[0], data[1]))

    def output(self):
        
        return None

        
    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "IDLE"