from evsim.system_simulator import SystemSimulator
from evsim.behavior_model_executor import BehaviorModelExecutor
from evsim.structural_model import StructuralModel
from evsim.system_message import SysMessage
from evsim.definition import *
from config import *

import functools
import operator
import re

class RegionModel(StructuralModel):
    def __init__(self, instance_time, destruct_time, name, engine_name, region):
        StructuralModel.__init__(self, name)
        
        self.region = region

        rm = RegionManagerModel(instance_time, destruct_time, name + ":manager", engine_name, region)
        rrm = RegionRouterModel(instance_time, destruct_time, name + ":router", engine_name, region)
        
        self.insert_model(rm)
        self.insert_model(rrm)

        self.configure_exceptional_cells(rm, rrm)
        
        if NETWORK_UI_FLAG:
            rp = RegionReport(instance_time, destruct_time, name + ":report", engine_name, region)
            self.insert_model(rp)
            self.configure_network_ui(rrm, rp)
    
    def configure_exceptional_cells(self, rm, rrm):
        # input: entry points
        entry_points = self.region.get_entry_points()
        for k in entry_points.keys():
            self.insert_input_port(f"agent_in[{k}]")
            rm.insert_input_port(f"agent_in[{k}]")
            self.insert_external_input_coupling(f"agent_in[{k}]", rm, f"agent_in[{k}]")

            self.insert_input_port("agent_in")
            rm.insert_input_port("agent_in")
            self.insert_external_input_coupling("agent_in", rm, "agent_in")

        self.insert_internal_coupling(rm, "agent_out", rrm, "active_agents")

        # output: entry points
        exit_points = self.region.get_exit_points()
        for k in exit_points.keys():
            self.insert_output_port(f"agent_out[{k}]")
            rrm.insert_output_port(f"agent_out[{k}]")
            self.insert_external_output_coupling(rrm, f"agent_out[{k}]", f"agent_out[{k}]")

            self.insert_output_port("agent_out")
            rrm.insert_output_port("agent_out")
            self.insert_external_output_coupling(rrm, "agent_out", "agent_out")

    def configure_network_ui(self, rrm, rp):
        entry_points = self.region.get_entry_points()
        for k in entry_points.keys():
            rp.insert_input_port(f"agent_in[{k}]")
            self.insert_external_input_coupling(f"agent_in[{k}]", rp, f"agent_in[{k}]")

            rp.insert_input_port("agent_in")
            self.insert_external_input_coupling("agent_in", rp, "agent_in")

        exit_points = self.region.get_exit_points()
        for k in exit_points.keys():
            rp.insert_input_port(f"agent_out[{k}]")
            self.insert_internal_coupling(rrm, f"agent_out[{k}]", rp, f"agent_out[{k}]")
            rp.insert_input_port("agent_out")
            self.insert_internal_coupling(rrm, "agent_out", rp, "agent_out")

'''
class RegionManagerModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, region):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        # Open CSV
        self.init_state("SCHEDULE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("PROCESS", 0)
        self.insert_state("SCHEDULE", MODEL_TIME_REQ)

        self.region = region

        self.prev_state = "IDLE"
        self.agents_to_process = []


    def ext_trans(self,port, msg):
        #print(port)
        if port == "agent_in":
            #self.prev_state = self._cur_state
            self._cur_state = "PROCESS"
            data = msg.retrieve()
            self.agents_to_process.append((data[0], data[1]))
        else:
            port_num = int(re.search(r"\[(\w+)\]", port).group(1))
            self._cur_state = "PROCESS"
            data = msg.retrieve()
            #print(self, data)
            #for agent in data:
            self.agents_to_process.append((self.region.get_entry_points()[port_num], data[0]))


    def output(self):
        if self.agents_to_process:
            for agent_info in self.agents_to_process:
                #print(agent_info)
                self.region.add_agent(agent_info[0], agent_info[1])

            self.agents_to_process.clear()

        agents_lst = self.region.schedule()
        msg = SysMessage(self.get_name(), "agent_out")
        #print(str(datetime.datetime.now()) + " Human Object:")
        msg.extend(agents_lst)

        
        return msg
        
    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "SCHEDULE"
        elif self._cur_state == "SCHEDULE":
            self._cur_state = "SCHEDULE"

class RegionRouterModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, region):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        # Open CSV
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("PROCESS", 0)

        self.insert_input_port("active_agents")
        #self.insert_output_port("agent_out")

        self.region = region

        self.agents_to_process = []

    def ext_trans(self,port, msg):
        if port == "active_agents":
            self._cur_state = "PROCESS"
            data = msg.retrieve()
            self.agents_to_process.extend(data)            

    def output(self):
        if self.agents_to_process:
            message_to_handle = []
            for agent in self.agents_to_process:
                # TODO call agent's perceive function
                perception = []
                ix, iy = agent.get_cell_idx()

                if ix > 0 and ix < self.region.get_shape()[1]-1 and \
                   iy > 0 and iy < self.region.get_shape()[0]-1 :                   
                    perception = functools.reduce(operator.iconcat, self.region.get_matrix()[iy-1:iy+2, ix-1:ix+2].tolist(), [])
                elif ix == 0 and iy > 0 and iy < self.region.get_shape()[0]-1 : 
                    perception = functools.reduce(operator.iconcat, self.region.get_matrix()[iy-1:iy+2, ix:ix+2].tolist(), [])
                elif iy == 0 and ix > 0 and ix < self.region.get_shape()[1]-1 : 
                    perception = functools.reduce(operator.iconcat, self.region.get_matrix()[iy:3, ix-1:ix+1].tolist(), [])
                elif iy == 0 and ix == 0 : 
                    perception = functools.reduce(operator.iconcat, self.region.get_matrix()[iy:iy+2, ix:ix+2].tolist(), [])
                elif ix == self.region.get_shape()[1]-1 and iy > 0 and iy < self.region.get_shape()[0]-1 : 
                    perception = functools.reduce(operator.iconcat, self.region.get_matrix()[iy-1:iy+1, ix-1:ix+1].tolist(), [])
                elif iy == self.region.get_shape()[0]-1 and ix > 0 and ix < self.region.get_shape()[1]-1 : 
                    perception = functools.reduce(operator.iconcat, self.region.get_matrix()[iy-1:iy+1, ix-1:ix+1].tolist(), [])
                elif iy == self.region.get_shape()[0]-1 and ix == self.region.get_shape()[1]-1 : 
                    perception = functools.reduce(operator.iconcat, self.region.get_matrix()[iy-1:iy+1, ix-1:ix+1].tolist(), [])

                nx, ny = agent.move(perception)
                if not(nx == 0 and ny == 0): 
                    self.region.remove_agent((ix, iy), agent)
                    # check exit points
                    if self.region.reached_to_exit(agent):
                        # send to output port
                        #print(self.region.get_exit_port(agent.get_cell_idx()))
                        msg = SysMessage(self.get_name(), self.region.find_exit_port(agent.get_cell_idx()))
                        #print(str(datetime.datetime.now()) + " Human Object:")
                        msg.insert(agent)
                        message_to_handle.append(msg)
                        pass
                    else:
                        self.region.update_agent((ix + nx, iy + ny), agent)

            self.agents_to_process.clear()
            return message_to_handle
        else:
            return None
        
    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "IDLE"
'''

class RegionManagerModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, region):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        # Open CSV
        self.init_state("SCHEDULE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("PROCESS", 0)
        self.insert_state("SCHEDULE", MODEL_TIME_REQ)

        self.region = region

        self.prev_state = "IDLE"
        self.agents_to_process = []


    def ext_trans(self,port, msg):
        #print(port)
        if port == "agent_in":
            #self.prev_state = self._cur_state
            self._cur_state = "PROCESS"
            data = msg.retrieve()
            self.agents_to_process.append((data[0], data[1]))
        else:
            port_num = int(re.search(r"\[(\w+)\]", port).group(1))
            self._cur_state = "PROCESS"
            data = msg.retrieve()
            #print(self, data)
            #for agent in data:
            self.agents_to_process.append((self.region.get_entry_points()[port_num], data[0]))


    def output(self):
        if self.agents_to_process:
            for agent_info in self.agents_to_process:
                #print(agent_info)
                self.region.add_agent(agent_info[0], agent_info[1])

            self.agents_to_process.clear()

        agents_lst = self.region.pre_execution()
        if agents_lst:
            msg = SysMessage(self.get_name(), "agent_out")
            #print(str(datetime.datetime.now()) + " Human Object:")
            msg.extend(agents_lst)

            return msg
        else:
            return None
        
    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "SCHEDULE"
        elif self._cur_state == "SCHEDULE":
            self._cur_state = "SCHEDULE"

class RegionRouterModel(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, region):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        # Open CSV
        self.init_state("IDLE")
        self.insert_state("IDLE", Infinite)
        self.insert_state("PROCESS", 0)

        self.insert_input_port("active_agents")
        #self.insert_output_port("agent_out")

        self.region = region

        self.agents_to_process = []

    def ext_trans(self,port, msg):
        if port == "active_agents":
            self._cur_state = "PROCESS"
            data = msg.retrieve()
            self.agents_to_process.extend(data)            

    def output(self):
        if self.agents_to_process:
            message_to_handle = []
            self.region.execution()

            exits = self.region.post_execution()

            if exits:
                for agent in exits:
                    msg = SysMessage(self.get_name(), self.region.find_exit_port(agent.get_cell_idx()))
                    #print(str(datetime.datetime.now()) + " Human Object:")
                    msg.insert(agent)
                    message_to_handle.append(msg)

            self.agents_to_process.clear()
            return message_to_handle
        else:
            return None
        
    def int_trans(self):
        if self._cur_state == "PROCESS":
            self._cur_state = "IDLE"

if NETWORK_UI_FLAG:
    from evsim.network_manager import NetworkManager
    class RegionReport(BehaviorModelExecutor):
        def __init__(self, instance_time, destruct_time, name, engine_name, region):
            BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

            # Open CSV
            self.init_state("REPORT")
            self.insert_state("REPORT", NETWORK_UPDATE_FREQ)

            self.region = region
            self.agents_to_process = []

            self.engine = SystemSimulator().get_engine(engine_name)

        def ext_trans(self, port, msg):
            if port[0:8] == "agent_in":
                self._cur_state = "REPORT"
                port_num = int(re.search(r"\[(\w+)\]", port).group(1))
 
                data = msg.retrieve()
                #print(self, data)
                #for agent in data:
                self.agents_to_process.append(("i", self.region.get_entry_points()[port_num], data[0]))
            elif port[0:9] == "agent_out":
                self._cur_state = "REPORT"
                port_num = int(re.search(r"\[(\w+)\]", port).group(1))
 
                data = msg.retrieve()
                self.agents_to_process.append(("o", self.region.get_exit_points()[port_num], data[0]))


        def output(self):
            if self.agents_to_process:
                for info in self.agents_to_process:
                    if REPORT_FLAG:
                        msg_contents = self.generate_report_contents(info[0], info[1], info[2], True)               
                        print(msg_contents)
                    
                    msg_contents = self.generate_report_contents(info[0], info[1], info[2], False) 
                    net_manager = NetworkManager()
                    net_manager.udp_send_string(NETWORK_HOST_ADDR, NETWORK_HOST_PORT, bytes(msg_contents))
                    #net_manager.tcp_send_string(msg_contents)
                
                self.agents_to_process.clear()
    
            return None
            
        def int_trans(self):
            if self._cur_state == "REPORT":
                self._cur_state = "REPORT"

        def generate_report_contents(self, _type, _coord, agent_info, verbose_mode = True):
            _str = ""
            if verbose_mode:
                _str = f"eventual|sim_time:{self.engine.get_global_time()}|region_id:{self.region.get_region_id()}|event_type:{_type}|coord:{_coord}|aid:{agent_info}"
            else:
                _str = bytearray()
                _str.append(ord('e'))
                _str.extend(struct.pack("d", self.engine.get_global_time()))
                _str.append(self.region.get_region_id())
                _str.append(ord(_type))
                _str.append(_coord[0])
                _str.append(_coord[1])
                _str.extend(agent_info.packing())
            return _str


if REPORT_FLAG:
    import numpy as np
    import struct
    from evsim.system_simulator import SystemSimulator
    class RegionsReportModel(BehaviorModelExecutor):
        def __init__(self, instance_time, destruct_time, name, engine_name, regions):
            BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

            # Open CSV
            self.init_state("REPORT")
            self.insert_state("REPORT", REPORT_FREQ)

            self.regions = regions
            self.engine = SystemSimulator().get_engine(engine_name)

        def ext_trans(self,port, msg):
            pass

        def output(self):
            for _id, region in self.regions.items():
                if REPORT_TO_CONSOLE:
                    _content = self.generate_report_contents(_id, region.get_matrix(), region.region_agents, True)
                    print(_content)
                    #print(region.get_matrix())
                if NETWORK_UI_FLAG:
                    _content = self.generate_report_contents(_id, region.get_matrix(), region.region_agents, False)
                    net_manager = NetworkManager()
                    net_manager.udp_send_string(NETWORK_HOST_ADDR, NETWORK_HOST_PORT, bytes(_content))

            return None
            
        def int_trans(self):
            if self._cur_state == "REPORT":
                self._cur_state = "REPORT"

        def generate_report_contents(self, _id, _region, agents, verbose_mode = True):
            contents = bytearray()
            if verbose_mode:
                str_lst = [agent.get_id() for agent in agents]
                contents = f"periodic|sim_time:{self.engine.get_global_time()}|region_id:{_id}|region:{_region.flatten()}|left:{str_lst}"
            else:
                contents.append(ord('p'))
                contents.extend(struct.pack("d", self.engine.get_global_time()))
                contents.append(_id)
                contents.append(_region.shape[1])
                contents.append(_region.shape[0])
                for cell in _region.flatten():
                    contents.append(len(cell.agent_lst))
            return contents
            