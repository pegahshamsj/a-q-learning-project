from server import Server
from agent import Agent

n_episode = 10000
n_step = 500

server = Server()
agent_state_1, agent_state_2, cow_state, cow_in_corral = server.start_simulation()
agent_1 = Agent(name=1, state=agent_state_1, ally_state=agent_state_2, cow_state=cow_state)
agent_2 = Agent(name=2, state=agent_state_2, ally_state=agent_state_1, cow_state=cow_state)

for episode in range(n_episode):
    server = Server()
    agent_state_1, agent_state_2, cow_state, cow_in_corral = server.start_simulation()
    # server.show_states()
    for step in range(n_step):
        action_1 = agent_1.choose_action()
        action_2 = agent_2.choose_action()
        server.send_action(action_1, 1)
        server.send_action(action_2, 2)
        goal_state = server.step()
        # server.show_states()
        if goal_state == True:
            reward = 50
        else:
            reward = -1
        server.get_precept(agent_1)
        server.get_precept(agent_2)
        agent_1.message_passing(agent_2.state_prime)
        agent_2.message_passing(agent_1.state_prime)
        agent_1.do_update(reward)
        agent_2.do_update(reward)
        if goal_state == True:
            print(f'{episode}------ Find goal_state {step}-------')
            break
    if goal_state == False:
        print(f'{episode}: Not goal_state')
    print()
server.send_action(4, 2)
server.send_action(8, 1)
print(server.show_states())
