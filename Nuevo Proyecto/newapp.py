import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import networkx as nx
import webbrowser
from threading import Timer


# Inicializar la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Network Simulator"

def open_browser():
    webbrowser.open_new("http://localhost:8050/")

# Función para generar el gráfico con Plotly
def create_figure(graph=None):
    if graph:
        pos = nx.spring_layout(graph)
        edge_x = []
        edge_y = []
        for edge in graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_x = []
        node_y = []
        for node in graph.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
            ),
            text=[str(node) for node in graph.nodes()]
        )
        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            xaxis=dict(showgrid=False, zeroline=False),
                            yaxis=dict(showgrid=False, zeroline=False)
                        ))
    else:
        fig = go.Figure()
    return fig

# Definir el layout de la aplicación
app.layout = html.Div([
    html.Header([
        html.Button('Generar Grafo', id='button-generate', className='button', style={'margin-right': 'auto'}),
        html.Button('Modificar Grafo', id='button-modify-graph', className='button', style={'margin': '0 auto'}),
        html.Div([
            html.Span("Modelo de Crecimiento", className='label'),
            dcc.Dropdown(
                id='dropdown-model',
                options=[
                    {'label': 'Opción 1', 'value': 'option1'},
                    {'label': 'Opción 2', 'value': 'option2'},
                    {'label': 'Opción 3', 'value': 'option3'},
                    {'label': 'Opción 4', 'value': 'option4'}
                ],
                value='option1',  # Opción por defecto seleccionada
                className='dropdown',
                style={'width': '200px'}
            )
        ], className='dropdown-container', style={'display': 'flex', 'align-items': 'left', 'margin-left': 'auto', 'margin-right': '20px'})
    ], className='header'),
    html.Div([
        dcc.Graph(id='graph', figure=create_figure(), style={'height': '80vh', 'width': '400vh'})
    ], className='content'),
    html.Footer([
        html.Button('Iniciar', id='button-start', className='button'),
        html.Button('Pausar', id='button-pause', className='button', disabled=True),
        html.Button('Continuar', id='button-resume', className='button', disabled=True),
        html.Button('Detener', id='button-stop', className='button', disabled=True),
        html.Div([
        html.Span("Anterior", className='label'),
        html.Button('←', id='button-previous', className='arrow-button'),
        html.Span("Siguiente", className='label'),
        html.Button('→', id='button-next', className='arrow-button')
    ], className='arrow-container', style={'display': 'flex', 'align-items': 'center', 'gap': '10px', 'margin-left': '20px'})
    ], className='footer', style={'justify-content': 'flex-start', 'gap': '10px', 'padding-left': '20px'}),
    dbc.Modal(
        [
            dbc.ModalHeader("Parámetros del Grafo"),
            dbc.ModalBody([
                dbc.Label('Cantidad de Nodos:'),
                dbc.Input(id='input-nodes', type='number', value=5),
                dbc.Label('Probabilidad de Arista:'),
                dbc.Input(id='input-probability', type='number', value=0.5, step=0.1),
            ]),
            dbc.ModalFooter(
                dbc.Button('Generar', id='generate-button', className='ml-auto')
            ),
        ],
        id='modal',
        is_open=False,
    ),
    dbc.Modal(
        [
            dbc.ModalHeader("Modificar Grafo"),
            dbc.ModalBody([
                dcc.Dropdown(
                    id='dropdown-modify',
                    options=[
                        {'label': 'Añadir Nodo', 'value': 'add_node'},
                        {'label': 'Quitar Nodo', 'value': 'remove_node'},
                        {'label': 'Añadir Arista', 'value': 'add_edge'},
                        {'label': 'Quitar Arista', 'value': 'remove_edge'}
                    ],
                    value='add_node',  # Opción por defecto
                    clearable=False,
                    searchable=False
                ),
                dbc.Label('Nombre del Nodo/Arista:'),
                dbc.Input(id='input-modify', type='text', value=''),
                dbc.Label('Nombre del Nodo 2 (para aristas):'),
                dbc.Input(id='input-modify-2', type='text', value='', style={'display': 'none'}),
            ]),
            dbc.ModalFooter(
                dbc.Button('Aplicar', id='modify-button', className='ml-auto')
            ),
        ],
        id='modify-modal',
        is_open=False,
    ),
    dbc.Modal(
        [
            dbc.ModalHeader("Error"),
            dbc.ModalBody(id='error-message'),
            dbc.ModalFooter(
                dbc.Button('Cerrar', id='close-error', className='ml-auto')
            ),
        ],
        id='error-modal',
        is_open=False,
    )
], className='container')

# Variable global para almacenar el estado de la simulación
simulation_state = 'stopped'  # Puede ser 'stopped', 'running', 'paused'
selected_model = None  # Variable global para almacenar la opción seleccionada
G = nx.Graph()  # Inicializar el grafo

@app.callback(
    [Output('graph', 'figure'), Output('modal', 'is_open'), Output('modify-modal', 'is_open'), Output('error-modal', 'is_open'), Output('error-message', 'children'), Output('input-modify-2', 'style'),
     Output('button-start', 'disabled'), Output('button-pause', 'disabled'), Output('button-resume', 'disabled'), Output('button-stop', 'disabled')],
    [Input('button-generate', 'n_clicks'), Input('generate-button', 'n_clicks'),
     Input('button-modify-graph', 'n_clicks'), Input('modify-button', 'n_clicks'), Input('close-error', 'n_clicks'), Input('dropdown-modify', 'value'),
     Input('button-start', 'n_clicks'), Input('button-pause', 'n_clicks'), Input('button-resume', 'n_clicks'), Input('button-stop', 'n_clicks'),
     Input('dropdown-model', 'value'), Input('button-previous', 'n_clicks'), Input('button-next', 'n_clicks')],
    [State('input-nodes', 'value'), State('input-probability', 'value'),
     State('dropdown-modify', 'value'), State('input-modify', 'value'), State('input-modify-2', 'value'),
     State('modal', 'is_open'), State('modify-modal', 'is_open'), State('error-modal', 'is_open')]
)
def handle_callbacks(btn_generate, btn_submit, btn_modify_graph, btn_modify, btn_close_error, modify_action,
                     btn_start, btn_pause, btn_resume, btn_stop,
                     selected_value, btn_previous, btn_next,
                     nodes, probability, action, modify_value, modify_value_2,
                     is_open, modify_is_open, error_is_open):
    global G, simulation_state, selected_model
    ctx = dash.callback_context

    if not ctx.triggered:
        return create_figure(G), is_open, modify_is_open, error_is_open, "", {'display': 'none'}, False, True, True, True

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'dropdown-model':
        selected_model = selected_value
        return create_figure(G), is_open, modify_is_open, error_is_open, "", {'display': 'none'}, False, True, True, True
    elif button_id == 'button-generate':
        if simulation_state == 'running':
            return dash.no_update, is_open, modify_is_open, error_is_open, "", {'display': 'none'}, False, True, True, True
        return dash.no_update, not is_open, modify_is_open, error_is_open, "", {'display': 'none'}, False, True, True, True
    elif button_id == 'generate-button':
        if simulation_state == 'running':
            return dash.no_update, is_open, modify_is_open, error_is_open, "", {'display': 'none'}, False, True, True, True
        G = nx.erdos_renyi_graph(nodes, probability)
        G = nx.relabel_nodes(G, {i: str(i) for i in G.nodes()})  # Renombrar nodos
        return create_figure(G), not is_open, modify_is_open, error_is_open, "", {'display': 'none'}, False, True, True, True
    elif button_id == 'button-modify-graph':
        return dash.no_update, is_open, not modify_is_open, error_is_open, "", {'display': 'none'}, False, True, True, True
    elif button_id == 'dropdown-modify':
        if modify_action in ['add_edge', 'remove_edge']:
            return dash.no_update, is_open, modify_is_open, error_is_open, "", {'display': 'block'}, False, True, True, True
        else:
            return dash.no_update, is_open, modify_is_open, error_is_open, "", {'display': 'none'}, False, True, True, True
    elif button_id == 'modify-button':
        if action == 'add_node':
            if modify_value in G.nodes:
                return dash.no_update, is_open, modify_is_open, not error_is_open, "El nodo ya existe.", {'display': 'none'}, False, True, True, True
            G.add_node(modify_value)
        elif action == 'remove_node':
            if modify_value not in G.nodes:
                return dash.no_update, is_open, modify_is_open, not error_is_open, "El nodo no existe.", {'display': 'none'}, False, True, True, True
            G.remove_node(modify_value)
        elif action == 'add_edge':
            if modify_value not in G.nodes or modify_value_2 not in G.nodes:
                return dash.no_update, is_open, modify_is_open, not error_is_open, "Uno o ambos nodos no existen.", {'display': 'block'}, False, True, True, True
            if G.has_edge(modify_value, modify_value_2):
                return dash.no_update, is_open, modify_is_open, not error_is_open, "La arista ya existe.", {'display': 'block'}, False, True, True, True
            G.add_edge(modify_value, modify_value_2)
        elif action == 'remove_edge':
            if not G.has_edge(modify_value, modify_value_2):
                return dash.no_update, is_open, modify_is_open, not error_is_open, "La arista no existe.", {'display': 'block'}, False, True, True, True
            G.remove_edge(modify_value, modify_value_2)
        return create_figure(G), is_open, not modify_is_open, error_is_open, "", {'display': 'none'}, False, True, True, True
    elif button_id == 'close-error':
        return dash.no_update, is_open, modify_is_open, not error_is_open, "", {'display': 'none'}, False, True, True, True
    elif button_id == 'button-start':
        simulation_state = 'running'
        return create_figure(G), is_open, modify_is_open, error_is_open, "", {'display': 'none'}, True, False, True, False
    elif button_id == 'button-pause':
        simulation_state = 'paused'
        return create_figure(G), is_open, modify_is_open, error_is_open, "", {'display': 'none'}, True, True, False, False
    elif button_id == 'button-resume':
        simulation_state = 'running'
        return create_figure(G), is_open, modify_is_open, error_is_open, "", {'display': 'none'}, True, False, True, False
    elif button_id == 'button-stop':
        simulation_state = 'stopped'
        return create_figure(G), is_open, modify_is_open, error_is_open, "", {'display': 'none'}, False, True, True, True
    elif button_id == 'button-previous':
        # Lógica para modificar el grafo al presionar "Anterior"
        return create_figure(G), is_open, modify_is_open, error_is_open, "", {'display': 'none'}, False, True, True, True
    elif button_id == 'button-next':
        # Lógica para modificar el grafo al presionar "Siguiente"
        return create_figure(G), is_open, modify_is_open, error_is_open, "", {'display': 'none'}, False, True, True, True

    return create_figure(G), is_open, modify_is_open, error_is_open, "", {'display': 'none'}, False, True, True, True


if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run_server(debug=False)