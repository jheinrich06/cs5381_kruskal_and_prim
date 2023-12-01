#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 09:04:18 2023

@author: Jason Heinrich
"""

import random
from time import process_time
import matplotlib.pyplot as plt

#set inf to 999 to make unconnected nodes infeasible for calculation. with max 20 this is exclusionary
inf = 999


#create empty adjacency matrices of chosen dimension size
#dimension = 20
max_cost = 10000
dense_adj_matrix = []
sparse_adj_matrix = []
varying_adj_matrix = []

def gen_matrices(dimension):
    #populate them with zeroes
    #tried populating all 3 at once but they were getting linked by the
    #compiler so I ran the loop 3 separate times to keep them isolated
    for d in range(0, dimension):
        row = []
        for j in range(dimension):
            row.append(0)
        dense_adj_matrix.append(row)
        #sparse_adj_matrix.append(row)
        #varying_adj_matrix.append(row)
    
    for d in range(0, dimension):
        row = []
        for j in range(dimension):
            row.append(0)
        sparse_adj_matrix.append(row)
    
    for d in range(0, dimension):
        row = []
        for j in range(dimension):
            row.append(0)
        varying_adj_matrix.append(row)
    
    #target densities for dense, sparse, varying matrices vs current
    density_targets = [0.75, 0.25, 0.5] 
    current_density = [0, 0, 0]
    
    dense_edges = []
    sparse_edges = []
    varying_edges = []
    
    #generate random edges checking uniqueness and self connection before adding
    #used all_zeroes check to ensure each vertex had at least 1 connection
    completeness_check_arr = [0] * dimension
    completeness_check = 0
    while density_targets[0] > current_density[0] or completeness_check == 0 or len(dense_edges) +1 < dimension:
        rand_edge = (random.randint(1, dimension), random.randint(1, dimension))
        rand_edge_inverted = (rand_edge[1], rand_edge[0])
        reject = False
        if rand_edge[0] == rand_edge[1]:
            reject = True
        for e in dense_edges:
            if e == rand_edge or e == rand_edge_inverted:
                reject = True
        if reject != True:
            dense_edges.append(rand_edge)
        #if acceptable push to array
        current_density[0] = 2*len(dense_edges)/(dimension * (dimension-1))
        # refresh checks
        completeness_check_arr[rand_edge[0]-1] = rand_edge[0]
        completeness_check_arr[rand_edge[1]-1] = rand_edge[1]
        completeness_check = 1
        for i in completeness_check_arr:
            completeness_check = completeness_check * i
            #print(completeness_check_arr)
    
    #reset tests for second set
    completeness_check_arr = [0] * dimension
    completeness_check = 0
    while density_targets[1] > current_density[1] or completeness_check == 0 or len(sparse_edges) +1 < dimension:
        rand_edge = (random.randint(1, dimension), random.randint(1, dimension))
        rand_edge_inverted = (rand_edge[1], rand_edge[0])
        reject = False
        if rand_edge[0] == rand_edge[1]:
            reject = True
        for e in sparse_edges:
            if e == rand_edge or e == rand_edge_inverted:
                reject = True
        if reject != True:
            sparse_edges.append(rand_edge)
        #if acceptable push to array
        current_density[1] = 2*len(sparse_edges)/(dimension * (dimension-1))
        # refresh checks
        completeness_check_arr[rand_edge[0]-1] = rand_edge[0]
        completeness_check_arr[rand_edge[1]-1] = rand_edge[1]
        completeness_check = 1
        for i in completeness_check_arr:
            completeness_check = completeness_check * i
            #print(completeness_check_arr)
    
    #reset tests for third set
    completeness_check_arr = [0] * dimension
    completeness_check = 0
    while density_targets[2] > current_density[2] or completeness_check == 0 or len(varying_edges) +1 < dimension:
        rand_edge = (random.randint(1, dimension), random.randint(1, dimension))
        rand_edge_inverted = (rand_edge[1], rand_edge[0])
        reject = False
        if rand_edge[0] == rand_edge[1]:
            reject = True
        for e in varying_edges:
            if e == rand_edge or e == rand_edge_inverted:
                reject = True
        if reject != True:
            varying_edges.append(rand_edge)
        #if acceptable push to array
        current_density[2] = 2*len(varying_edges)/(dimension * (dimension-1))
        # refresh checks
        completeness_check_arr[rand_edge[0]-1] = rand_edge[0]
        completeness_check_arr[rand_edge[1]-1] = rand_edge[1]
        completeness_check = 1
        for i in completeness_check_arr:
            completeness_check = completeness_check * i
            #print(completeness_check_arr)
    
             
    print(f"\n\tDense Edges = \n{dense_edges}")
    print(f"\n\tSparse Edges = \n{sparse_edges}")
    print(f"\n\tVarying Edges = \n{varying_edges}")
    print(f"\n\tCurrent Density = \n{current_density}")
    
    # convert those edges into an adjacency matrix with random but consistent costs
    for e in dense_edges:
        row = e[0]
        column = e[1]
        rand_cost = random.randint(1, max_cost)
        dense_adj_matrix[row -1][column -1] = rand_cost
        dense_adj_matrix[column -1][row -1] = rand_cost
        
    for e in sparse_edges:
        row = e[0]
        column = e[1]
        rand_cost = random.randint(1, max_cost)
        sparse_adj_matrix[row -1][column -1] = rand_cost
        sparse_adj_matrix[column -1][row -1] = rand_cost
    
    #for this case we set cost range between -max_cost and max_cost
    for e in varying_edges:
        row = e[0]
        column = e[1]
        rand_cost = random.randint(-max_cost, max_cost)
        varying_adj_matrix[row -1][column -1] = rand_cost
        varying_adj_matrix[column -1][row -1] = rand_cost
    
    print(f"\n\tDense Adjacency Matrix = \n{dense_adj_matrix}")
    print(f"\n\tSparse Adjacency Matrix = \n{sparse_adj_matrix}")
    print(f"\n\tVarying Adjacency Matrix = \n{varying_adj_matrix}")
    
    #pre-process the zero nodes setting them to our infinity number
    #not counting this in time interval since the choice of zero vs inf was for aesthetics/simplicity
    for i in range(dimension):
        for j in range(dimension):
            if dense_adj_matrix[i][j] == 0:
                dense_adj_matrix[i][j] = inf
            if sparse_adj_matrix[i][j] == 0:
                sparse_adj_matrix[i][j] = inf
            if varying_adj_matrix[i][j] == 0:
                varying_adj_matrix[i][j] = inf
    
    #print(f"\n\tDense Adjacency Matrix = \n{dense_adj_matrix}")
    #print(f"\n\tSparse Adjacency Matrix = \n{sparse_adj_matrix}")
    #print(f"\n\tVarying Adjacency Matrix = \n{varying_adj_matrix}")


#initialize empty parent node array


#simple implementations of union and find functions of unionFind Data Structure
def find_par(i, par):
    if par[i] != i:
        i = par[i]
    return i
def union(i, j, par):
    if i != j:
        par[j] = par[i]
        compress(par)
        return 1
    return 0

#compress feature that flattens the parent pointer so comparisons don't need to be recursive
def compress(par):
    for p in range(len(par)):
        if par[p] != p:
            par[p] = find_par(par[p], par)




def kruskal_mst(adj_matrix, graph_name, dimension):
    par = [0] * dimension
    print(f"\n\nKruskal's {graph_name} Graph Minimum Cost Spanning Tree for {dimension} nodes:\n") 
    tmp_matrix = adj_matrix
    #initilize min_cost and connecting_edges to 0. Set up parent with each node as its own parent
    min_cost = 0
    connecting_edges = 0
    for i in range (dimension):
        par[i] = i
    
    #loop to add edges
    while connecting_edges +1 < dimension:
        #set min val to inf for each loop to reset it from previous best
        min_val = inf
        #loop through each array in the array searching for minimum values that don't share a parent
        for i in range(dimension):
            for j in range(dimension):
                if tmp_matrix[i][j] < min_val and find_par(i, par) != find_par(j, par):
                    min_val = tmp_matrix[i][j]
                    #save location for best values for operation after inner loops exit
                    a = i
                    u = i
                    b = j
                    v = j
                    
        #pre-compress, run find then union on u and v
        compress(par)
        u = find_par(u, par)
        v = find_par(v, par)
        if union(u, v, par) != 0:
            print(f"{a} -> {b} at weight {min_val}")
            min_cost += min_val
        #weed out edges we've used from future consideration
        tmp_matrix[a][b] = 999
        tmp_matrix[b][a] = 999
        connecting_edges += 1
        #print(par)
    print(f"\n\tMinimum cost: {graph_name} Graph = \n{min_cost}")
    #print(f"\n\tParent: {graph_name} Graph = \n{par}")

"""
#Driver code for tests
dimension_choice = 6
gen_matrices(dimension_choice)
t_1 = process_time()
kruskal_mst(dense_adj_matrix, "Dense", dimension_choice)
t_2 = process_time()
elapsed = t_2-t_1
print(f"\nKruskal's Process Time for Dense Graph with {dimension_choice} nodes: {elapsed}")

t_1 = process_time()
kruskal_mst(sparse_adj_matrix, "Sparse", dimension_choice)
t_2 = process_time()
elapsed = t_2-t_1
print(f"\nKruskal's Process Time for Sparse Graph with {dimension_choice} nodes: {elapsed}")

t_1 = process_time()
kruskal_mst(varying_adj_matrix, "Varying", dimension_choice)
t_2 = process_time()
elapsed = t_2-t_1
print(f"\nKruskal's Process Time for Varying Graph with {dimension_choice} nodes: {elapsed}")
"""

# Driver code for sequentially run time tests
dimension = 5
dimension_arr = [25, 50, 100, 200]
results_dense = []
results_sparse = []
results_varying = []

for i in dimension_arr:
    dense_adj_matrix = []
    sparse_adj_matrix = []
    varying_adj_matrix = []
    dimension_choice = i
    gen_matrices(dimension_choice)
    
    t_1 = process_time()
    kruskal_mst(dense_adj_matrix, "Dense", dimension_choice)
    t_2 = process_time()
    elapsed = t_2-t_1
    print(f"\nKruskal's Process Time for Dense Graph with {dimension_choice} nodes: {elapsed}")
    results_dense.append(elapsed)
    
    
    t_1 = process_time()
    kruskal_mst(sparse_adj_matrix, "Sparse", dimension_choice)
    t_2 = process_time()
    elapsed = t_2-t_1
    print(f"\nKruskal's Process Time for Sparse Graph with {dimension_choice} nodes: {elapsed}")
    results_sparse.append(elapsed)
    
    t_1 = process_time()
    kruskal_mst(varying_adj_matrix, "Varying", dimension_choice)
    t_2 = process_time()
    elapsed = t_2-t_1
    print(f"\nKruskal's Process Time for Varying Graph with {dimension_choice} nodes: {elapsed}")
    results_varying.append(elapsed)

plt.plot(dimension_arr, results_dense, '-ok', color='black')
plt.title('Kruskal Performance: Dense')
plt.xlabel('Vertex Count')
plt.ylabel('Run Times')
#plt.xscale('log')
plt.grid(True)
plt.show()

plt.plot(dimension_arr, results_sparse,  '-ok', color='black')
plt.title('Kruskal Performance: Sparse')
plt.xlabel('Vertex Count')
plt.ylabel('Run Times')
#plt.xscale('log')
plt.grid(True)
plt.show()

plt.plot(dimension_arr, results_varying,  '-ok', color='black')
plt.title('Kruskal Performance: Varying')
plt.xlabel('Vertex Count')
plt.ylabel('Run Times')
#plt.xscale('log')
plt.grid(True)
plt.show()