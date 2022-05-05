
class ControllerCapacityConstraint:
    
    def __init__(self, capacity, network):
        self.capacity = capacity
        self.network = network
        self.name = "controller_capacity_constraint"
    
    def check_if_satisfy(self, sdn):
        sat = True
        for controller in sdn.controllers:
            total_load = 0
            for i in range(sdn.switch_count):
                if sdn.placement[i][controller] == 1:
                    total_load += self.network.load[str(i)]
            if total_load > self.capacity:
                sat = False
                break
        return sat
        
    def get_value(self, sdn):
        return None    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            