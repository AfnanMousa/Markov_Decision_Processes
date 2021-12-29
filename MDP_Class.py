class MDPProcess:
    # the main grid is :
    # 0 1 2
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

    def break_condition(self, V_K_new, V_k_old, state, epsilon):
        temp_new_value, temp_new_direction = V_K_new[state]
        temp_old_value, temp_old_direction = 0, 'None'
        if state in V_k_old:
            temp_old_value, temp_old_direction = V_k_old[state]
        if abs(temp_new_value - temp_old_value) > epsilon:
            epsilon = abs(temp_new_value - temp_old_value)
        return epsilon

    def value_iteration(self, k_iteration):
        i = 0
        V_k_old = {}
        V_K_new = {}
        while i < k_iteration:
            print(i)
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
                if self.is_terminal(state):
                    V_K_new[state] = (Q_star[max_Q_direction], 'None')
                else:
                    V_K_new[state] = (Q_star[max_Q_direction], max_Q_direction)

                epsilon = self.break_condition(V_K_new, V_k_old, state, epsilon)
                V_k_old[state] = V_K_new[state]
                print("convergence ", ((1 - self.discount_factor) / (self.discount_factor)), " delta ", epsilon)
                if epsilon < ((1 - self.discount_factor)/(self.discount_factor )) and epsilon != 0:
                    return V_K_new
            i +=1
        return V_K_new

    # def policy_iteration(self):


# rewards = [100, -1, 10, -1, -1, -1, -1, -1, -1]
# temp_class = MDPProcess(rewards)
# # print(temp_class.transitions)
#
# print(temp_class.value_iteration(100))
# dic_t = {}
# print(dic_t['shimaa'])
