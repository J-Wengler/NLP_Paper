# 1. Create node class 
# 2. Retrofit the old code for DB code to use the node class 
# 3. Function to find eulerian path in a DB graph
# 4. Takes a eulerian path and turns it into a genome

class Graph:
    




def get_start(adjacency):
    return adjacency.split("->")[0]


def get_ends(adjacency):
    return adjacency.split("->")[1].split(",")


if __name__ == '__main__':
    input_file = open('input.txt')
    adjacencies = input_file.readlines()

    # Remove whitespace
    for i in range(len(adjacencies)):
        adjacencies[i] = ''.join(adjacencies[i].split())

    # Create and populate adjacency list
    # Key = "AGG"
    # Value = ["GGA", "GGT"]
    adjacency_list = {}
    for adjacency in adjacencies:
        start_node = get_start(adjacency)
        end_nodes = get_ends(adjacency)
        adjacency_list[start_node] = end_nodes

    edge_count = 0
    for connection_list in adjacency_list.values():
        edge_count += len(connection_list)

    # Take adjaceny list and create a list of node classes
    # graph class 

    out_file = open("output.txt", "w+")
    out_file.write("write me")

    out_file.close()
    input_file.close()