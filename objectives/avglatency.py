
class AvgSCLatencyObjective:
    
    def __init__(self, network):
        self.network = network
        self.name = "avg_sc_latency_score"

    def evaluate_score(self, sdn):
        latency_running_sum = 0
        for i in range(sdn.switch_count):
            for j in range(sdn.switch_count):
                if sdn.placement[i][j] == 1:
                    latency = self.network.get_latency(i, j)
                    latency_running_sum += latency
                    break
                
        return round(latency_running_sum/self.network.node_count, 3)