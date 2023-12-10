import Import
import Packing
import ea

import matplotlib.pyplot as plt

def calc_fitness(location, information, route, packing_plan, max_weight):
    total_fitness = []
    max_velocity = 1.00
    min_velocity = 0.10
    item_num = len(information[0])  # item number of each city
    distance = 0.0
    current_velocity = 1.00
    
    for a in range(len(route)):
        for b in range(len(packing_plan)):
            current_weight = 0
            total_profit = 0
            total_time = 0
            

            for i in range(len(route[a]) - 1):
                distance = location[route[a][i] - 1][route[a][i + 1] - 1]

                for j in range(item_num):
                    if packing_plan[b][route[a][i] - 1][j] == 1:
                        
                        current_weight += information[route[a][i] - 2][j][2]
                        total_profit += information[route[a][i] - 2][j][1]
                        current_velocity = max_velocity - (max_velocity - min_velocity) * current_weight / max_weight
                        
                        

                total_time += distance / current_velocity

            distance = location[route[a][-1]][route[a][0]]

            for j in range(item_num):
                if packing_plan[b][route[a][-1] - 1][j] == 1:
                    current_weight += information[route[a][-1] - 1][j][2]
                    total_profit += information[route[a][-1] - 1][j][1]
                    current_velocity = max_velocity - (max_velocity - min_velocity) * current_weight / max_weight

                total_time += distance / current_velocity

            total_fitness.append([a, b, total_profit, total_time])
            

    return total_fitness



information = Import.items_array
    
information = [[list(t) for t in inner_list] for inner_list in information]


'''[
    # (INDEX, PROFIT, WEIGHT, ASSIGNED NODE NUMBER)
    [[1, 50, 1, 2], [4, 100, 2, 2]],  # city 2
    [[2, 50, 1, 3], [5, 100, 2, 3]],  # city 3
    [[3, 50, 1, 4], [6, 100, 2, 4]]   # city 4
]
'''
e = ea.EA(pop_size = 20, tour_size = 10, D=Import.create_distance_matrix(Import.node_coord_section))
pop_slice = e.run()

result_list = []
for data in pop_slice:
    index_of_1 = data.index(1)
    result = data[index_of_1:] + data[:index_of_1]
    result_list.append(result)

route = result_list
#print(len(route[0]))



''' [
[1, 3, 4, 2],   # route 1
[1, 4, 2, 3]    # route 2
]
'''

packing_plan = Packing.best_solution


'''[
# city 1, city 2, city 3, city 4
[[0, 0], [0, 1], [1, 1], [0, 0]],  # packingPlan 1
[[0, 0], [1, 0], [0, 1], [1, 0]]   # packingPlan 2
]
'''
location = Import.D

'''[
[0, 2, 3, 4],
[2, 0, 1, 3],
[3, 1, 0, 2],
[4, 3, 2, 0]
]
'''
max_weight = Import.capacity

total_fitness = calc_fitness(location, information,  route, packing_plan, max_weight)

for row in total_fitness:
    print("\t".join(map(str, row)))
    
total_profit = [row[2] for row in total_fitness]
total_time = [row[3] for row in total_fitness]

plt.scatter(total_time, total_profit, alpha=0.5, s=5)
plt.title('Total Profit vs Total Time')
plt.xlabel('Total Time')
plt.ylabel('Total Profit')
plt.show()


