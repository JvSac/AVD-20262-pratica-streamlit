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
- **O que mede:** percentual de registros classificados com falha. Calcula-se dividindo a quantidade de valores iguais a 1 pelo total de classificações válidas, iguais a 0 ou 1, e multiplicando por 100.
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

## Filtros do Dashboard 2

- **Tipo de veículo:** seleção de uma ou mais categorias de vehicle_type.
- **Idade do veículo:** intervalo de vehicle_age_years, incluindo os dois limites.

Os quatro indicadores e os três gráficos consideram os mesmos filtros.
O filtro de saúde da bateria do Dashboard 1 não é aplicado ao Dashboard 2.

## Visual 1: Proporção de falhas por tipo de veículo

- **Variáveis:** vehicle_type e battery_failure.
- **Tipo de visualização:** gráfico de barras.
- **O que apresenta:** percentual de registros com falha em cada tipo de veículo, considerando somente classificações válidas, iguais a 0 ou 1.
- **Por que foi escolhido:** permite comparar a proporção de falhas entre categorias.
- **Decisão apoiada:** identificar grupos que mereçam investigação técnica.
- **Detalhes interativos:** tipo de veículo, total de registros válidos, quantidade com falha e percentual com falha.

As contagens ajudam a contextualizar os percentuais, especialmente em grupos pequenos.

## Visual 2: Saúde média por tipo de veículo

- **Variáveis:** vehicle_type e battery_health_percent.
- **Tipo de visualização:** gráfico de barras.
- **O que apresenta:** média dos valores válidos de saúde da bateria em cada tipo de veículo.
- **Por que foi escolhido:** permite comparar a condição média das baterias entre categorias.
- **Decisão apoiada:** selecionar grupos com menor saúde média para avaliação mais detalhada.
- **Detalhes interativos:** tipo de veículo, saúde média e quantidade de registros válidos.

A média resume o grupo, mas pode esconder diferenças importantes entre registros.

## Visual 3: Ciclos × saúde da bateria

- **Variáveis:** cycle_count, battery_health_percent e battery_failure.
- **Tipo de visualização:** gráfico de dispersão.
- **O que apresenta:** relação entre ciclos e saúde da bateria. Cada ponto representa um registro com valores válidos nas duas variáveis.
- **Por que foi escolhido:** permite explorar tendências, dispersão e sobreposição entre registros com e sem falha.
- **Decisão apoiada:** identificar padrões e combinações que mereçam investigação.
- **Detalhes interativos:** tipo de veículo, ciclos, saúde da bateria e classificação de falha, com zoom e deslocamento.

As cores distinguem registros sem falha, com falha e sem classificação válida.
A associação observada não comprova causalidade nem prevê falhas futuras.

## Comportamento sem registros

Quando os filtros não retornam registros:

- O total apresentado é 0.
- As médias e a proporção aparecem como “—”.
- Os gráficos não são exibidos.
- Uma mensagem orienta a selecionar tipos de veículo ou ampliar o intervalo de idade.

Quando existem registros, mas faltam valores válidos para determinado cálculo,
o indicador aparece como “—” ou o gráfico correspondente apresenta um aviso.

## Limitações da análise

O tratamento da EDA preservou 8.792 dos 20.000 registros originais,
removendo 56,04% das linhas por ausências nas variáveis selecionadas.

Essa remoção pode alterar a composição dos grupos. Os resultados descrevem
a amostra tratada e não devem ser generalizados automaticamente para toda
a população de veículos elétricos.

Os indicadores e gráficos apoiam a exploração dos dados, sem substituir
uma avaliação técnica de manutenção.
