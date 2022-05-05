
class AvgSCLatencyObjective:
    
    def __init__(self, network, topo_map):
        self.network = network
        self.topo_map = topo_map
        self.name = "avg_sc_latency_score"

    def evaluate_score(self, sdn):
        latency_running_sum = 0
        for i in range(sdn.switch_count):
            for j in range(sdn.switch_count):
                if sdn.placement[i][j] == 1:
                    latency = self.network.get_latency(self.topo_map[i], self.topo_map[j])
                    latency_running_sum += latency
                    break
                
        return round(latency_running_sum/sdn.switch_count, 3)