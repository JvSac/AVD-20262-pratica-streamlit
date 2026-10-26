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
