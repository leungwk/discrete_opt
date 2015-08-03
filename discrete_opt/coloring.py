#!/usr/bin/python
# -*- coding: utf-8 -*-

import networkx as nx
import sys

def read_input(fin_path):
    dgraph = nx.DiGraph()
    with open(fin_path, 'r') as fin:
        line = fin.readline().split(' ') # header
        cnt_node, cnt_edge = int(line[0]), int(line[1])
        for line in fin:
            line = line.strip().split(' ')
            src, dest = int(line[0]), int(line[1])
            dgraph.add_edge(src, dest)
    return dgraph


def read_colours(fin_path):
    colours = {}
    with open(fin_path, 'r') as fin:
        line = fin.readline() # header
        line = fin.readline()
        for idx_node, colour in enumerate(line.strip().split(' ')): # idx-0
            colours[idx_node] = colour
    return colours


def colouring_satisfied(graph, colours):
    for node in graph.nodes():
        node_colour = colours[node]
        for nei in graph.neighbors(node):
            if node_colour == colours[nei]:
                return False
    return True



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--mode', help='what to do', default='sat')
    parser.add_argument('--graph', help='list of edges (w/ header)')
    parser.add_argument('--soln', help='chromatic number and colour of nodes')
    args = parser.parse_args()

    if args.mode == 'sat':
        graph = read_input(args.graph)
        colours = read_colours(args.soln)
        print(1 if colouring_satisfied(graph, colours) else 0)
    else:
        raise ValueError('Invalid mode specified: {}'.format(args.mode))
