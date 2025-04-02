import requests

class SistemaApostas:
    def __init__(self):
        self.dados = []  # Banco de dados temporário
        self.api_url = "https://api.football-data.org/v4/matches"  # Exemplo de API
        self.api_key = "SUA_CHAVE_API"  # Substitua pela sua chave real
    
    def atualizar_dados(self):
        """Método para atualizar estatísticas diariamente."""
        headers = {"X-Auth-Token": self.api_key}
        response = requests.get(self.api_url, headers=headers)
        
        if response.status_code == 200:
            self.dados = response.json().get("matches", [])
            print("Dados atualizados com sucesso!")
        else:
            print(f"Erro ao buscar dados: {response.status_code}")
    
    def filtrar_por_gols(self, jogo, min_gols=None, max_gols=None):
        """Filtra jogos pelo número de gols marcados na partida."""
        total_gols = jogo.get('score', {}).get('fullTime', {}).get('homeTeam', 0) + \
                     jogo.get('score', {}).get('fullTime', {}).get('awayTeam', 0)

        if min_gols is not None and total_gols < min_gols:
            return False
        if max_gols is not None and total_gols > max_gols:
            return False
        return True

    def filtrar_por_local(self, jogo, time, local):
        """Filtra jogos onde o time joga em casa ou fora."""
        if local == "casa":
            return jogo.get('homeTeam', {}).get('name') == time
        elif local == "fora":
            return jogo.get('awayTeam', {}).get('name') == time
        return False

    def filtrar_por_odds(self, jogo, min_odd=None, max_odd=None):
        """Filtra jogos por odds das casas de apostas."""
        odd = jogo.get('odds', {}).get('homeWin', 0)  # Exemplo pegando odd da vitória do time da casa

        if min_odd is not None and odd < min_odd:
            return False
        if max_odd is not None and odd > max_odd:
            return False
        return True

    def filtrar_por_media_gols(self, time, ultimos_jogos, min_media=None, max_media=None):
        """Filtra jogos baseando-se na média de gols do time nos últimos jogos."""
        total_gols = sum(jogo.get('score', {}).get('fullTime', {}).get('homeTeam', 0) +
                         jogo.get('score', {}).get('fullTime', {}).get('awayTeam', 0)
                         for jogo in ultimos_jogos)
        
        media_gols = total_gols / len(ultimos_jogos) if ultimos_jogos else 0

        if min_media is not None and media_gols < min_media:
            return False
        if max_media is not None and media_gols > max_media:
            return False
        return True

    def aplicar_filtros(self, filtros):
        """Recebe uma lista de filtros e retorna jogos futuros compatíveis."""
        jogos_filtrados = []
        for jogo in self.dados:
            if all(filtro(jogo) for filtro in filtros):
                jogos_filtrados.append(jogo)
        return jogos_filtrados
    
    def exibir_resultados(self, jogos):
        """Mostra os jogos filtrados ao usuário."""
        for jogo in jogos:
            print(jogo)  # Futuramente podemos formatar melhor a interface

# Exemplo de uso
sistema = SistemaApostas()
sistema.atualizar_dados()

# Criar filtros
filtros = [
    lambda jogo: sistema.filtrar_por_gols(jogo, min_gols=2),   # Jogos com pelo menos 2 gols
    lambda jogo: sistema.filtrar_por_local(jogo, "Flamengo", "casa"),  # Flamengo jogando em casa
    lambda jogo: sistema.filtrar_por_odds(jogo, min_odd=1.5, max_odd=3.0)  # Odds entre 1.5 e 3.0
]

# Aplicar filtros
resultados = sistema.aplicar_filtros(filtros)
sistema.exibir_resultados(resultados)
