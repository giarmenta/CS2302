# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 14:06:40 2019

@author: Gerardo Armenta
Instructor: Dr. Olac Fuentes
TA: Anindita Nath, Maliheh Zargaran, Erik Macik, Eduardo Lara
Purpose:To use the previous lab 6 and create a maze that asks the user to select the number of walls they want removed
        and then create an adjacency list of each pathcreated from each wall removal. Then implement breadth first search,
        depth first search and depth first search using recursion. Finally create a path from start, cell 0, to goal, top
        left corner.
"""

import matplotlib.pyplot as plt
import numpy as np
import time
import random
import math
import queue

def DisjointSetForest(size):
    # Creates disjoint set forest all set to -1 (the root)
    return np.zeros(size,dtype=np.int)-1

def find(S,i):
    # Returns root of tree that i belongs to
    if S[i]<0:
        return i
    return find(S,S[i])

def find_c(S,i): #Find with path compression 
    if S[i]<0: 
        return i
    r = find_c(S,S[i]) 
    S[i] = r 
    return r
    
def union(S,i,j):
    # Joins i's tree and j's tree, if they are different
    ri = find(S,i) 
    rj = find(S,j)
    if ri!=rj:
        S[rj] = ri
        return True
    return False

def union_c(S,i,j):
    # Joins i's tree and j's tree, if they are different
    # Uses path compression
    ri = find_c(S,i) 
    rj = find_c(S,j)
    if ri!=rj:
        S[rj] = ri
        return True
    return False

def union_by_size(S,i,j):
    # if i is a root, S[i] = number of elements in tree (set)
    # Makes root of smaller tree point to root of larger tree 
    # Uses path compression
    ri = find_c(S,i) 
    rj = find_c(S,j)
    if ri!=rj:
        if S[ri]>S[rj]:
            S[rj] += S[ri]
            S[ri] = rj
        else:
            S[ri] += S[rj]
            S[rj] = ri

def NumSets(S):
    # Counts the number of sets of a disjoint set forest
    count =0
    for i in S:
        if i < 0:
            count += 1
    return count

def draw_maze(walls,maze_rows,maze_cols,cell_nums=False):
    # Draws a maze
    fig, ax = plt.subplots()
    for w in walls:
        if w[1]-w[0] ==1: #vertical wall
            x0 = (w[1]%maze_cols)
            x1 = x0
            y0 = (w[1]//maze_cols)
            y1 = y0+1
        else:#horizontal wall
            x0 = (w[0]%maze_cols)
            x1 = x0+1
            y0 = (w[1]//maze_cols)
            y1 = y0  
        ax.plot([x0,x1],[y0,y1],linewidth=1,color='k')
    sx = maze_cols
    sy = maze_rows
    ax.plot([0,0,sx,sx,0],[0,sy,sy,0,0],linewidth=2,color='k')
    if cell_nums:
        for r in range(maze_rows):
            for c in range(maze_cols):
                cell = c + r*maze_cols   
                ax.text((c+.5),(r+.5), str(cell), size=10,
                        ha="center", va="center")
    ax.axis('off') 
    ax.set_aspect(1.0)
    return ax

def wall_list(maze_rows, maze_cols):
    # Creates a list with all the walls in the maze
    w =[]
    for r in range(maze_rows):
        for c in range(maze_cols):
            cell = c + r*maze_cols
            if c!=maze_cols-1:
                w.append([cell,cell+1])
            if r!=maze_rows-1:
                w.append([cell,cell+maze_cols])
    return w

# Creates the adjacency list for the graph
def get_adj_list(p, A):
    for i in range(len(p)):
        temp0 = p[i][0]
        temp1 = p[i][1]
        A[temp0].append(temp1)
        A[temp1].append(temp0)
    return A

# Creates the path from start to goal
# Will check for a path recursively from goal to start by checking if path exists
def path(plot, previous, vertex, x, y) :
    # Since only element at previous[0] should equal -1 if a path exists
    # if a -1 is found before hand, it means no path exists.
    if previous[vertex] != -1:
        # path is ploted in red from removed wall 
        if vertex == (previous[vertex] + maze_cols) :
            x1 = x
            y1 = y - 1
            path(plot, previous, previous[vertex], x1, y1)
            plot.plot([x1, x], [y1, y], linewidth = 2, color = 'r')
        if  vertex == (previous[vertex] - maze_cols) :
            x1 = x
            y1 = y + 1
            path(plot, previous, previous[vertex], x1, y1)
            plot.plot([x1, x], [y1, y], linewidth = 2, color = 'r')       
        if vertex == (previous[vertex] + 1) :
            x1 = x - 1
            y1 = y
            path(plot, previous, previous[vertex], x1, y1)
            plot.plot([x1, x], [y1, y], linewidth = 2, color = 'r')         
        if vertex == (previous[vertex] - 1) :
            x1 = x + 1
            y1 = y
            path(plot, previous, previous[vertex], x1, y1)
            plot.plot([x1, x],[y1, y], linewidth = 2, color = 'r')

def draw_graph(G):
    fig, ax = plt.subplots()
    n = len(G)
    r = 30
    coords =[]
    for i in range(n):
        theta = 2*math.pi*i/n+.001 # Add small constant to avoid drawing horizontal lines, which matplotlib doesn't do very well
        coords.append([-r*np.cos(theta),r*np.sin(theta)])
    for i in range(n):
        for dest in G[i]:
            ax.plot([coords[i][0],coords[dest][0]],[coords[i][1],coords[dest][1]],
                     linewidth=1,color='k')
    for i in range(n):
        ax.text(coords[i][0],coords[i][1],str(i), size=10,ha="center", va="center",
         bbox=dict(facecolor='w',boxstyle="circle"))
    ax.set_aspect(1.0)
    ax.axis('off')
    
# Traverses adjacency list using depth-first search
def depth_first_search(G):
    start = time.time()*1000
    visited = [False] * len(G)  # creates a list of boolean False of length G
    prev = [-1] * len(G)  # creates a list of -1 of length G
    S = []  # A list used as a stack that starts empty
    S.append(0)  #  Starting point is vertex 0 so it is appended fist
    visited[0] = True  # Visisted list is changed to True for 0, the starting point
    # Traversal starts from 0
    while S:  # While the stack is not empty
        v = S.pop()  # v is for the vertext which is popped from S
        for t in G[v]:
            if not visited[t]:  # if visited[t] is False
                visited[t] = True
                prev[t] = v
                S.append(t)
    stop = time.time()*1000
    print('Depth First Search took: ', stop-start, ' milliseconds')
    return prev

# Traverses adjacency list using depth-first search with recursion
def depth_first_search_recursion(G, source):
    visited[source] = True  # Source starts at 0 and moves on recursively
    for t in G[source]:
        if not visited[t]:  # if visited[t] is False
            prev[t] = source  # the source is appended to prev list
            depth_first_search_recursion(G, t)
    return prev

# Travereses adjacency list using breadth-first search
def breadth_first_search(G):
    start = time.time()*1000
    visited = [False] * len(G)  # creates a list of boolean False of length G
    prev = [-1] * len(G)  # creates a list of -1 of length G
    Q = queue.Queue()  # a queue that starts empty
    Q.put(0)  #  Starting point is vertex 0 so it is placed fist
    visited[0] = True  # Visisted list is changed to True for 0, the starting point
    # Traversal starts from 0
    while Q.empty() is False:  # While the queue is not empty
        v = Q.get()  # v is for the vertext which is popped from Q
        for t in G[v]:
            if not visited[t]:  # if visited[t] is False
                visited[t] = True
                prev[t] = v  # the vertex is assigned to prev list
                Q.put(t)
    stop = time.time()*1000
    print('Breadth First Search took: ', stop-start, ' milliseconds')
    return prev
    
def Union_Maze(M, w, m):  # creates a maze and asks the user how many walls to remove
    
    popped = []
    start_union = time.time() * 1000

    while m > 0:
        d = random.randint(0, len(walls)-1) # d equals the wall to be removed at random
        if NumSets(M) == 1:
            popped.append(walls.pop(d))
            m -= 1
        elif union_c(M, walls[d][0], walls[d][1]) is True:
            popped.append(walls.pop(d))
            m -=1

    stop_union = time.time() * 1000
    print('Running time for this maze is with maze size: ', 
          maze_rows, ' rows, ', maze_cols, ' columns, time in milliseconds: ', (stop_union-start_union))
    
    temp_list = []
    for i in range(maze_rows*maze_cols):
        temp_list.append([])
        
    adj_list = get_adj_list(popped, temp_list)
    return adj_list

plt.close("all") 
maze_rows = 10
maze_cols = 15
n = maze_rows*maze_cols  # Total number of cells in the maze

walls = wall_list(maze_rows,maze_cols) # Creates the walls for the maze
M = DisjointSetForest(maze_rows*maze_cols)
draw_maze(walls,maze_rows,maze_cols,cell_nums=True)

# This loop created in case user wants to remove more walls than the ones in the maze
while True:
    m = int(input('How many walls do you want to remove: '))  # Asks user for number of walls to be removed
    # This checks if the user wants to remove more walls than there are in the maze.
    if m > len(walls)-1:
        print('The number of walls you want to remove exeeds the number of walls that are present.')
        continue  # This will cause the loop to continue and ask the user to select less walls to remove        
    if m > n-1:
        print('There is at least one path from source to destination (m > n-1).')
        break  # Will exit loop
    if m < n-1:
        print('A path from source to destination is not guaranteed to exist (m < n-1).')
        break  # Will exit loop
    if m == n-1:
        print('There is a unique path from source to destination (m = n-1).')
        break  # will exit loop
    
G = Union_Maze(M, walls, m)  # Creates maze

visited = [False] * len(G)  # variable created to be used by depth_first_search_recursion
prev = [-1] * len(G)  # variable created to be used by depth_first_search_recursion

bfs = breadth_first_search(G)
print('Breadth First Search: ', bfs)
dfs = depth_first_search(G)
print('Depth First Search: ', dfs)
start_dfsr = time.time()
dfsr = depth_first_search_recursion(G, 0)
stop_dfsr = time.time()
print('Depth First Search using recursion took: ', stop_dfsr-start_dfsr, ' milliseconds')
print('Depth First Search using recursion: ', dfsr)

line = draw_maze(walls,maze_rows,maze_cols)  # used to send to path to generate path from start to goal
# Path will generate a red line from start to goal if path is available
ans = int(input('How do you want to generate a path if at least one is available, select 1 for Breadth First Search, 2 for Depth First Search, or 3 for Depth First Search using recursion: '))
start_path = time.time()*1000
if ans == 1:  # Will generate a path using breadth first search
    path(line,bfs,(n)-1,maze_cols-.5,maze_rows-.5)
elif ans== 2:  # Will generate a path using depth first search
    path(line,dfs,(n)-1,maze_cols-.5,maze_rows-.5)
else:  # Will generate a path using depth first search using recursion
    path(line,dfsr,(n)-1,maze_cols-.5,maze_rows-.5)
stop_path = time.time()*1000
print('It took ', stop_path-start_path, ' milliseconds to generate a path, (if one exists) from start to goal.')
draw_maze(walls,maze_rows,maze_cols)
plt.show()
