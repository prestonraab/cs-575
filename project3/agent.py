import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from networkx.algorithms import community

class Agent:
    def __init__(self, node_id, initial_state='B'):
        self.node_id = node_id
        self.state = initial_state
        self.next_state = initial_state

    def compute_next_state(self, G, agent_map, threshold_type, threshold_val, debug=False):
        if self.state == 'A':
            return
            
        neighbors = list(G.neighbors(self.node_id))
        if not neighbors:
            return
            
        a_count = sum(1 for n in neighbors if agent_map[n].state == 'A')
        
        if debug:
            print(f"DEBUG: Node {self.node_id} has {a_count} 'A' neighbors out of {len(neighbors)}.")
            
        if threshold_type == 'absolute':
            if a_count >= threshold_val:
                self.next_state = 'A'
        elif threshold_type == 'fractional':
            fraction = a_count / len(neighbors)
            if fraction >= threshold_val:
                self.next_state = 'A'

    def update_state(self):
        """Apply the computed state synchronously."""
        self.state = self.next_state

class Population:
    def __init__(self, G, early_adopters, threshold_type='fractional', threshold_val=0.2):
        """Initialize population and networks."""
        self.G = G
        self.threshold_type = threshold_type
        self.threshold_val = threshold_val
        self.history = {'A': [], 'B': []}
        self.agent_map = {}
        
        # Initialize early adopters as A, others as B.
        for node_id in G.nodes():
            state = 'A' if node_id in early_adopters else 'B'
            self.agent_map[node_id] = Agent(node_id, state)
            
        self.record_history()

    def record_history(self):
        """Log the current counts of states A and B."""
        a_count = sum(1 for agent in self.agent_map.values() if agent.state == 'A')
        b_count = len(self.agent_map) - a_count
        self.history['A'].append(a_count)
        self.history['B'].append(b_count)

    def update(self, debug=False):
        # Compute next state.
        for agent in self.agent_map.values():
            agent.compute_next_state(self.G, self.agent_map, self.threshold_type, self.threshold_val, debug=debug)
            
        # Apply the new states.
        for agent in self.agent_map.values():
            agent.update_state()
            
        self.record_history()

# ==========================================
#  Graph Utils
# ==========================================

def load_and_project_kg(filepath, debug=False):
    G_kg = nx.read_graphml(filepath)

    # Identify person nodes.
    persons = [n for n, attr in G_kg.nodes(data=True) if attr.get('kind') == 'person']
    
    if debug:
        print(f"DEBUG: Found {len(persons)} person nodes out of {G_kg.number_of_nodes()} total nodes.")

    # Create one-mode projection graph.
    G_user = nx.Graph()
    
    # Add person nodes with their attributes (e.g., Student, TA, Instructor).
    for p in persons:
        G_user.add_node(p, **G_kg.nodes[p])
        
    # Connect persons if they share a common thread or channel.
    for p in persons:
        neighbors = set(G_kg.neighbors(p))
        for neighbor in neighbors:
            other_persons = [n for n in G_kg.neighbors(neighbor) if n in persons and n != p]
            for op in other_persons:
                if G_user.has_edge(p, op):
                    G_user[p][op]['weight'] += 1
                else:
                    G_user.add_edge(p, op, weight=1)
                    
    if debug:
        print(f"DEBUG: Projected graph has {G_user.number_of_edges()} edges.")
        
    return G_user

def analyze_user_network(G):
    """Compute centralities and communities for the user network."""
    # Compute centralities.
    degree_cent = nx.degree_centrality(G)
    pagerank_cent = nx.pagerank(G, weight='weight')
    
    try:
        eigen_cent = nx.eigenvector_centrality(G, max_iter=1000, weight='weight')
    except nx.PowerIterationFailedConvergence:
        print("Warning: Eigenvector centrality failed to converge. Defaulting to 0.")
        eigen_cent = {n: 0 for n in G.nodes()}

    # Compute Louvain communities.
    communities = community.louvain_communities(G, weight='weight')
    comm_map = {}
    for i, comm_set in enumerate(communities):
        for node in comm_set:
            comm_map[node] = i

    # Build DataFrame.
    data = []
    for node, attrs in G.nodes(data=True):
        data.append({
            'NodeID': node,
            'Role': attrs.get('value', 'Unknown'), # Expected: Student, TA, Instructor
            'Degree': degree_cent.get(node, 0),
            'Eigenvector': eigen_cent.get(node, 0),
            'PageRank': pagerank_cent.get(node, 0),
            'Community': comm_map.get(node, -1)
        })

    df = pd.DataFrame(data)
    return df

# ==========================================
# Experiments
# ==========================================

def run_cascade(network, early_adopters, threshold_type='fractional', threshold_val=0.2, debug=False):
    """Run simulation until cascade stops."""
    pop = Population(network, early_adopters, threshold_type, threshold_val)
        
    t = 0
    while True:
        prev_A = pop.history['A'][-1]
        pop.update(debug=debug)
        t += 1
        
        # Stop when no new agents adopt the behavior.
        if pop.history['A'][-1] == prev_A:
            break
            
    return pop.history

def plot_adoption_curve(history, title):
    """Plot total adoptions over time."""
    plt.figure(figsize=(8, 5))
    plt.plot(history['A'], label="Adopted (A)", color="cyan", linewidth=2)
    plt.plot(history['B'], label="Baseline (B)", color="blue", linewidth=2)
    plt.title(title)
    plt.xlabel("Time Step")
    plt.ylabel("Number of Agents")
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.legend()
    plt.grid(True)
    plt.show()

# ==========================================
# Workflow
# ==========================================
if __name__ == "__main__":
    graph_file = "project_3_graph.graphml"
    
    print(f"Loading and projecting {graph_file}...")
    G_users = load_and_project_kg(graph_file, debug=False)
    
    print("\nAnalyzing network metrics and identifying communities...")
    df_metrics = analyze_user_network(G_users)
    
    print("\nTop 5 Influential Users by PageRank:")
    top_pagerank = df_metrics.sort_values(by='PageRank', ascending=False).head(5)
    print(top_pagerank[['NodeID', 'Role', 'PageRank', 'Community']].to_string(index=False))
    
    print("\nRunning Fractional Threshold Cascade (f=0.2)...")
    # Use node IDs of the top 5 pagerank users as seeds
    seed_nodes = top_pagerank['NodeID'].tolist()
    
    history = run_cascade(
        network=G_users, 
        early_adopters=seed_nodes, 
        threshold_type='fractional', 
        threshold_val=0.2
    )
    
    plot_adoption_curve(history, "Project 3: Discord Cascade (Seeds: Top 5 PageRank | Threshold: 20%)")
    print(f"Final Adoption Count: {history['A'][-1]} / {G_users.number_of_nodes()}")
    