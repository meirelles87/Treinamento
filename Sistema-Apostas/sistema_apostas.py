class SistemaApostas:
    def __init__(self):
        self.dados = []  # Banco de dados temporário
    
    def atualizar_dados(self):
        """Método para atualizar estatísticas diariamente."""
        pass  # Implementação futura para buscar dados de sites esportivos
    
    def aplicar_filtros(self, filtros):
        """Recebe filtros e retorna jogos futuros compatíveis."""
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
def filtro_exemplo(jogo):
    return jogo.get('gols_mandante', 0) > 2  # Exemplo de critério

sistema = SistemaApostas()
sistema.atualizar_dados()
resultados = sistema.aplicar_filtros([filtro_exemplo])
sistema.exibir_resultados(resultados)
