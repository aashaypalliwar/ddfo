
class MaxControllersConstraint:
    
    def __init__(self, available_controllers):
        self.available_controllers = available_controllers
        self.name = "max_controllers_constraint"
    
    def check_if_satisfy(self, sdn):
        return sdn.controller_count <= self.available_controllers
            
    def get_value(self, sdn):
        return sdn.controller_count        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            