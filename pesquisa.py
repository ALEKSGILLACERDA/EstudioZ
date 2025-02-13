from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# Função para calcular o nível de atividade
def calcular_nivel_atividade(soma):
    if soma <= -1:
        return 'inativo'
    elif soma <= 4:
        return 'pouco ativo'
    elif soma <= 7:
        return 'ativo'
    elif soma <= 12:
        return 'muito ativo'
    else:
        return 'globeleza'

# Função para determinar a personalidade
def determinar_personalidade(nivel_atividade, respostas):
    maratonar_series, tomar_todas, trabalhar, paquerar, dar_close = respostas
    personalidade = 'folião moderado'  # Valor padrão

    if nivel_atividade == 'inativo':
        if trabalhar > 4:
            personalidade = 'workholic'
        else:
            personalidade = 'Carnaval não dá xp'
    elif nivel_atividade == 'pouco ativo':
        if tomar_todas > 4:
            personalidade = 'boemio'
        elif paquerar > 4:
            personalidade = 'beijoqueiro'
        elif dar_close > 4:
            personalidade = 'icone da moda'
    elif nivel_atividade == 'ativo':
        if tomar_todas + dar_close >= 8:
            personalidade = 'furacao'
        elif tomar_todas + paquerar >= 8:
            personalidade = 'amanhã é outro dia'
        elif paquerar + dar_close >= 8:
            personalidade = 'o diabo veste gliter'
    elif nivel_atividade == 'muito ativo':
        if tomar_todas + paquerar + dar_close >= 13:
            personalidade = 'globeleza'
        elif tomar_todas + dar_close >= 8:
            personalidade = 'furacao'
        elif tomar_todas + paquerar >= 8:
            personalidade = 'amanhã é outro dia'
        elif paquerar + dar_close >= 8:
            personalidade = 'o diabo veste gliter'

    return personalidade

# Criar o aplicativo Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout do aplicativo
app.layout = dbc.Container([
    html.H1("Pesquisa de Carnaval", className="text-center mt-4 mb-4"),

    dbc.Card([
        dbc.CardBody([
            # Linha para inputs
            dbc.Row([
                dbc.Col([
                    html.Label("Carnaval pra você é maratonar séries? (0 a 5)"),
                    dcc.Input(id="input-maratonar-series", type="number", min=0, max=5, value=0, className="form-control")
                ], width=6),

                dbc.Col([
                    html.Label("Carnaval pra você é tomar todas? (0 a 5)"),
                    dcc.Input(id="input-tomar-todas", type="number", min=0, max=5, value=0, className="form-control")
                ], width=6),
            ], className="mb-3"),

            dbc.Row([
                dbc.Col([
                    html.Label("Carnaval pra você é trabalhar? (0 a 5)"),
                    dcc.Input(id="input-trabalhar", type="number", min=0, max=5, value=0, className="form-control")
                ], width=6),

                dbc.Col([
                    html.Label("Carnaval pra você é paquerar? (0 a 5)"),
                    dcc.Input(id="input-paquerar", type="number", min=0, max=5, value=0, className="form-control")
                ], width=6),
            ], className="mb-3"),

            dbc.Row([
                dbc.Col([
                    html.Label("Carnaval pra você é dar close? (0 a 5)"),
                    dcc.Input(id="input-dar-close", type="number", min=0, max=5, value=0, className="form-control")
                ], width=6),
            ], className="mb-3"),

            # Botão centralizado
            dbc.Row([
                dbc.Col([
                    dbc.Button("Calcular", id="botao-calcular", color="primary", className="w-100")
                ], width=6, className="mx-auto")
            ], className="mt-3")
        ])
    ], className="shadow p-4"),

    html.Div(id="resultado", className="mt-4")
], className="container mt-4")

# Callback para calcular o resultado
@app.callback(
    Output("resultado", "children"),
    Input("botao-calcular", "n_clicks"),
    State("input-maratonar-series", "value"),
    State("input-tomar-todas", "value"),
    State("input-trabalhar", "value"),
    State("input-paquerar", "value"),
    State("input-dar-close", "value"),
)
def calcular_resultado(n_clicks, maratonar_series, tomar_todas, trabalhar, paquerar, dar_close):
    if n_clicks is None:
        return ""
    
    # Verificar se todas as entradas são válidas
    if None in [maratonar_series, tomar_todas, trabalhar, paquerar, dar_close]:
        return dbc.Alert("Por favor, preencha todas as notas.", color="danger")
    
    # Calcular a soma
    soma = (tomar_todas + paquerar + dar_close) - (maratonar_series + trabalhar)
    
    # Determinar o nível de atividade e a personalidade
    nivel_atividade = calcular_nivel_atividade(soma)
    personalidade = determinar_personalidade(nivel_atividade, [maratonar_series, tomar_todas, trabalhar, paquerar, dar_close])
    
    # Exibir o resultado
    return dbc.Card([
        dbc.CardBody([
            html.H4("Resultado", className="card-title"),
            html.P(f"Nível de atividade: {nivel_atividade}"),
            html.P(f"Personalidade: {personalidade}")
        ])
    ], className="shadow mt-3")

# Rodar o aplicativo
if __name__ == "__main__":
    app.run_server(debug=True)  
