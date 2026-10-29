# Justificativa das métricas — Dashboard 2

## Métrica 1: Total de registros analisados

- **Variável:** quantidade de linhas após aplicar os filtros.
- **O que mede:** tamanho do grupo utilizado para calcular os indicadores.
- **Por que foi escolhida:** permite interpretar os demais indicadores considerando o tamanho da amostra.
- **Público-alvo:** gestores de frota e equipes de manutenção.
- **Qual decisão pode ser apoiada por essa métrica?** Avaliar se é necessário ampliar a seleção antes de comparar grupos com poucos registros.
- **O que comunica ao público-alvo:** quantos registros sustentam os resultados exibidos. A contagem não presume que cada registro corresponda a um veículo único.

## Métrica 2: Proporção de registros com falha

- **Variável:** battery_failure.
- **O que mede:** percentual de registros classificados com falha. Calcula-se dividindo a quantidade de valores iguais a 1 pelo total de valores válidos e multiplicando por 100.
- **Por que foi escolhida:** permite comparar a presença de falhas entre grupos de tamanhos diferentes, considerando também suas contagens.
- **Público-alvo:** gestores de frota e equipes de manutenção.
- **Qual decisão pode ser apoiada por essa métrica?** Identificar grupos com maior proporção observada de falhas para investigação técnica.
- **O que comunica ao público-alvo:** qual percentual do grupo apresenta falha registrada. Não representa uma previsão de falha futura nem uma taxa temporal.

## Métrica 3: Saúde média da bateria

- **Variável:** battery_health_percent.
- **O que mede:** média dos percentuais válidos de saúde da bateria no grupo selecionado.
- **Por que foi escolhida:** resume uma variável central da análise e complementa a classificação de presença ou ausência de falha.
- **Público-alvo:** gestores de frota e equipes de manutenção.
- **Qual decisão pode ser apoiada por essa métrica?** Selecionar grupos com menor saúde média para avaliação mais detalhada, considerando também as distribuições.
- **O que comunica ao público-alvo:** o nível médio de saúde das baterias analisadas. A média pode esconder diferenças entre registros e não substitui uma avaliação técnica.

## Métrica 4: Média de ciclos

- **Variável:** cycle_count.
- **O que mede:** quantidade média de ciclos registrada para as baterias do grupo selecionado, considerando valores válidos.
- **Por que foi escolhida:** contextualiza o uso acumulado e auxilia na interpretação das diferenças de saúde entre grupos.
- **Público-alvo:** gestores de frota e equipes de manutenção.
- **Qual decisão pode ser apoiada por essa métrica?** Identificar grupos com maior uso acumulado para investigar em conjunto com os indicadores de saúde e falha.
- **O que comunica ao público-alvo:** o uso acumulado médio das baterias, em ciclos. Mais ciclos não demonstram, isoladamente, a causa de uma falha.
