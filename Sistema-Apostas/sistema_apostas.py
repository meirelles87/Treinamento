import requests
from datetime import datetime
from flask import Flask, jsonify

app = Flask(__name__)

class SistemaApostas:
    def __init__(self):
        self.dados = []  # Banco de dados temporário
        self.api_url = "https://api.football-data.org/v4/matches"  # Nova API confiável
        self.api_key = "c278f48363ee49eb9c979a338104addc"  # Chave de API fornecida pelo usuário
        self.torneios = ["WC", "CL", "BL1", "DED", "BSA", "PD", "FL1", "ELC", "PPL", "EC", "SA", "PL"]
    
    def atualizar_dados(self):
        """Método para atualizar estatísticas diariamente."""
        headers = {
            "X-Auth-Token": self.api_key,
            "Content-Type": "application/json"
        }
        response = requests.get(f"{self.api_url}?competitions={','.join(self.torneios)}", headers=headers)
        
        if response.status_code == 200:
            self.dados = response.json().get("matches", [])
            print(self.dados)
            print("Dados atualizados com sucesso!")
        else:
            print(f"Erro ao buscar dados: {response.status_code} - {response.text}")
    
    def filtrar_por_gols(self, jogo, min_gols=None, max_gols=None):
        """Filtra jogos pelo número de gols marcados na partida."""
        gols_casa = jogo.get('score', {}).get('fullTime', {}).get('home', 0) or 0
        gols_fora = jogo.get('score', {}).get('fullTime', {}).get('away', 0) or 0
        total_gols = gols_casa + gols_fora

        if min_gols is not None and total_gols < min_gols:
            return False
        if max_gols is not None and total_gols > max_gols:
            return False
        return True

    def filtrar_por_local(self, jogo, time, local):
        """Filtra jogos onde o time joga em casa ou fora."""
        if local == "casa":
            return jogo.get('homeTeam', {}).get('name', '') == time
        elif local == "fora":
            return jogo.get('awayTeam', {}).get('name', '') == time
        return False

    def filtrar_por_odds(self, jogo, min_odd=None, max_odd=None):
        """Filtra jogos por odds das casas de apostas."""
        odd = jogo.get('odds', {}).get('homeWin', 0) or 0

        if min_odd is not None and odd < min_odd:
            return False
        if max_odd is not None and odd > max_odd:
            return False
        return True

    def aplicar_filtros(self, filtros):
        """Recebe uma lista de filtros e retorna jogos futuros compatíveis."""
        jogos_filtrados = []
        for jogo in self.dados:
            if all(filtro(jogo) for filtro in filtros):
                jogos_filtrados.append(jogo)
        return jogos_filtrados

sistema = SistemaApostas()
sistema.atualizar_dados()

@app.route('/')
def home():
    """Página inicial que exibe os jogos filtrados."""
    filtros = [
        lambda jogo: sistema.filtrar_por_gols(jogo, min_gols=2),   # Jogos com pelo menos 2 gols
        lambda jogo: sistema.filtrar_por_local(jogo, "Flamengo", "casa"),  # Flamengo jogando em casa
        lambda jogo: sistema.filtrar_por_odds(jogo, min_odd=1.5, max_odd=3.0)  # Odds entre 1.5 e 3.0
    ]
    resultados = sistema.aplicar_filtros(filtros)
    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True)
