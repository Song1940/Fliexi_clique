import networkx as nx
import math
import time
import argparse
import os



def load_network(file_path):
    G = nx.Graph()
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                G.add_edge(int(parts[0]), int(parts[1]))
    return G

def largestCC(G, sub):
    largest_cc = max(nx.connected_components(G.subgraph(sub)), key=len)
    return G.subgraph(largest_cc).copy()


def flexi_clique(G, tau):
    c = nx.core_number(G)
    k_star = max(c.values())
    k = 2

    while k <= k_star:
        kc = [v for v in c if c[v] >= k]
        T = largestCC(G, kc)
        if math.floor(len(T)**tau) <= k:
            break
        k += 1

    kc = [v for v in c if c[v] >= k-1]
    H = largestCC(G, kc)

    degrees = {v: H.degree(v) for v in H}

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


def flexi_clique_no_k_core(G, tau):
    H = G.copy()  # Copy the graph G to H
    degrees = {v: G.degree(v) for v in H}

    def degree(v):
        return degrees[v]

    while min(degree(v) for v in H) < math.floor(len(H) ** tau):
        A = set(nx.articulation_points(H))
        T = set(H.nodes()) - A
        u = min(T, key=degree)
        for neighbor in list(H.neighbors(u)):  # Only consider neighbors still in H
            if neighbor in degrees:
                degrees[neighbor] -= 1
        H.remove_node(u)
        del degrees[u]

    return list(H.nodes())




if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Peeling Algorithm for tau-clique")
    parser.add_argument("--file_path", help="Path to the network file")
    parser.add_argument("--tau", type=float, help="Value of tau")
    args = parser.parse_args()

    # Load graph
    file_path = args.file_path+"network.dat"

    G = load_network(file_path)
    G.remove_edges_from(nx.selfloop_edges(G))
    tau = args.tau

    # Run algorithm
    start = time.time()
    result = flexi_clique(G, tau)
    end = time.time()

    subgraph = G.subgraph(result)
    minimum_degree = min(subgraph.degree(v) for v in subgraph)

    time = end - start
    # Write results to file
    output_dir = os.path.dirname(args.file_path)
    output_filename = f"{tau}_flexi_peeling.dat"
    output_path = os.path.join(output_dir, output_filename)

    with open(output_path, 'w') as output_file:
        # output_file.write(f"{tau}-clique, running time :  {time}\n")
        output_file.write(f"{tau}-clique: nodes: {result}\n")
        output_file.write(f"{tau}-clique: # of nodes: {len(result)}\n")
        output_file.write(f"{tau}-clique: degree threshold: {minimum_degree}\n")

    print(f"Results written to {output_path}")