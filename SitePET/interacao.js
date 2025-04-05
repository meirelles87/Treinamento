function toggleConteudo(conteudoId, botaoId) {
  const conteudo = document.getElementById(conteudoId);
  const botao = document.getElementById(botaoId);

  if (conteudo.style.display === "none" || conteudo.style.display === "") {
    conteudo.style.display = "block";
    botao.textContent = "🔽 Mostrar menos";
  } else {
    conteudo.style.display = "none";
    botao.textContent = "📖 Leia mais";
  }
}
