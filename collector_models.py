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

        self.insert_input_port("agent_in")

        self.prev_state = "IDLE"
        self.agents_to_process = []

        self.tot_agent_map = {}
        self.evac_agent_lst = []

    def __del__(self):
        print("AAAA")
        pass

    def add_agent(self, agent):
    	self.tot_agent_map[agent.get_id()] = agent

    def ext_trans(self,port, msg):
        if port == "agent_in":
            self._cur_state = "PROCESS"
            data = msg.retrieve()
            self.agents_to_process.append((data[0], data[1]))
            print("!!!!")

    def output(self):
        SystemSimulator().get_engine(self.engine_name).simulation_stop()
        return None

        
    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "IDLE"