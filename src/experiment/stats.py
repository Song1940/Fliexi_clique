import networkx as nx


def load_network(file_path):
    G = nx.Graph()
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                G.add_edge(int(parts[0]), int(parts[1]))
    return G



if __name__ == '__main__':

    # Load karate network
    G = load_network("network.dat")

    # Read the part file
    with open('output.txt', 'r') as file:
        lines = file.readlines()

    # Output results to a part-specific file
    with open('stats.txt', 'w', encoding='utf-8') as outfile:
       for line in lines:
           node_list = list(map(int, line.strip().split()))
           subgraph = nx.induced_subgraph(G, node_list)
           min_degree = min(dict(subgraph.degree()).values())
           outfile.write(f"{min_degree} {str(len(node_list))}\n")