import os
import math
import argparse
import networkx as nx
import time

def load_network(file_path):
    G = nx.Graph()
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                G.add_edge(int(parts[0]), int(parts[1]))
    return G

def flexi_clique(G, tau):
    H = G.copy()  # Copy the graph G to H
    degrees = {v: G.degree(v) for v in H}

    def degree(v):
        return degrees[v]

    while degrees and min(degree(v) for v in H) < math.floor(len(H) ** tau):
        A = set(nx.articulation_points(H))
        T = set(H.nodes()) - A
        u = min(T, key=degree)
        for neighbor in list(H.neighbors(u)):  # Only consider neighbors still in H
            if neighbor in degrees:
                degrees[neighbor] -= 1
        H.remove_node(u)
        del degrees[u]

    return list(H.nodes())

def find_all_flexi_cliques(G, tau):
    remaining_nodes = set(G.nodes())
    cliques = []

    while remaining_nodes:
        subgraph = G.subgraph(remaining_nodes)
        clique = flexi_clique(subgraph, tau)
        if not clique:
            break
        cliques.append(clique)
        remaining_nodes -= set(clique)

    return cliques

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flexi-clique Algorithm")
    parser.add_argument("--file_path", help="Path to the network file")
    parser.add_argument("--tau", type=float, help="Tau value for flexi-clique")
    args = parser.parse_args()

    tau = args.tau
    file_path = args.file_path+"network.dat"
    G = load_network(file_path)

    start = time.time()
    cliques = find_all_flexi_cliques(G, tau)
    end = time.time()

    output_dir = os.path.dirname(args.file_path)
    output_filename = "flexi_cliques_enum.dat"
    output_path = os.path.join(output_dir, output_filename)

    with open(output_path, 'w') as output_file:
        output_file.write(f"tau = {tau}\n")
        output_file.write(f"Time taken = {end-start}\n")
        output_file.write(f"Number of cliques = {len(cliques)}\n")
        output_file.write(f"Cliques = {cliques}\n")
    print(f"Results written to {output_path}")