import networkx as nx
import math
import heapq
import time
import argparse
import os
from collections import defaultdict


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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tau-clique_scalability_test')
    parser.add_argument('--file_path', type=str, help='Input file path')
    # parser.add_argument('--tau', type=float, help='Tau value')
    args = parser.parse_args()

    # file_path args.file_path/network.dat
    num = args.file_path.replace("syn_N_", "").replace("/","")
    file_path = args.file_path + "network.dat"
    G = load_network(file_path)
    # tau = int(args.tau)

    ts = [0.2, 0.4, 0.6, 0.8]
    size = []
    result = []

    for i in ts:
        start = time.time()
        H = flexi_clique(G, i)
        end = time.time()
        result.append(end-start)
        size.append(len(H))

    output_file = os.path.join(args.file_path,f'syn_{num}_time_k.txt')
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for i in range(len(ts)):
            outfile.write("tau: " + str(ts[i]) + " execution time: " + str(result[i]) + " size : " + str(size[i]) + "\n")

    print(f'Result is written to {output_file}')