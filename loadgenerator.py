import random
import json

gml_folder = "/home/aashay/cupboard/ddfo/topologies/"

topo_name = "Latnet"
node_count = 69

min_load = 20000
max_load = 100000

load = {}
for i in range(node_count):
    load[i] = ((random.randint(min_load, max_load)) // 1000 ) * 1000

with open(gml_folder + topo_name + ".json", "w+") as file:
    json.dump(load, file)

print(load)