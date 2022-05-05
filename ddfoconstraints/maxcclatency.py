
class MaxCCLatencyConstraint:
    
    def __init__(self, network, fraction, undisturbed_controllers, topo_map):
        self.network = network
        self.threshold = fraction * network.get_max_latency()
        self.undisturbed_controllers = undisturbed_controllers
        self.topo_map = topo_map
        self.name = "max_cc_latency_constraint"

        self.worst_observed_latency = 0
        for i in undisturbed_controllers:
            for j in undisturbed_controllers:
                latency = self.network.get_latency(i, j)
                if latency > self.worst_observed_latency:
                    self.worst_observed_latency = latency
    
    def check_if_satisfy(self, sdn):
        wlatency = self.worst_observed_latency
        new_controllers = [self.topo_map[c] for c in sdn.controllers]
        all_controllers = self.undisturbed_controllers + new_controllers
        for i in new_controllers:
            for j in all_controllers:
                latency = self.network.get_latency(i, j)
                if latency > wlatency:
                    wlatency = latency                    
        
        return wlatency <= self.threshold
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            