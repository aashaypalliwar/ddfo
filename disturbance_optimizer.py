from sdn import SDN
import math
import copy
import random
import matplotlib.pyplot as plt

class NSGA2_DisturbanceOptimizer:
    
    def __init__(self, params):
        self.objectives = params["objectives"]
        self.constraints = params["constraints"]
        self.evaluators = params["evaluators"]
        self.population_size = params["population_size"]
        self.mutation_fraction = params["mutation_fraction"]
        self.network = params["original_network"]
        self.controllers_available = params["controllers_available"]
        self.generations = params["generations"]
        self.capacity = params["single_controller_capacity"]
        self.ds_count = params["disturbed_switches_count"]
        self.mapped_pcl = params["mapped_permisible_controller_locations"]
        self.topo_map = params["topo_map"]
        self.load_map = params["load_map"]
        self.out = params["out"]
        
    def run(self):

        sdns = set()
        print("Generating initial population")
        
        controller_count = self.controllers_available
        switch_count = self.ds_count
        mapped_pcl = self.mapped_pcl
        capacity = self.capacity
        ses = self.objectives
        topo_map = self.topo_map
        load_map = self.load_map
        
        saturation_counter_1 = 0
        old_size = 0
        while len(sdns) < self.population_size:
            sdn = SDN.get_capacitated_random_sdn_subgraph_placement(controller_count, switch_count, capacity, topo_map, load_map, mapped_pcl, ses)
            sat = True
            for constraint in self.constraints:
                sat = sat and constraint.check_if_satisfy(sdn)
            
            if sat:
                sdns.add(sdn)
                print(len(sdns), end=" ")
            
                if not len(sdns) > old_size:   
                    saturation_counter_1 += 1
                else:
                    saturation_counter_1 = 0
                    old_size = len(sdns)

            if saturation_counter_1 > 1000:
                break
        
        print()
        if len(sdns) < 4:
            print("NOT ENOUGH SDNs")
            return []
        print("Initial population generated")
        self.fast_nds(sdns)
        self.calculate_crowding_distance(sdns)    
        
        old_front = set([sdn for sdn in sdns if sdn.rank == 1])
        saturation_counter = 0        
        counter = 0
        while counter != self.generations:
            print("Generation:", counter, "Population:", len(sdns))
            parents = self.select_parents(sdns)
            next_generation = self.cross(parents)
            self.mutate_generation(next_generation)        
            
            next_gen_list = list(next_generation)
            for constraint in self.constraints:            
                next_gen_list = [sdn for sdn in next_gen_list if constraint.check_if_satisfy(sdn)]
            
            sdns.update(set(next_gen_list))
            
            self.fast_nds(sdns)
            self.calculate_crowding_distance(sdns)
            
            sdn_list = list(sdns)
            sdn_list = sorted(sdn_list, key = lambda sdn: (sdn.rank, -1 * sdn.crowding_distance))
            
            sdns = set(sdn_list[:self.population_size])
            self.plot(sdns, counter)
            counter += 1
            
            front_1 = set([sdn for sdn in sdns if sdn.rank == 1])
            new_better_placements = len(front_1 - old_front)
            print("Found", new_better_placements, "new better placements")
            
            if new_better_placements == 0:
                saturation_counter += 1
            else:
                saturation_counter = 0
                
            old_front = front_1
            
            if saturation_counter == 5:
                break
        
        print("Front of length", len(old_front), "found")
        
        for sdn in old_front:
            info = {}
            for eval in self.evaluators:
                info[eval.name] = eval.get_value(sdn)
            print(info)
        
        return old_front
    
    def plot(self, population, counter):
        x = [sdn.score["controller_count_score"] for sdn in population]# if sdn.rank == 1]
        y = [sdn.score["avg_sc_latency_score"] for sdn in population]# if sdn.rank == 1]
        plt.scatter(x, y)
        plt.xlim(0, self.controllers_available + 1)
        plt.xlabel('Number of controllers')
        
        plt.ylim(0, self.network.get_max_latency())
        plt.ylabel('Avg SC latency')
        figure = plt.gcf()
        figure.set_size_inches(8, 6)
        plt.savefig('ddfo_runs/' + self.out + "/" + str(counter) + '.png',  dpi = 100)
        plt.clf()
    
    def mutate_generation(self, generation):
        mutant_count = (int)(self.mutation_fraction * len(generation))
        mutants = random.sample(generation, mutant_count)
        for sdn in mutants:
            self.mutate(sdn)
    
    def mutate(self, sdn):
        controllers = sdn.controllers
        mutation_location = controllers[random.randint(0, len(controllers)-1)]

        if len(controllers) == len(self.mapped_pcl):
            return sdn
        
        new_controller_location = random.sample(self.mapped_pcl, 1)[0]
                
        while new_controller_location in controllers:
            new_controller_location = random.sample(self.mapped_pcl, 1)[0]
    
        for i in range(sdn.switch_count):
            sdn.placement[i][new_controller_location] = sdn.placement[i][mutation_location]
            sdn.placement[i][mutation_location] = 0
            
        sdn.update_placement()
        
        return sdn
    
    def cross(self, parents):
        children = set()
        children_count = self.population_size
        
        old_size = 0
        sat_count = 0
        while len(children) < children_count:
            to_be_crossed = random.sample(parents, 2)
            o1, o2 = self.crossover(to_be_crossed[0], to_be_crossed[1])
            children.add(o1)
            children.add(o2)
            
            if old_size == len(children):
                sat_count += 1
            else:
                sat_count = 0
                old_size = len(children)
                
            if sat_count > children_count:
                break
            
        return children
            
    def crossover(self, p1, p2):
        o1 = copy.deepcopy(p1.placement)
        o2 = copy.deepcopy(p2.placement)
        
        pivot = random.randint(0, p1.switch_count-1)
        
        for i in range(pivot, p1.switch_count):
            o1[i], o2[i] = o2[i], o1[i]
        
        offspring_placement_1 = SDN.get_random_sdn_placement(1, 1, p1.switch_count, self.objectives)
        offspring_placement_2 = SDN.get_random_sdn_placement(1, 1, p2.switch_count, self.objectives)
        
        offspring_placement_1.placement = o1
        offspring_placement_1.update_placement()
        offspring_placement_2.placement = o2
        offspring_placement_2.update_placement()
        
        return offspring_placement_1, offspring_placement_2
        
    
    def fast_nds(self, population):
        
        front = []
        front_number = 1
        
        for p in population:
            p.dom_list = []
            p.dom_count = 0
            for q in population:
                
                if p == q:
                    continue
                
                if p.dominates(q):
                    p.dom_list.append(q)
                elif q.dominates(p):
                    p.dom_count += 1
            
            if p.dom_count == 0:
                front.append(p)
                p.rank = front_number
                
        while len(front) != 0:
            next_front= []
            for p in front:
                for q in p.dom_list:
                    q.dom_count -= 1
                    if q.dom_count == 0:
                        q.rank = front_number + 1
                        next_front.append(q)
            front_number += 1
            front = [p for p in next_front]
            
    def calculate_crowding_distance(self, population):
        temp = [p for p in population]
        front_number = 1
        while len(temp) != 0:
            front = [p for p in temp if p.rank == front_number]
            self.calculate_crowding_distance_for_front(front)
            temp = list(filter(lambda p: p.rank != front_number, temp))
            front_number += 1
        
    def calculate_crowding_distance_for_front(self, front):
        for p in front:
            p.crowding_distance = 0
                
        for obj in self.objectives:
            front.sort(key=lambda p: p.score[obj.name])
            min_obj_val = min(front, key=lambda x: x.score[obj.name]).score[obj.name]
            max_obj_val = max(front, key=lambda x: x.score[obj.name]).score[obj.name]
            obj_range = max_obj_val - min_obj_val
            
            front[0].crowding_distance = math.inf
            front[-1].crowding_distance = math.inf
            
            for i in range(1,len(front)-1):
                if obj_range != 0:
                    front[i].crowding_distance += (front[i+1].score[obj.name] - front[i-1].score[obj.name]) / obj_range
                else:
                    front[i].crowding_distance += math.inf
        
    def select_parents(self, population):
        selection_count = self.population_size / 2
        
        selected_parents = set()
        old_size = 0
        sat_count = 0
        while len(selected_parents) < selection_count:
            sample = random.sample(population, 2)
            
            if sample[0].rank < sample[1].rank:
                selected_parents.add(sample[0])
            elif sample[0].rank > sample[1].rank:
                selected_parents.add(sample[1])
            elif sample[0].crowding_distance > sample[1].crowding_distance:
                selected_parents.add(sample[0])
            else:
                selected_parents.add(sample[1])
                
            if old_size == len(selected_parents):
                sat_count += 1
            else:
                sat_count = 0
                old_size = len(selected_parents)
                
            if sat_count > selection_count:
                break
            
        return selected_parents
 