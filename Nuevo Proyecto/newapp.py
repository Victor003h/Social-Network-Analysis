import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt
import networkx as nx
import io
import base64

# Inicializar la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Aplicación Estética"

# Función para generar el gráfico con Matplotlib
def create_figure(graph=None):
    fig, ax = plt.subplots(figsize=(10, 6))  # Aumentar el tamaño del gráfico
    if graph:
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, ax=ax, with_labels=True, node_color='skyblue', edge_color='gray', node_size=500, font_size=10)
    else:
        ax.text(0.5, 0.5, 'No hay grafo generado', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=15)
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img = base64.b64encode(buf.read()).decode('utf-8')
    return f'data:image/png;base64,{img}'

# Definir el layout de la aplicación
app.layout = html.Div([
    html.Header([
        html.Button('Generar Grafo', id='button-generate', className='button'),
        html.Button('Botón 1', id='button-1', className='button'),
        html.Button('Botón 2', id='button-2', className='button'),
    ], className='header'),
    html.Div([
        html.Img(id='graph', src=create_figure())
    ], className='content'),
    html.Footer([
        html.Button('Botón 3', id='button-3', className='button'),
        html.Button('Botón 4', id='button-4', className='button'),
        html.Button('Botón 5', id='button-5', className='button'),
    ], className='footer'),
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
    )
], className='container')

# Callback para manejar la lógica de abrir/cerrar el modal y generar el grafo
@app.callback(
    [Output('graph', 'src'), Output('modal', 'is_open')],
    [Input('button-generate', 'n_clicks'), Input('generate-button', 'n_clicks')],
    [State('input-nodes', 'value'), State('input-probability', 'value'), State('modal', 'is_open')]
)
def handle_callbacks(btn_generate, btn_submit, nodes, probability, is_open):
    ctx = dash.callback_context

    if not ctx.triggered:
        return create_figure(), is_open

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'button-generate':
        return dash.no_update, not is_open
    elif button_id == 'generate-button':
        graph = nx.erdos_renyi_graph(nodes, probability)
        return create_figure(graph), not is_open

    return create_figure(), is_open

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
