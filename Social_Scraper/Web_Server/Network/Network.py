import networkx as nx
from matplotlib import pyplot as plt
from Social_Scraper.Web_Server.Network.Node import Node

class Network(Node):
    def __init__(self, name):
        self.name = name
        self.edges = []
        self.senders = []
        self.receivers = []
        self.nodes = []

        super().__init__(identifier=name, description=name, type=str(type(self)))

        self.G = nx.DiGraph()
        self.pos = nx.spring_layout(self.G)
        self.options = {"node_size": 500, "alpha": 0.8}

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)
        self.senders.append(edge.get_sender())
        self.receivers.append(edge.get_receiver())

    def show_graph(self):
        for node in self.nodes:
            self.G.add_node(node.get_id(), type=node.type)

        #for node in self.receivers:
        #    self.G.add_node(node.get_id(), type=node.type)

        for i,edge in enumerate(self.edges):
            self.G.add_edge(edge.sender.get_id(), edge.receiver.get_id(), kin=i, label=edge.description())

        #metrics
        degree_centrality = nx.degree_centrality(self.G)
        closeness_centrality = nx.closeness_centrality(self.G)
        betweenness_centrality = nx.betweenness_centrality(self.G)

        #visualize
        nx.draw_spring(self.G, with_labels=True, node_size=3000)
        plt.show()
