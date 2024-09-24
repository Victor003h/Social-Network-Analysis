import networkx as nx

# Degree_centrality
def DegreeCentrality(G,scaleValue):
    degree_centrality=nx.degree_centrality(G)
    #degree_centrality=nx.degree(G)
    
    for node,newsize in degree_centrality.items():
        value=newsize * scaleValue
        G.nodes[node]['size']=value

    return (G,degree_centrality)

def DegreeCentralityReport(degree_centrality):
    lists= max(degree_centrality.values())


def BetweennessCentrality(G,scaleValue):
    degree_centrality=nx.betweenness_centrality(G)
    #degree_centrality=nx.degree(G)
    
    for node,newsize in degree_centrality.items():
        value=newsize * scaleValue
        G.nodes[node]['size']=value

    return (G,degree_centrality)


def ClosenessCentrality(G,scaleValue):
    degree_centrality=nx.closeness_centrality(G)
    #degree_centrality=nx.degree(G)
    
    for node,newsize in degree_centrality.items():
        value=newsize * scaleValue
        G.nodes[node]['size']=value

    return (G,degree_centrality)
