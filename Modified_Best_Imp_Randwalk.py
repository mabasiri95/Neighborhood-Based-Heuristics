#basic hill climbing search provided as base code for the DSA/ISE 5113 course
#author: Charles Nicholson
#date: 4/5/2019

#NOTE: You will need to change various parts of this code.  However, please keep the majority of the code intact (e.g., you may revise existing logic/functions and add new logic/functions, but don't completely rewrite the entire base code!)  
#However, I would like all students to have the same problem instance, therefore please do not change anything relating to:
#   random number generation
#   number of items (should be 150)
#   random problem instance
#   weight limit of the knapsack

#------------------------------------------------------------------------------

#Student name: Group 7
#Date: 03/31/2023


#need some python libraries
import copy
from random import Random   #need this for the random number generation -- do not change
import numpy as np
import random


#to setup a random number generator, we will specify a "seed" value
#need this for the random number generation -- do not change
seed = 51132023
myPRNG = Random(seed)

#to get a random number between 0 and 1, use this:             myPRNG.random()
#to get a random number between lwrBnd and upprBnd, use this:  myPRNG.uniform(lwrBnd,upprBnd)
#to get a random integer between lwrBnd and upprBnd, use this: myPRNG.randint(lwrBnd,upprBnd)

#number of elements in a solution
n = 150

#create an "instance" for the knapsack problem
value = []
for i in range(0,n):
    value.append(round(myPRNG.triangular(5,1000,200),1))
    
weights = []
for i in range(0,n):
    weights.append(round(myPRNG.triangular(10,200,60),1))
    
#define max weight for the knapsack
maxWeight = 2500

#change anything you like below this line ------------------------------------

#monitor the number of solutions evaluated
solutionsChecked = 0

#function to evaluate a solution x
# returns totalValue[0], totalWeight[1]
def evaluate(x):
          
    a=np.array(x)
    b=np.array(value)
    c=np.array(weights)
    isFeasible = True
    
    totalValue = np.dot(a,b)     #compute the value of the knapsack selection
    totalWeight = np.dot(a,c)    #compute the weight value of the knapsack selection
    
    if totalWeight > maxWeight:
        #print ("Oh no! The solution is infeasible!  What to do?  What to do?")   #you will probably want to change this...
        isFeasible = False
        

    return [totalValue, totalWeight, isFeasible]   #returns a list of both total value and total weight
          
       
#here is a simple function to create a neighborhood
#1-flip neighborhood of solution x         
# def neighborhood(x):
        
#     nbrhood = []     
    
#     for i in range(0,len(x)):
#         nbrhood.append(x[:])
#         if nbrhood[i][i] == 1:
#             nbrhood[i][i] = 0
#         else:
#             nbrhood[i][i] = 1
      
#     return nbrhood
          

def neighborhood(x):
        
    nbrhood = []     
    
    for i in range(0,len(x)):
        if x[i] == 0: #picking stuff
            temp = x[:];
            temp[i] = 1
            nbrhood.append(temp[:])
            for j in range(0,len(x)):
                if j != i:
                    if temp[j] == 1: # dropping stuff
                        temp1 = temp[:]
                        temp1[j] = 0
                        nbrhood.append(temp1[:])
      
    return nbrhood


#create the initial solution
def initial_solution(n, weights, maxWeight):
    x = []   #i recommend creating the solution as a list
    
    #need logic here!
    for i in range(0,n):
        x.append(0)    
    
    #solnChecked = 0
    done = False
    while not done:
        prevx = x[:]    # stores previous iterations solution
        index = myPRNG.randint(0,n-1)
        #index = random.randint(0,n-1)
        x[index] = 1
        # check weights
        solnWeight = np.dot(np.array(x), np.array(weights))
        #solnChecked += 1
        if solnWeight >= maxWeight:
            done = True
 
    print("Solution initialized. Total Weight is ", np.dot(np.array(prevx), np.array(weights)))
    #print("Number of iterations: ",solnChecked)
    print("Items selected: ",sum(prevx))
            
    return prevx



def SimulatedAnnealing():
    print("Initiating local search with best improvement .........\n")
    #varaible to record the number of solutions evaluated
    solutionsChecked = 0
    
    
    x_curr = initial_solution(n, weights, maxWeight)  #x_curr will hold the current solution 
    x_best = x_curr[:]           #x_best will hold the best solution 
    f_curr = evaluate(x_curr)   #f_curr will hold the evaluation of the current soluton 
    f_best = f_curr[:]
    
    #begin local search overall logic ----------------
    done = 0
    M_k = 1
        
    while done != 10:
        m = 0
        P = 0.50
        while m < M_k:
            m = m + 1
            Neighborhood = neighborhood(x_curr)   #create a list of all neighbors in the neighborhood of x_curr
            Neighbor_ev = []
            Feasible_Neighbor =[]
            for s in Neighborhood:                #evaluate every member in the neighborhood of x_curr
                currEval = evaluate(s)[:]
                if currEval[2] == True:
                    Feasible_Neighbor.append(s)
                    Neighbor_ev.append(currEval[0])
                
                
            topidx = Neighbor_ev.index(max(Neighbor_ev))       # getting top     
            solutionsChecked = solutionsChecked + 1
            rnd = myPRNG.random()
            #if rnd > P:
            
            if f_curr[0] >   Neighbor_ev[topidx] and f_best[0] <= f_curr[0]:               #if there were no improving solutions in the neighborhood
                f_best = f_curr[:]
                x_best = x_curr[:]
                done = done + 1
            
            if rnd > P:
                x_curr = (Feasible_Neighbor[topidx])[:]        #else: move to the neighbor solution and continue
                f_curr = evaluate(x_curr)[:]         #evalute the current solution 
                if f_best[0] < f_curr[0]:
                    f_best = f_curr[:]
                    x_best = x_curr[:]
            else:
                x_curr = (Feasible_Neighbor[myPRNG.randint(0,len(Neighbor_ev)-1)])[:]        #else: move to the neighbor solution and continue
                f_curr = evaluate(x_curr)[:]         #evalute the current solution 
                if f_best[0] < f_curr[0]:
                    f_best = f_curr[:]
                    x_best = x_curr[:]
        
        
    print ("\nFinal number of solutions checked: ", solutionsChecked)
    print ("Best value found: ", f_best[0])
    print ("Weight is: ", f_best[1])
    print ("Total number of items selected: ", np.sum(x_best))
    print ("Best solution: ", x_best)
    
    results = {"Best Solution": x_best,
                      "Value": f_best[0],
                      "Weight": f_best[1],
                      "Total Number of Items selected": np.sum(x_best)}
    return(results)    


output = SimulatedAnnealing()