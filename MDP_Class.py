import numpy as np
class MDPProcess:
    # the main grid is :
    # 100 1 2
    # 3 4 5
    # 6 7 8
    def __init__(self, reward, discount_factor=0.99):
        self.reward = reward
        self.discount_factor = discount_factor
        self.action_directions = ['right', 'left', 'up', 'down']
        self.create_transitions() # call this function to generate the transition matrix.

    def validate(self, direction):
        direction_list = []
        for i in direction:
            if (i > -1) and (i < 9):
                direction_list.append(i)
        return direction_list

    def state_directions(self, i):
        return [i + 1, i - 1, i + 3, i - 3]  #rigth, left, down, up.

    def create_transitions(self):
        self.transitions ={}
        for i in range(9):
            if self.is_terminal(i):
                continue
            else:
                for j in self.validate(self.state_directions(i)):
                    if (j - i) == 1 and not (i%3 == 2 and j%3 == 0): # not use left.
                        self.transitions[(i, j, 'right')] = 0.8
                        self.transitions[(i, j, 'down')] = 0.1
                        self.transitions[(i, j, 'up')] = 0.1
                    elif (j - i) == -1 and not (i%3 == 0 and j%3 == 2): # not use right.
                        self.transitions[(i, j, 'left')] = 0.8
                        self.transitions[(i, j, 'down')] = 0.1
                        self.transitions[(i, j, 'up')] = 0.1
                    elif (j - i) == 3: # not use up.
                        self.transitions[(i, j, 'down')] = 0.8
                        self.transitions[(i, j, 'left')] = 0.1
                        self.transitions[(i, j, 'right')] = 0.1
                    elif (j - i) == -3:  # not use down.
                        self.transitions[(i, j, 'up')] = 0.8
                        self.transitions[(i, j, 'left')] = 0.1
                        self.transitions[(i, j, 'right')] = 0.1
                    # elif (j - i) == 0 :  # not use down.
                    #     self.transitions[(i, j, 'up')] = 0.9
                    #     self.transitions[(i, j, 'left')] = 0.1
                    #     self.transitions[(i, j, 'right')] = 0.1
        dict1 = {(1, 1, 'up') : 0.8, (1, 1, 'right') : 0.1, (1, 1, 'left') : 0.1, (3, 3, 'left') : 0.8, (3, 3, 'up') : 0.1, (3, 3, 'down'): 0.1,
                 (5, 5, 'right'):0.8, (5, 5, 'up'):0.1, (5, 5, 'down'): 0.1,
                 (6, 6, 'down'):0.9, (6, 6, 'left'):0.9, (6, 6, 'right'): 0.1, (6, 6, 'up'):0.1,
                 (7, 7, 'down'):0.8, (7, 7, 'right'):0.1, (7, 7, 'left'): 0.1,
                 (8, 8, 'right'): 0.9, (8, 8, 'down'):0.9, (8, 8, 'left'): 0.1, (8, 8, 'up'):0.1}
        self.transitions.update(dict1)
        return

    def is_terminal(self, state):
        if state == 0 or state == 2:
            return True
        else: return False

    def break_condition(self, V_K_new, V_K_old, epsilon):
        temp_new_value = 0
        temp_old_value = 0
        for key in V_K_new:
            value, direction = V_K_new[key]
            temp_new_value +=value
        for key in V_K_old:
            value, direction = V_K_old[key]
            temp_old_value +=value
        if abs(temp_new_value - temp_old_value) > epsilon:
            epsilon = abs(temp_new_value - temp_old_value)
        return epsilon
    def check_stability(self, Q_star):
        for key in Q_star:
            value = Q_star[key]
            if(value != -1):
                return True
        return False

    def value_iteration(self, k_iteration):
        iteration = 0
        V_k_old = {}
        V_K_new = {}
        while iteration < k_iteration:
            print(iteration)
            V_K_new = {}
            for state in range(9):
                epsilon = 0
                Q_star = {'right': 0, 'left': 0, 'up': 0, 'down': 0}  # dictionary connect the direction and the values of Q*.
                for direction in self.action_directions:
                    # for new_state in range(9):
                    list_new_states = self.validate(self.state_directions(state))
                    list_new_states.append(state)
                    for new_state in list_new_states:
                        if (state, new_state, direction) in self.transitions:
                            V_datsh = 0
                            if new_state in V_k_old:
                                V_datsh, temp = V_k_old[new_state]
                            Q_star[direction] += self.transitions[(state, new_state, direction)]*(self.reward[new_state] + self.discount_factor * V_datsh )
                max_Q_direction = max(Q_star, key=Q_star.get) # get the max key indicate up, down, right, left.

                if self.is_terminal(state) or not(self.check_stability(Q_star)):
                    V_K_new[state] = (Q_star[max_Q_direction], 'None')
                else:
                    V_K_new[state] = (Q_star[max_Q_direction], max_Q_direction)

            epsilon = self.break_condition(V_K_new, V_k_old, epsilon)
            V_k_old = V_K_new
            print("stability ", ((1 - self.discount_factor) / (self.discount_factor)), " epsilon ", epsilon)
            if epsilon < ((1 - self.discount_factor)/(self.discount_factor )) and epsilon != 0:
                return V_K_new
            iteration +=1
        return V_K_new


    def policy_iteration(self, k_iteration):
        policy = [0,'right',0,'up','up','up','up','up','up']
        old_V = [0,0,0,0,0,0,0,0,0]
        new_V = [0,0,0,0,0,0,0,0,0]
        iterations = 0
        while iterations < k_iteration:
            is_value_changed = False
            iterations += 1
            old_V = new_V
            new_V = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            # run value iteration for each state
            for state in range(9):
                for new_state in range(9):
                    if (state, new_state,policy[state]) in self.transitions:
                        print(self.discount_factor * old_V[new_state])
                        new_V[state] += self.transitions[(state, new_state, policy[state])] * (self.reward[new_state] + (self.discount_factor * old_V[new_state]))


            for state in range(9):
                Q_star = [0,0,0,0]
                q_sa = 0
                for direction in self.action_directions:
                    for new_state in range(9):
                        if (state, new_state, direction) in self.transitions:
                            Q_star[q_sa] += self.transitions[(state, new_state, direction)] * (self.reward[new_state] + self.discount_factor * new_V[new_state])
                    q_sa += 1
                    # if q_sa > q_best:
                    #     # print
                    #     # "State", s, ": q_sa", q_sa, "q_best", q_best
                    #     policy[state] = direction
                    #     q_best = q_sa
                    #     is_value_changed = True
                    # else:
                    #     return policy
                if (policy[state] != 0):
                    if (policy[state] != self.action_directions[np.argmax(Q_star)]) or self.is_terminal(state):
                        is_value_changed = True
                    policy[state] = self.action_directions[np.argmax(Q_star)]
                else:
                    is_value_changed = True
                if(not is_value_changed):
                    return policy
            print("Iterations:", iterations)

        return policy


rewards = [100, -1, 10, -1, -1, -1, -1, -1, -1]
temp_class = MDPProcess(rewards)
# # print(temp_class.transitions)
#
print(temp_class.policy_iteration(100))
# dic_t = {}
# print(dic_t['shimaa'])
