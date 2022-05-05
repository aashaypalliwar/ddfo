
class ControllerCount:
    
    def __init__(self):
        self.name = "controller_count_score"
        
    def evaluate_score(self, sdn):
        return sdn.controller_count
