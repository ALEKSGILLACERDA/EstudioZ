from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# Função para calcular o nível de atividade
def calcular_nivel_atividade(soma):
    if soma <= -1:
        return 'inativo'
    elif soma <= 3:
        return 'pouco ativo'
    elif soma <= 6:
        return 'ativo'
    elif soma <= 10:
        return 'muito ativo'
    else:
        return 'globeleza'

# Função para determinar a personalidade
def determinar_personalidade(soma_funcao, respostas):
    a, b, c, d, e = respostas
    personalidade = 'folião moderado'
    if soma_funcao == 'inativo':
        if c > 4:
            personalidade = 'workholic'
        else:
            personalidade = 'Carnaval não dá xp'
    elif soma_funcao == 'pouco ativo':
        if b > 4:
            personalidade = 'boemio'
        elif d > 4:
            personalidade = 'beijoqueiro'
        elif e > 4:
            personalidade = 'icone da moda'
    elif soma_funcao == 'ativo':
        if b + e >= 8:
            personalidade = 'furacao'
        elif b + d >= 8:
            personalidade = 'amanhã é outro dia'
        elif d + e >= 8:
            personalidade = 'o diabo veste gliter'
    elif soma_funcao == 'muito ativo':
        if b + d + e >= 12:
            personalidade = 'globeleza'
    return personalidade

# Criar o aplicativo Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout do aplicativo
app.layout = dbc.Container([
    html.H1("Pesquisa de Carnaval", className="text-center mt-4 mb-4"),
    dbc.Card([
        dbc.CardBody([
            html.Label("Carnaval pra você é maratonar séries? (0 a 5)"),
            dcc.Input(id="input-a", type="number", min=0, max=5, value=0, className="mb-3"),
            
            html.Label("Carnaval pra você é tomar todas?? (0 a 5)"),
            dcc.Input(id="input-b", type="number", min=0, max=5, value=0, className="mb-3"),
            
            html.Label("Carnaval pra você é trabalhar? (0 a 5)"),
            dcc.Input(id="input-c", type="number", min=0, max=5, value=0, className="mb-3"),
            
            html.Label("Carnaval pra você é paquerar? (0 a 5)"),
            dcc.Input(id="input-d", type="number", min=0, max=5, value=0, className="mb-3"),
            
            html.Label("Carnaval pra você é dar close? (0 a 5)"),
            dcc.Input(id="input-e", type="number", min=0, max=5, value=0, className="mb-3"),
            
            dbc.Button("Calcular", id="botao-calcular", color="primary", className="mt-3" ,
            style={"marginLeft": "55px"})
        ])
    ]),
    html.Div(id="resultado", className="mt-4")
])

# Callback para calcular o resultado
@app.callback(
    Output("resultado", "children"),
    Input("botao-calcular", "n_clicks"),
    State("input-a", "value"),
    State("input-b", "value"),
    State("input-c", "value"),
    State("input-d", "value"),
    State("input-e", "value"),
)
def calcular_resultado(n_clicks, a, b, c, d, e):
    if n_clicks is None:
        return ""
    
    # Verificar se todas as entradas são válidas
    if None in [a, b, c, d, e]:
        return dbc.Alert("Por favor, preencha todas as notas.", color="danger")
    
    # Calcular a soma
    soma = (b + d + e) - (a + c)
    
    # Determinar o nível de atividade e a personalidade
    nivel_atividade = calcular_nivel_atividade(soma)
    personalidade = determinar_personalidade(nivel_atividade, [a, b, c, d, e])
    
    # Exibir o resultado
    return dbc.Card([
        dbc.CardBody([
            html.H4("Resultado", className="card-title"),
            html.P(f"Nível de atividade: {nivel_atividade}"),
            html.P(f"Personalidade: {personalidade}")
        ])
    ])

# Rodar o aplicativo
if __name__ == "__main__":
    app.run_server(debug=True)
  