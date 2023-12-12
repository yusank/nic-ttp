import numpy as np
import sys
from collections import Counter
from scipy.spatial.distance import cdist

# Initialize variables to store the read data
problem_name = ""  # Store the name of the problem
knapsack_data_type = ""  # Store the data type of the knapsack problem
dimension = 0  # Store the dimension of the problem
num_items = 0  # Store the number of items
capacity = 0  # Store the capacity of the knapsack
min_speed = 0.0  # Store the minimum speed
max_speed = 0.0  # Store the maximum speed
renting_ratio = 0.0  # Store the renting ratio
edge_weight_type = ""  # Store the type of edge weight
node_coord_section = []  # Store the list of node coordinates
items_section = []  # Store the list of item information


# Choose file name


file_name = ""
try:
    file_name = sys.argv[1]
    if file_name == "" or file_name is None:
        raise SystemExit("must provide a dataset filename as input.")
except Exception as e:
    sys.exit(f"read args failed with error:{e}")

# file_name = input("Input the file name(e.g.: a280-n1395.txt):")

# Open the file
with open(file_name, "r") as file:
    # Read the file content line by line
    for line in file:
        # Remove the newline character at the end of the line
        line = line.strip()

        # Parse the file content line by line
        if line.startswith("PROBLEM NAME:"):
            problem_name = line.split(":")[1].strip()
        elif line.startswith("KNAPSACK DATA TYPE:"):
            knapsack_data_type = line.split(":")[1].strip()
        elif line.startswith("DIMENSION:"):
            dimension = int(line.split(":")[1].strip())
        elif line.startswith("NUMBER OF ITEMS:"):
            num_items = int(line.split(":")[1].strip())
        elif line.startswith("CAPACITY OF KNAPSACK:"):
            capacity = int(line.split(":")[1].strip())
        elif line.startswith("MIN SPEED:"):
            min_speed = float(line.split(":")[1].strip())
        elif line.startswith("MAX SPEED:"):
            max_speed = float(line.split(":")[1].strip())
        elif line.startswith("RENTING RATIO:"):
            renting_ratio = float(line.split(":")[1].strip())
        elif line.startswith("EDGE_WEIGHT_TYPE:"):
            edge_weight_type = line.split(":")[1].strip()
        elif line.startswith("NODE_COORD_SECTION"):
            # Start reading node coordinate data
            break
        elif line:  # If the line is not empty
            # Handle other possible information
            print("Other information:", line)

    # Continue reading node coordinate data
    for line in file:
        line = line.strip()
        if line.startswith("ITEMS SECTION"):
            # Start reading item information
            break
        elif line:  # If the line is not empty
            # Parse node coordinate data
            index, x, y = map(int, line.split())
            node_coord_section.append((index, x, y))

    # Continue reading item information
    for line in file:
        line = line.strip()
        if line:  # If the line is not empty
            # Parse item information
            index, profit, weight, assigned_node_number = map(int, line.split())
            items_section.append((index, profit, weight, assigned_node_number))

# Convert items_section into an array and group by "ASSIGNED NODE NUMBER"
items_array = []

# Use a dictionary to group rows with the same "ASSIGNED NODE NUMBER"
grouped_items = {}
for item in items_section:
    assigned_node_number = item[3]  # Index of "ASSIGNED NODE NUMBER" is 3

    # If the current ASSIGNED NODE NUMBER already exists in the dictionary, add to the group
    if assigned_node_number in grouped_items:
        grouped_items[assigned_node_number].append(item)
    # Otherwise, create a new group
    else:
        grouped_items[assigned_node_number] = [item]

# Add grouped data to the array
for group in grouped_items.values():
    items_array.append(group)


# Convert grouped data to an array and record the count of ASSIGNED NODE NUMBER
items_array = []
assigned_node_counts = Counter()

for group in grouped_items.values():
    items_array.append(group)

    assigned_node_numbers = [
        item[3] for item in group
    ]  # Get all ASSIGNED NODE NUMBER in the current group
    node_number_counts = Counter(
        assigned_node_numbers
    )  # Count the occurrences of ASSIGNED NODE NUMBER

    # Update the total counter with the count of ASSIGNED NODE NUMBER
    assigned_node_counts.update(node_number_counts)


node_coord_section = np.array(node_coord_section)


def create_distance_matrix(coords):
    return cdist(coords[:, 1:], coords[:, 1:], metric="euclidean")


D = create_distance_matrix(node_coord_section)
# print(node_coord_section)

"""
# Print the results
print("PROBLEM NAME:", problem_name)
print("KNAPSACK DATA TYPE:", knapsack_data_type)
print("DIMENSION:", dimension)
print("NUMBER OF ITEMS:", num_items)
print("CAPACITY OF KNAPSACK:", capacity)
print("MIN SPEED:", min_speed)
print("MAX SPEED:", max_speed)
print("RENTING RATIO:", renting_ratio)
print("EDGE_WEIGHT_TYPE:", edge_weight_type)
print("NODE_COORD_SECTION:", node_coord_section)
print("ITEMS SECTION:", items_array)
print(f"{node_number_counts")
print(D)
"""
# print("ITEMS SECTION:", items_array)
