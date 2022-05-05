
class MaxCCLatencyConstraint:
    
    def __init__(self, network, fraction):
        self.network = network
        self.threshold = fraction * network.get_max_latency()
        self.name = "max_cc_latency_constraint"

    
    def check_if_satisfy(self, sdn):
        worst_observed_latency = 0
        for i in sdn.controllers:
            for j in sdn.controllers:
                latency = self.network.get_latency(i, j)
                if latency > worst_observed_latency:
                    worst_observed_latency = latency
        
        return worst_observed_latency <= self.threshold
            
            
    def get_value(self, sdn):
        worst_observed_latency = 0
        for i in sdn.controllers:
            for j in sdn.controllers:
                latency = self.network.get_latency(i, j)
                if latency > worst_observed_latency:
                    worst_observed_latency = latency
        
        return worst_observed_latency
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            