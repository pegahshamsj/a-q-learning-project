import operator
import random
import math

# possible actions
ACTION_NORTH = 0
ACTION_NORTH_EAST = 1
ACTION_EAST = 2
ACTION_SOUTH_EAST = 3
ACTION_SOUTH = 4
ACTION_SOUTH_WEST = 5
ACTION_WEST = 6
ACTION_NORTH_WEST = 7
ACTION_SKIP = 8

W_AGENT = -2
W_EMPTY = 1
W_OBSTACLE = -1
W_CORRAL = 1


class Server:
    __GRID_WIDTH = 5
    __GRID_HEIGHT = 5
    __CORRAL = [__GRID_WIDTH - 1, 0]
    __WEIGHT_DICT = {-1: -1,
                     100: 0,
                     1: -2,
                     2: -2,
                     0: 1}
    __OBSTACLES = [[1, 1], [1, 2]]
    __SKIP_NO = 8
    __Action_DICT = {0: (1, 0),
                     1: (1, 1),
                     2: (0, 1),
                     3: (-1, 1),
                     4: (-1, 0),
                     5: (-1, -1),
                     6: (0, -1),
                     7: (1, -1),
                     __SKIP_NO: (0, 0)}

    __AGENT_NO = 2

    def __init__(self):
        self.__goal_state = False
        self.__agent_state_1 = [0, self.__GRID_HEIGHT - 1]
        self.__agent_state_2 = [self.__GRID_WIDTH - 1, self.__GRID_HEIGHT - 1]
        self.__cow_state = [2, self.__GRID_HEIGHT - 1]
        self.__cow_counter = 0
        self.__grid = [[-1 if [i, j] in self.__OBSTACLES else 0 for j in range(self.__GRID_WIDTH)]
                       for i in range(self.__GRID_HEIGHT)]
        self.__grid[self.__CORRAL[0]][self.__CORRAL[1]] = 100
        self.__reset_action_dict()
        self.__refresh_grid()

    def __reset_action_dict(self):
        self.__actions_dict = dict()
        self.__actions_dict.setdefault(1, self.__SKIP_NO)
        self.__actions_dict.setdefault(2, self.__SKIP_NO)

    def start_simulation(self):
        self.__init__()
        return self.__agent_state_1, self.__agent_state_2, self.__cow_state, self.__goal_state

    def send_action(self, action, agent_number):
        if agent_number > self.__AGENT_NO:
            print(f'{agent_number} is not registered in server')
        else:
            self.__actions_dict[agent_number] = action

    def step(self):
        action_1 = self.__actions_dict[1]
        action_2 = self.__actions_dict[2]
        if random.random() > 0.5:
            self.__move_agent(action_1, 1)
            self.__move_agent(action_2, 2)
        else:
            self.__move_agent(action_2, 2)
            self.__move_agent(action_1, 1)
        if self.__cow_counter % 2 == 0:
            self.__move_cow()
        self.__cow_counter += 1
        self.__refresh_grid()
        self.__reset_action_dict()
        return self.__goal_state

    def get_precept(self, agent):
        try:
            if agent.name == 1:
                agent.state_prime = self.__agent_state_1
                agent.cow_state_prime = self.__cow_state
            elif agent.name == 2:
                agent.state_prime = self.__agent_state_2
                agent.cow_state_prime = self.__cow_state
        except:
            print(f'agent is not registered in server')

    def show_states(self):
        print('***************************************')
        for row in self.__grid:
            str_ = ','.join(f"{col: ^4d}" for col in row)
            print(str_)

    def __get_cell_value(self, cell_i, cell_j):
        value = 0
        if self.__CORRAL == [cell_i, cell_j]:
            value = -100
        else:
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if i == 0 and j == 0:
                        continue
                    try:
                        value += self.__WEIGHT_DICT[self.__grid[cell_i + i][cell_j + j]]
                    except:
                        pass
        return value

    def __move_cow(self):
        grid = self.__grid
        cow_i, cow_j = self.__cow_state
        around_cell_lst = []
        for i, j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            try:
                neighbour_i = cow_i + i
                neighbour_j = cow_j + j
                if neighbour_j >= 0 and neighbour_i >= 0:
                    if grid[neighbour_i][neighbour_j] in [0, 100]:
                        around_cell_lst.append((neighbour_i, neighbour_j))
            except:
                pass
        pos_value_dict = {}
        for i, j in around_cell_lst:
            pos_value_dict[(i, j)] = self.__get_cell_value(i, j)
        if len(pos_value_dict):
            max_value = max(pos_value_dict.items(), key=operator.itemgetter(1))[1]
            positions = [key for key, value in pos_value_dict.items() if value == max_value]
            cow_move_i, cow_move_j = random.choice(positions)
            self.__cow_state[0] = cow_move_i
            self.__cow_state[1] = cow_move_j
            if self.__cow_state == self.__CORRAL:
                self.__goal_state = True

    def __move_agent(self, action, agent_number):
        move_i, move_j = self.__Action_DICT[action]
        if agent_number == 1:
            state = self.__agent_state_1
        else:
            state = self.__agent_state_2
        i_prime = state[0] + move_i
        j_prime = state[1] + move_j
        if i_prime >= 0 and j_prime >= 0:
            try:
                cell_content = self.__grid[i_prime][j_prime]
                if cell_content == 0:
                    state[0] += move_i
                    state[1] += move_j
            except:
                pass
            self.__refresh_grid()

    def __refresh_grid(self):
        self.__grid = [[-1 if [i, j] in self.__OBSTACLES else 0 for j in range(self.__GRID_WIDTH)]
                       for i in range(self.__GRID_HEIGHT)]
        self.__grid[self.__CORRAL[0]][self.__CORRAL[1]] = 100
        self.__grid[self.__agent_state_1[0]][self.__agent_state_1[1]] = 1
        self.__grid[self.__agent_state_2[0]][self.__agent_state_2[1]] = 2
        self.__grid[self.__cow_state[0]][self.__cow_state[1]] = 50


if __name__ == '__main__':
    s = Server()
