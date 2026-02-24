from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

def get_infect_prob(contact_rate, Beta, days_infectious):
    numerator = contact_rate / (1 - contact_rate) * np.exp(Beta * (days_infectious**3 - 1))
    return numerator / (1 + numerator)

class Agent:
    def __init__(self, node_id, exposed_dist, infectious_dist, contact_rate, Beta, initial_state='S'):
        self.node_id = node_id
        self.countdown_to_infectious = np.ceil(exposed_dist.rvs())
        self.countdown_to_recovery = np.ceil(infectious_dist.rvs())
        self.days_spent_infectious = 0
        self.state = initial_state
        self.Beta = Beta
        self.contact_rate = contact_rate

    def infect_neighbors(self, G, agent_map):
        infect_prob = get_infect_prob(self.contact_rate, self.Beta, self.days_spent_infectious)
        neighbor_ids = list(G.neighbors(self.node_id))
        
        for n_id in neighbor_ids:
            neighbor_agent = agent_map[n_id]
            if neighbor_agent.state == 'S' and np.random.rand() < infect_prob:
                neighbor_agent.state = 'E'

    def update(self, G, agent_map):
        match self.state:
            case 'S':
                pass
            case 'E':
                self.countdown_to_infectious -= 1
                if self.countdown_to_infectious <= 0:
                    self.state = 'I'
            case 'I':
                self.days_spent_infectious += 1
                self.countdown_to_recovery -= 1
                if self.countdown_to_recovery <= 0:
                    self.state = 'R'
                else:
                    self.infect_neighbors()
            case 'R':
                pass


class Population:
    def __init__(self, G, exposed_dist, infectious_dist, contact_rate, Beta, p_succeptible=None, p_exposed=None, p_infectious=None):
        self.n = G.number_of_nodes()
        self.G = G

        match sum([p_succeptible is None, p_exposed is None, p_infectious is None]):
            case 3:
                p_succeptible = 0.90
                p_exposed = 0.05
                p_infectious = 0.05
            case 2: 
                raise ValueError("Must specify 0, 2, or 3 of the initial probabilities")
            case 1:
                props = [p_succeptible, p_exposed, p_infectious]
                props[props == None] = 1 - props[props != None].sum()
                p_succeptible, p_exposed, p_infectious = props
            case 0:
                if abs(sum([p_succeptible, p_exposed, p_infectious]) - 1) > 1e-10:
                    raise ValueError("Initial probabilities must sum to 1")
                p_succeptible = 1 - p_exposed - p_infectious

        n_succeptible = round(p_succeptible * self.n)
        n_exposed = round(p_infectious * self.n)
        n_infectious = self.n - n_succeptible - n_exposed

        initial_states = ['S'] * n_succeptible + ['E'] * n_exposed + ['I'] * n_infectious
        np.random.shuffle(initial_states)

        self.agent_map = {}
        for node_id, initial_state in zip(G.nodes(), initial_states):
            agent = Agent(exposed_dist, infectious_dist, initial_state)
            self.agent_map[node_id] = agent

    def update(self):
        for agent in self.agents:
            agent.update()

    def get_characteristics():
        n_succeptible, n_exposed, n_infectious, n_recovered = 0, 0, 0, 0
        for agent in self.agents:
            match agent.state:
                case 'S':
                    n_succeptible += 1
                case 'E':
                    n_exposed += 1
                case 'I':
                    n_infectious += 1
                case 'R':
                    n_recovered += 1
        
        return n_succeptible, n_exposed, n_infectious, n_recovered


        



