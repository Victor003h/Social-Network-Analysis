import networkx as nx
import plotly.graph_objects as go
import graph_analysis as ga


def DrawGraph(G):
    sizes = [G.nodes[n]['size'] for n in G.nodes()]
    pos = nx.spring_layout(G)

    node_trace = go.Scatter(
    x=[pos[node][0] for node in G.nodes()],
    y=[pos[node][1] for node in G.nodes()],
    mode='markers',
    marker=dict(size=sizes, color='blue'),
    text=[str(node) for node in G.nodes()],
    hoverinfo='text'
    )

    edge_trace = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace.append(
            go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode='lines',
                line=dict(width=1, color='black')
            )
        )

    fig = go.Figure(data=edge_trace + [node_trace],
        layout=go.Layout(
            showlegend=False,
            hovermode='closest',
            margin=dict(b=0, l=0, r=0, t=0),
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False)
        ))

    # Mostrar la figura
    fig.show()



# DrawGraph(G)


# G2,degree_centrality=ga.DegreeCentrality(G,100)
# DrawGraph(G2)

# G2,degree_centrality=ga.ClosenessCentrality(G,100)
# DrawGraph(G2)

# G2,degree_centrality=ga.BetweennessCentrality(G,100)
# DrawGraph(G2)
