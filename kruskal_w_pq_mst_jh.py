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
max_cost = 20
dense_adj_matrix = []
sparse_adj_matrix = []
varying_adj_matrix = []

dense_edges_weighted = []
sparse_edges_weighted = []
varying_edges_weighted = []

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
        #dense_adj_matrix[row -1][column -1] = rand_cost
        #dense_adj_matrix[column -1][row -1] = rand_cost
        dense_edges_weighted.append([row-1, column-1, rand_cost])

        
    for e in sparse_edges:
        row = e[0]
        column = e[1]
        rand_cost = random.randint(1, max_cost)
        #sparse_adj_matrix[row -1][column -1] = rand_cost
        #sparse_adj_matrix[column -1][row -1] = rand_cost
        sparse_edges_weighted.append([row-1, column-1, rand_cost])
    
    #for this case we set cost range between -max_cost and max_cost
    for e in varying_edges:
        row = e[0]
        column = e[1]
        rand_cost = random.randint(-max_cost, max_cost)
        #varying_adj_matrix[row -1][column -1] = rand_cost
        #varying_adj_matrix[column -1][row -1] = rand_cost
        varying_edges_weighted.append([row-1, column-1, rand_cost])
        
    
    print(f"\n\tDense Edges w Weights - len {len(dense_edges_weighted)}  = \n{dense_edges_weighted}")
    print(f"\n\tSparse Edges w Weights - len {len(sparse_edges_weighted)}  = \n{sparse_edges_weighted}")
    print(f"\n\tVarying Edges w Weights - len {len(varying_edges_weighted)}  = \n{varying_edges_weighted}")
    
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

def compress(par):
    for p in range(len(par)):
        if par[p] != p:
            par[p] = find_par(par[p], par)


#My original attmep at sorting the weights. This was wildly slow.
def sort_by_weight(edges_and_weight):
    n = len(edges_and_weight)
    if n <= 1:
        return
    for i in range(1, n):
        val = edges_and_weight[i]
        j = i-1
        while j >= 0 and val[2] < edges_and_weight[j][2]:
            edges_and_weight[j+1] = edges_and_weight[j]
            j = j-1
        edges_and_weight[j+1] = val
    return edges_and_weight
 
    
#insertionSort, Hybridsort, and MergeSort recycled from previous projects and modified for array of arrays
def insertionSort(arr, leftIndex, rightIndex):

    for i in range(leftIndex+1, rightIndex+1):
        for j in range(i, leftIndex,-1):
            k=arr[j]
            if arr[j][2]<arr[j-1][2]:
                arr[j]=arr[j-1]
                arr[j-1]=k
            else:
                break           

def hybridSort(arr, leftIndex, rightIndex, k):
    #Make sure length is at least 1
    if rightIndex - leftIndex <=0:
        return 0
    
    #Send arrays shorter than k to be insertion sorted
    if rightIndex - leftIndex +1 <= k:
        return insertionSort(arr, leftIndex, rightIndex)
    
    #Find Middle
    middleIndex = (rightIndex+leftIndex)//2
        
    # recursively call hybridsort until n length is reached
    hybridSort(arr, leftIndex, middleIndex, k)
    hybridSort(arr, middleIndex+1, rightIndex, k)
    merge(arr, leftIndex, middleIndex, rightIndex)
    return arr


def merge(arr, leftIndex, middleIndex, rightIndex):

	# initialize temp arrays
    LEFT = arr[leftIndex:middleIndex+1]
    RIGHT = arr[middleIndex+1:rightIndex+1]

    # Merge loop
    i = 0
    j = 0
    k = leftIndex

    while i < len(LEFT) and j < len(RIGHT):
        if LEFT[i][2] <= RIGHT[j][2]:
            arr[k] = LEFT[i]
            i = i+1
            k = k+1
        else:
            arr[k] = RIGHT[j]
            j += 1
            k += 1

    # Copy remaining LEFT, if any
    while i < len(LEFT):
        arr[k] = LEFT[i]
        i += 1
        k += 1

    #Copy remaining RIGHT, if any
    while j < len(RIGHT):
        arr[k] = RIGHT[j]
        j += 1
        k += 1
    
    if j < len(RIGHT):
        for r in range(len(RIGHT)-j, len(RIGHT)):
            arr[k] = RIGHT[j]
            j +=1
            k+=1


#main function. This version took a weighted edge list rathe than an adjacency matrix
def kruskal_mst(graph_name, dimension, weighted_edge_list):
    #initilize min_cost and connecting_edges to 0. Set up parent with each node as its own parent
    par = [0] * dimension
    print(f"\n\nKruskal's {graph_name} Graph Minimum Cost Spanning Tree for {dimension} nodes:\n") 
    min_cost = 0
    connecting_edges = 0
    kept_edges = []
    
    #hybridsort the weighted edgelist with a k value of 7 for a fairly optimal sort
    pq = hybridSort(weighted_edge_list, 0, len(weighted_edge_list)-1, 7)
    #print("pq")
    #print(pq)
    u = 0
    v = 0

    #Set parent pointers for each node to itself
    for i in range (dimension):
        par[i] = i
    
    #add edges to list or discard them until we have v-1 looking at only the 0 index
    while connecting_edges +1 < dimension:
        #if both nodes in the edge share a parent, discard without adding
        if find_par(pq[0][0], par) == find_par(pq[0][1], par):
            pq.pop(0)
        #othewise add edge, run union on their parents and compress before popping the entry off
        else:
            kept_edges.append(pq[0])
            u = pq[0][0]
            v = pq[0][1]
            par_u = find_par(u, par)
            par_v = find_par(v, par)
            compress(par)
            if union(par_u, par_v, par) != 0:
                print(f"{u} -> {v} at weight {pq[0][2]}")
                min_cost += pq[0][2]
            connecting_edges +=1
            pq.pop(0)
    print(f"\n\tKept Edges: {kept_edges} ")  
    print(f"\n\tMinimum cost: {graph_name} Graph = \n{min_cost}")  
    

"""
#Driver code for tests

dimension_choice = 6
gen_matrices(dimension_choice)

print("Both Edges and Weights before processing")
print(dense_edges_weighted)
print("Both Edges and Weights After processing")
sort_by_weight(dense_edges_weighted)
print(dense_edges_weighted)

t_1 = process_time()
kruskal_mst("Dense", dimension_choice, dense_edges_weighted)
t_2 = process_time()
elapsed = t_2-t_1
print(f"\nKruskal's Process Time for Dense Graph with {dimension_choice} nodes: {elapsed}")

t_1 = process_time()
kruskal_mst("Sparse", dimension_choice, sparse_edges_weighted)
t_2 = process_time()
elapsed = t_2-t_1
print(f"\nKruskal's Process Time for Sparse Graph with {dimension_choice} nodes: {elapsed}")

t_1 = process_time()
kruskal_mst( "Varying", dimension_choice, varying_edges_weighted)
t_2 = process_time()
elapsed = t_2-t_1
print(f"\nKruskal's Process Time for Varying Graph with {dimension_choice} nodes: {elapsed}")

"""
# Driver code for sequentially run time tests
dimension = 5
dimension_arr = [25, 50, 
                 100, 200
                 ]
results_dense = []
results_sparse = []
results_varying = []

dense_edges_weighted = []
sparse_edges_weighted = []
varying_edges_weighted = []

for i in dimension_arr:
    dense_adj_matrix = []
    sparse_adj_matrix = []
    varying_adj_matrix = []
    
    dense_edges_weighted = []
    sparse_edges_weighted = []
    varying_edges_weighted = []
    
    dimension_choice = i
    gen_matrices(dimension_choice)
    
    t_1 = process_time()
    kruskal_mst( "Dense", dimension_choice, dense_edges_weighted)
    t_2 = process_time()
    elapsed = t_2-t_1
    print(f"\nKruskal's Process Time for Dense Graph with {dimension_choice} nodes: {elapsed}")
    results_dense.append(elapsed)
    
    
    t_1 = process_time()
    kruskal_mst("Sparse", dimension_choice, sparse_edges_weighted)
    t_2 = process_time()
    elapsed = t_2-t_1
    print(f"\nKruskal's Process Time for Sparse Graph with {dimension_choice} nodes: {elapsed}")
    results_sparse.append(elapsed)
    
    t_1 = process_time()
    kruskal_mst("Varying", dimension_choice, varying_edges_weighted)
    t_2 = process_time()
    elapsed = t_2-t_1
    print(f"\nKruskal's Process Time for Varying Graph with {dimension_choice} nodes: {elapsed}")
    results_varying.append(elapsed)

plt.plot(dimension_arr, results_dense, '-ok', color='black')
plt.title('Kruskal w/ HybridSort PQ Performance: Dense')
plt.xlabel('Vertex Count')
plt.ylabel('Run Times')
#plt.xscale('log')
plt.grid(True)
plt.show()

plt.plot(dimension_arr, results_sparse,  '-ok', color='black')
plt.title('Kruskal w/ HybridSort PQ Performance: Sparse')
plt.xlabel('Vertex Count')
plt.ylabel('Run Times')
#plt.xscale('log')
plt.grid(True)
plt.show()

plt.plot(dimension_arr, results_varying,  '-ok', color='black')
plt.title('Kruskal w/ HybridSort PQ Performance: Varying')
plt.xlabel('Vertex Count')
plt.ylabel('Run Times')
#plt.xscale('log')
plt.grid(True)
plt.show()
