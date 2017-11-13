#!/usr/bin/env python

#Using the Bellman equation to esimate the utility of a state

import numpy as np

def return_state_utility(v, T, u, reward, gamma):
    action_array = np.zeros(4)
	#ToDo: calculate the state value (utility)
	state_utility = -1000    
    
	return state_utility

def main():

    #ToDo: choose the state number
    #state = set the state number
	
	
    #Assuming that the discount factor is equal to 1.0
    gamma = 1.0

    #Starting state vector
    v = np.zeros(12)
    v[state] = 1.0

    #Transition matrix loaded from file
    T = np.load("T.npy")

    #Utility vector
    u = np.array([[0.812, 0.868, 0.918,   1.0,
                   0.762,   0.0, 0.660,  -1.0,
                   0.705, 0.655, 0.611, 0.388]])

    #Reward vector
    r = np.array([-0.04, -0.04, -0.04,  +1.0,
                  -0.04,   0.0, -0.04,  -1.0,
                  -0.04, -0.04, -0.04, -0.04])

    #Use the Beelman equation to find the utility of state	
    utility = return_state_utility(v, T, u, r[state], gamma)
    print("Utility of the state: " + str(utility))

if __name__ == "__main__":
    main()