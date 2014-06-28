#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import sys
import pandas as pd

def feasible(taken, capacity, weights):
    return np.dot(taken, weights) <= capacity


def branch_bound(n_items, capacity, values, weights):
    """assume capacity >= 0"""
    def _estimate(taken):
        ## calculate optimistic estimate
        df_vw = pd.DataFrame([values,weights,taken]).T
        df_vw.columns = ['v','w','t']
        df_vw['r'] = (1.*df_vw['v']/df_vw['w'])
        df_vw.sort(['t','r'], ascending=[False,False], inplace=True)

        rem_k = capacity
        val_est = 0
        ## only consider unconsidered, and use remaining capacity
        for _, v, w, t, r in df_vw.itertuples():
            if t == 0: # already accounted for
                continue

            if t == 1 or rem_k -w >= 0:
                ## take whole
                val_est += 1*v
                rem_k -= w
            else:
                ## take partial
                val_est += 1.*rem_k/w *v
        return val_est

    lvl = 0 # top of branch level
    val_lvl, w_lvl = values[lvl], weights[lvl]
    ## item no., taken array, remaining capacity, total value
    unvisited = [(lvl, [0], capacity, 0)]
    if val_lvl <= capacity: # only enqueue node if capacity will not be exceeded
        unvisited.append( (lvl, [1], capacity -w_lvl, val_lvl) )
    ## start with taken (left) so to prune faster
 
    best_taken = []
    best_val = -float('inf')
    while True:
        if not unvisited:
            break

        lvl, taken, rem_cap, tot_val = unvisited.pop()
        tmp_taken = taken +[-1]*(n_items -(lvl +1)) # -1 indicates to be considered. 0 means not taken
        val_est = _estimate(tmp_taken)
        if best_val > val_est:
            ## prune by best estimate as it cannot be exceeded down this path
            continue

        ## keep
        if tot_val > best_val:
            best_val = tot_val
            best_taken = [(x if x != -1 else 0) for x in tmp_taken]

        ## enqueue new, if any
        new_lvl = lvl+1
        if new_lvl < n_items: # still more nodes to expand
            val_lvl, w_lvl = values[new_lvl], weights[new_lvl]
            unvisited.append( (new_lvl, taken+[0], rem_cap, tot_val) )
            if w_lvl <= rem_cap:
                unvisited.append( (new_lvl, taken+[1], rem_cap -w_lvl, tot_val +val_lvl) )

    return best_taken





def dyn_prog(n_items, capacity, values, weights):
    tab = np.zeros( (capacity +1, n_items +1) ) # incl. 0 item, or 0 capacity case
    tab[:,0] = 0
    for j in xrange(1,n_items +1): # item idx
        for k in xrange(0,capacity +1):
            w_j = weights[j -1] # idx-1
            if w_j <= k:
                v_j = values[j -1] # idx-1
                tab[k,j] = max( tab[k, j-1], v_j +tab[k -w_j, j-1] )
            else: # do not take the item
                tab[k,j] = tab[k, j-1]

    ## backtrack
    taken = []
    k,j = tab.shape[0] -1, tab.shape[1] -1
    while True:
        if j == 0:
            break
        if tab[k, j] == tab[k, j-1]:
            taken.append(0)
        else:
            w_j = weights[j -1] # idx-1
            k -= w_j
            taken.append(1)
        j -= 1
    return taken[::-1]


def greedy(n_items, capacity, values, weights):
    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = []

    for i in range(0, n_items):
        if weight + weights[i] <= capacity:
            taken.append(1)
            value += values[i]
            weight += weights[i]
        else:
            taken.append(0)
    return taken


def read_output(fin_path):
    with open(fin_path, 'r') as fin:
        line_1 = fin.readline().split(' ')
        v_star, opt = int(line_1[0]), int(line_1[1])
        taken = np.array(map(int,fin.readline().split(' ')))
        return {
            'v_star': v_star,
            'opt': opt,
            'taken': taken,
            }


def read_input(fin_path):
    with open(fin_path, 'r') as fin:
        input_data = ''.join(fin.readlines())
        lines = input_data.split('\n')

        firstLine = lines[0].split()
        items, capacity = int(firstLine[0]), int(firstLine[1])

        values = []
        weights = []

        for i in range(1, items+1):
            line = lines[i]
            parts = line.split()

            values.append(int(parts[0]))
            weights.append(int(parts[1]))

        n_items = len(values)
        return {
            'n_items': n_items,
            'values': values,
            'weights': weights,
            'capacity': capacity,
            }


def _format_output(v_star, taken):
    out_str = str(v_star) + ' ' + str(0) + '\n'
    out_str += ' '.join(map(str, taken))
    return out_str


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('mode', help='what to do', const=1, nargs='?', default='run')
    parser.add_argument('func', help='input file', default='dyn_prog')
    parser.add_argument('--input', help='input file')
    parser.add_argument('--output', help='input file')
    args = parser.parse_args()

    if args.mode == 'run':
        input_vals = read_input(args.input)
        taken = locals()[args.func](**input_vals)
        v_star = np.dot(input_vals['values'], taken)
        sys.stdout.write(_format_output(v_star, taken))
    elif args.mode == 'check':
        input_vals = read_input(args.input)
        output_vals = read_output(args.output)
        res = feasible(output_vals['taken'], input_vals['capacity'], input_vals['weights'])
        sys.stdout.write( ('1' if res else '0') +'\n')
