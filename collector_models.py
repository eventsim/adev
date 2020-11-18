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
        self.early_exit = False

    def __del__(self):
    	if not self.early_exit:
	        print(f"Simulation End Time:{SystemSimulator().get_engine(self.engine_name).get_global_time()}" )
	        print(f"Total Agents:{len(self.tot_agent_map)+ len(self.evac_agent_lst)}, Evacuated:{len(self.evac_agent_lst)}, Survival Ratio:{float(len(self.evac_agent_lst)/(len(self.tot_agent_map)+ len(self.evac_agent_lst)))}")

    def check_sim_end(self, aid):
        if aid in self.tot_agent_map.keys():
            self.evac_agent_lst.append(self.tot_agent_map[aid])
            del self.tot_agent_map[aid]

        if not bool(self.tot_agent_map):
            return True
        else:
            return False

    def add_agent(self, agent):
    	self.tot_agent_map[agent.get_id()] = agent

    def ext_trans(self,port, msg):
        if port == "agent_in":
            self._cur_state = "PROCESS"
            data = msg.retrieve()
            self.agents_to_process.append(data[0])
            

    def output(self):
        for agent in self.agents_to_process:
            if self.check_sim_end(agent.get_id()):
                self.early_exit = True
                print(f"Simulation End Time:{SystemSimulator().get_engine(self.engine_name).get_global_time()}" )
                print(f"Total Agents:{len(self.tot_agent_map)+ len(self.evac_agent_lst)}, Evacuated:{len(self.evac_agent_lst)}, Survival Ratio:{float(len(self.evac_agent_lst)/(len(self.tot_agent_map)+ len(self.evac_agent_lst)))}")
                SystemSimulator().get_engine(self.engine_name).simulation_stop()

        self.agents_to_process.clear()
        return None

        
    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "IDLE"