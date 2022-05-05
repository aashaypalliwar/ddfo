
class MaxCCLatencyEvaluator:
    
    def __init__(self, network):
        self.network = network
        self.name = "max_cc_latency"        
            
    def get_value(self, sdn):
        worst_observed_latency = 0
        for i in sdn.controllers:
            for j in sdn.controllers:
                latency = self.network.get_latency(i, j)
                if latency > worst_observed_latency:
                    worst_observed_latency = latency
        
        return worst_observed_latency
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            