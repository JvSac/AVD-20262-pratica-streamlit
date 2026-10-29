# Declaração de Uso de IA

**Nome:** preencher pelo aluno.
**Data desta assistência:** 26/10/2026.

## Ferramenta

ChatGPT, com integração do GitHub, para revisão do notebook e adaptação do esqueleto Streamlit ao dataset de baterias.

## Pedidos usados nesta conversa

- Após enviar o notebook da Aula 11: “vc pode concertar ele pra mim ?”
- Após enviar os arquivos ao repositório: “ok consegui dar push e agora ?”

Contexto fornecido: notebook de EDA, repositório-modelo da professora e imagens das instruções da primeira entrega. A etapa solicitada inclui sidebar, seletor de variáveis, filtro de intervalo e áreas de Correlação e Distribuição; heatmap e histograma ficam para a próxima aula.

## Alterações produzidas e validação

- Notebook: substituição de referências médicas, revisão de explicações, exportação de dados e execução com o dataset indicado. Detalhes e limitações constam na síntese final do notebook.
- App: uso das 13 variáveis quantitativas da EDA, seleção de variáveis para correlação, filtro de saúde da bateria aplicado às duas áreas, seletor de distribuição e prévia dos registros filtrados.
- Carregamento: caminho do CSV baseado na localização do projeto e cache de um minuto.
- Dependências: inclusão de `kagglehub` para reproduzir o download no notebook.
- Verificação da aplicação: execução e interação com os filtros usando o dataset tratado.

## Revisão do aluno

As alterações acima foram aplicadas com assistência de IA. O aluno deve revisar o código e preencher sua decisão antes da entrega:

- **Aceito e por quê:** a preencher.
- **Modificado e por quê:** a preencher.
- **Rejeitado e por quê:** a preencher, ou registrar que não houve rejeições, se for o caso.

## Limitação registrada

A remoção de ausentes adotada na EDA mantém 8.792 dos 20.000 registros (56,04% removidos). Essa escolha foi preservada e documentada, sem afirmar ausência de viés.
## Aula 22 — 29/10/2026

### Ferramenta utilizada

ChatGPT, para apoio à implementação, documentação e geração
do rascunho do Dashboard 2.

### Pedidos e contexto fornecidos

Foram fornecidos os slides da Aula 22, o código do projeto
e imagens dos resultados e erros encontrados.

Os pedidos incluíram orientações passo a passo, blocos completos
de código, justificativas no modelo da professora e uma imagem
de referência para o Dashboard 2.

### O que foi aceito

- Heatmap de correlação de Spearman e histograma com Altair.
- Organização dos dashboards em abas.
- Quatro indicadores: total de registros, proporção com falha,
  saúde média da bateria e média de ciclos.
- Filtros de tipo e idade do veículo para o Dashboard 2.
- Gráfico de proporção de falhas por tipo de veículo.
- Rascunho do Dashboard 2 gerado pelo ChatGPT.
- Apoio à redação das justificativas das métricas.

Essas sugestões foram adotadas por corresponderem ao planejamento
do projeto e às atividades propostas para a aula.

### O que foi modificado ou rejeitado

A sugestão de alterar a cor de destaque do tema foi rejeitada.
Foi mantido o tema escuro já utilizado na aplicação.

As justificativas foram organizadas conforme o modelo
disponibilizado pela professora.

### Validação realizada

Os indicadores e o agrupamento por tipo de veículo foram
calculados no notebook antes da implementação no app.

Foram conferidos o heatmap, o histograma e a atualização dos
resultados pelos filtros. No Dashboard 2, foram testados os
valores gerais, a seleção apenas de SUV e a seleção vazia.

Os resultados gerais foram: 8.792 registros, 6,54% com falha,
81,79% de saúde média e 1.367,88 ciclos em média.

### Limitações consideradas

Os resultados descrevem a amostra tratada, que preservou
8.792 dos 20.000 registros originais. A remoção de ausentes
pode alterar a composição dos grupos.

As associações observadas não comprovam causalidade e os
indicadores não representam previsões de falhas futuras.