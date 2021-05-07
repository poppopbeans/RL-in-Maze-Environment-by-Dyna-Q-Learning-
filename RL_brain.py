import numpy as np
import pandas as pd
import random


class Agent:
    ### START CODE HERE ###

    def __init__(self, actions):
        self.actions = actions
        self.epsilon = 0.4
        self.epsilon_min=0.02
        self.epsilon_decay=0.002
        self.epsilon2 = 0.1
        self.epsilon_min2 = 0.02
        self.epsilon_decay2 = 0.001

    def choose_action(self, s,Q_value,episode,eating):
        si=int(s[0]/40)
        sj=int(s[1]/40)
        if eating==False:
            k=30
        else:
            k=5
        if episode<50:
            max_value=max(Q_value[si][sj][i]+k/Q_value[si][sj][i+4] for i in range(4))
            action_list=[i for i in range(4) if Q_value[si][sj][i]+k/Q_value[si][sj][i+4]==max_value ]
            action=random.choice(action_list)
        else:
            max_value = max(Q_value[si][sj][:4])
            action_list = [i for i in range(4) if Q_value[si][sj][i]  == max_value]
            action = random.choice(action_list)
            ran=random.random()
            if eating==False:
                if self.epsilon>self.epsilon_min:
                    self.epsilon-=self.epsilon_decay
                if ran<self.epsilon:
                    action_list1=[0,1,2,3]
                    action_list1.remove(action)
                    action=random.choice(action_list1)
            else:
                if self.epsilon2 > self.epsilon_min2:
                    self.epsilon2 -= self.epsilon_decay2
                if ran < self.epsilon2:
                    action_list2 = [0, 1, 2, 3]
                    action_list2.remove(action)
                    action = random.choice(action_list2)
        return action

    ### END CODE HERE ###