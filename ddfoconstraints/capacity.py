
class ControllerCapacityConstraint:
    
    def __init__(self, capacity, load_map):
        self.capacity = capacity
        self.load_map = load_map
        self.name = "controller_capacity_constraint"
    
    def check_if_satisfy(self, sdn):
        sat = True
        for controller in sdn.controllers:
            total_load = 0
            for i in range(sdn.switch_count):
                if sdn.placement[i][controller] == 1:
                    total_load += self.load_map[i]
            if total_load > self.capacity:
                sat = False
                break
        return sat
    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            