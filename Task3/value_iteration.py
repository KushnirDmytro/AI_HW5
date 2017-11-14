#!/usr/bin/env python

#Implementation of the Value Iteration algorithm

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

def return_state_utility(v, T, u, reward, gamma):
    """Return the utility of a single state.
    This is an implementation of the Bellman equation.
    """
    action_array = np.zeros(4)

    for action in range(len(action_array)):
        action_array[action] = action  # indexes of actions from Transition matrix

    #print(T)

    actions_results_probalilities = []
    for move in range(len(action_array)):
        actions_results_probalilities.append(np.dot(v, T[move]))
    # now we have coefficients of transition probalilities to neighbouring states
    for a in range(len(action_array)):
        action_array[a] = np.dot(actions_results_probalilities[a], u)

    #print(actions_results_probalilities)
    state_utility = reward + gamma * max(action_array)

    return state_utility

def generate_graph(utility_list):
    """Given a list of utility arrays (one for each iteration)
       it generates a matplotlib graph and save it as 'output.png'
    """
    name_list = ('(1,3)', '(2,3)', '(3,3)', '+1', '(1,2)', '#', '(3,2)', '-1', '(1,1)', '(2,1)', '(3,1)', '(4,1)')
    color_list = ('cyan', 'teal', 'blue', 'green', 'magenta', 'black', 'yellow', 'red', 'brown', 'pink', 'gray', 'sienna')
    counter = 0
    index_vector = np.arange(len(utility_list))
    for state in range(12):
        state_list = list()
        for utility_array in utility_list:
             state_list.append(utility_array[state])
        plt.plot(index_vector, state_list, color=color_list[state], label=name_list[state])
        counter += 1
    #Adjust the legend and the axis
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 0.4), ncol=3, fancybox=True, shadow=True)
    plt.ylim((-1.1, +1.1))
    plt.xlim((1, len(utility_list)-1))
    plt.ylabel('Utility', fontsize=15)
    plt.xlabel('Iterations', fontsize=15)
    plt.savefig("./output.png", dpi=500)

def main():
    #Change as you want
    tot_states = 12
    gamma = 0.999 #Discount factor
    iteration = 0 #Iteration counter
    epsilon = 0.01 #Stopping criteria small value

    #List containing the data for each iteation
    graph_list = list()

    #Transition matrix loaded from file
    T = np.load("T.npy")

    #Reward vector
    r = np.array([-0.04, -0.04, -0.04,  +1.0,
                  -0.04,   0.0, -0.04,  -1.0,
                  -0.04, -0.04, -0.04, -0.04])

    #Utility vectors
    u = np.array([0.0, 0.0, 0.0,  0.0,
                   0.0, 0.0, 0.0,  0.0,
                   0.0, 0.0, 0.0,  0.0])
    u1 = np.array([0.0, 0.0, 0.0,  0.0,
                    0.0, 0.0, 0.0,  0.0,
                    0.0, 0.0, 0.0,  0.0])

    while True:
        delta = 0
        u = u1.copy()
        iteration += 1
        graph_list.append(u)
        for s in range(tot_states):
            reward = r[s]
            v = np.zeros((1,tot_states))
            v[0,s] = 1.0 #marking probability of being in some of states as 1
            u1[s] = return_state_utility(v, T, u, reward, gamma)
            delta = abs(u - u1)
           # print("DELTA")
            print(u)
            print(u1)
            print(delta)
            delta = np.sum(delta)
            #ToDo: calculate delta
			#delta = 10000
        #Stopping criteria
        if delta < epsilon* (1-gamma) / gamma:
                print("=================== FINAL RESULT ==================")
                print("Iterations: " + str(iteration))
                print("Delta: " + str(delta))
                print("Gamma: " + str(gamma))
                print("Epsilon: " + str(epsilon))
                print("===================================================")
                print(u[0:4])
                print(u[4:8])
                print(u[8:12])
                print("===================================================")
                break

    generate_graph(graph_list)

if __name__ == "__main__":
    main()