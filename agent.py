import random

from base_agent import BaseAgent


class Agent(BaseAgent):
    def __init__(self, name, state, ally_state, cow_state):
        super(Agent, self).__init__(name=name, state=state, ally_state=ally_state, cow_state=cow_state)
        self.q_table = {}
        self.e = 1
        self.l = 1
        self.g = 0.9

    def choose_action(self, ):
        s = (self.state[0], self.state[1], self.ally_state[0], self.ally_state[1],
             self.cow_state[0], self.cow_state[1])
        if random.random() < self.e:
            action = random.randrange(9)
        else:

            max_value = max(self.q_table[s])
            action = self.q_table[s].index(max_value)
        self.s = s
        self.action = action
        return action

    def do_update(self, reward):
        if reward == 50:
            v = 10
        s_ = (self.state_prime[0], self.state_prime[1], self.ally_state_prime[0], self.ally_state_prime[1],
              self.cow_state_prime[0], self.cow_state_prime[1])

        if s_ in self.q_table.keys():
            value = max(self.q_table[s_])
        else:
            self.q_table[s_] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            value = max(self.q_table[s_])

        if self.s not in self.q_table.keys():
            self.q_table[self.s] = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.q_table[self.s][self.action] = self.l * (reward + self.g * value) + (1 - self.l) * self.q_table[self.s][self.action]

        self.state = self.state_prime
        self.ally_state = self.ally_state_prime
        self.cow_state = self.cow_state_prime
        if reward == 50:
            self.l *= 0.99
            self.e *= 0.98
