#!/usr/bin/env python

import numpy as np

def return_policy_evaluation(p, u, r, T, gamma):
    # v = R + γPv <=== initial form
    # (I − γP) v = R < == step 1
    # v = (I − γP)inv −1 * R < === answer of equasion to calculate

    transition_probabilities_matrix = []

    for state in range(len(u)):
        policy = p[state]
        transition_probabilities_matrix.append(T[policy][state]) # transitions from the corresponding state

    I = np.identity(len(u))

    matr_to_invert = I -  np.dot(transition_probabilities_matrix, gamma)

    inverted_matrix  = np.linalg.inv(matr_to_invert)

    answer = np.dot(r, inverted_matrix.transpose())
    return answer


def return_expected_action(u, T, v):
    """Return the expected action.
    It returns an action based on the
    expected utility of doing a in state s,
    according to T and u. This action is
    the one that maximize the expected
    utility.
    @param u utility vector
    @param T transition matrix
    @param v starting vector
    @return expected action (int)
    """
    actions_array = np.zeros(4)

    for action in range(len(actions_array)):
        a = np.dot(v, T[action])
        c = np.dot(a,u)
        actions_array[action] = c[0]

    expected_action = np.argmax(actions_array)
    return expected_action

def print_policy(p, shape):
    """Print the policy on the terminal
    Using the symbol:
    * Terminal state
    ^ Up
    > Right
    v Down
    < Left
    # Obstacle
    """
    counter = 0
    policy_string = ""
    for row in range(shape[0]):
        for col in range(shape[1]):
            if(p[counter] == -1): policy_string += " *  "
            elif(p[counter] == 0): policy_string += " ^  "
            elif(p[counter] == 1): policy_string += " >  "
            elif(p[counter] == 2): policy_string += " v  "
            elif(p[counter] == 3): policy_string += " <  "
            elif(p[counter]==-2): policy_string += " #  "
            counter += 1
        policy_string += '\n'
    print(policy_string)


def main():
    """Finding the solution using the iterative approach
    """
    gamma = 0.999
    iteration = 0
    T = np.load("T.npy")

    #Generate the first policy randomly
    # Nan=Nothing, -1=Terminal, 0=Up, 1=Left, 2=Down, 3=Right
    p = np.random.randint(0, 4, size=(12))
    p[5] = -2 #don't like arrays of floats here
    p[3] = p[7] = -1

    #Utility vectors
    u = np.array([0.0, 0.0, 0.0,  0.0,
                   0.0, 0.0, 0.0,  0.0,
                   0.0, 0.0, 0.0,  0.0])
    #Reward vector
    r = np.array([-0.04, -0.04, -0.04,  +1.0,
                  -0.04,   0.0, -0.04,  -1.0,
                  -0.04, -0.04, -0.04, -0.04])

    while True:
        iteration += 1
        epsilon = 0.0001
        #1- Policy evaluation
        u1 = u.copy()
        u = return_policy_evaluation(p, u, r, T, gamma)

        #Stopping criteria
        delta = np.sum(abs(u-u1))

        # print(delta)
        if delta < epsilon * (1-gamma) *gamma: break
        for s in range(12):
            if not p[s]==-2 and not p[s]==-1: #skipping evaluation for terminal and impossible states
                v = np.zeros((1,12))
                v[0,s] = 1.0 # assuming probability of being in current state as 1
                #2- Policy improvement
                a = return_expected_action(u, T, v)
                if a != p[s]: p[s] = a
        # print(u[0:4])
        # print(u[4:8])
        # print(u[8:12])
        # print_policy(p, shape=(3,4))

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
    print_policy(p, shape=(3,4))
    print("===================================================")


if __name__ == "__main__":
    main()