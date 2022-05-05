
class MaxSCLatencyEvaluator:
    
    def __init__(self, network):
        self.network = network
        self.name = "max_sc_latency"
        
    def get_value(self, sdn):
        worst_observed_latency = 0
        for i in range(sdn.switch_count):
            for j in range(sdn.switch_count):
                if sdn.placement[i][j] == 1:
                    latency = self.network.get_latency(i, j)
                    if latency > worst_observed_latency:
                        worst_observed_latency = latency
                    break
        
        return worst_observed_latency
            
            
            
            
            
            
            
            
            
            
            
            
            
