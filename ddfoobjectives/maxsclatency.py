
class MaxSCLatencyObjective:
    
    def __init__(self, network, topo_map):
        self.max_latency = network.get_max_latency()
        self.topo_map = topo_map
        self.network = network
        self.name = "max_sc_latency_score"

    def evaluate_score(self, sdn):
        worst_observed_latency = 0
        for i in range(sdn.switch_count):
            for j in range(sdn.switch_count):
                if sdn.placement[i][j] == 1:
                    latency = self.network.get_latency(self.topo_map[i], self.topo_map[j])
                    if latency > worst_observed_latency:
                        worst_observed_latency = latency
                    break
                
        return round(worst_observed_latency, 3)