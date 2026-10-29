# entregas/

Artefatos de entrega que não são sobre uso de IA (isso fica em [`prompts/`](../prompts)). Cada arquivo tem uma função específica na correção. Os rascunhos aceitam `.jpg` ou `.png`. Tudo desta pasta, incluindo as entregas do Dashboard 2 (rascunho + justificativa), deve estar pronto até a Aula 22; a Aula 23 é para finalizar a implementação, fazer o deploy e os ajustes finais.

| Arquivo                      | Quando    | O que é                                                                                      |
|-------------------------------|-----------|-----------------------------------------------------------------------------------------------|
| `rascunho-dashboard1.jpg`/`.png`     | Aula 21   | Foto do rascunho do layout do Dashboard 1, feito antes de codar                               |
| `rascunho-dashboard2.jpg`/`.png`     | Aula 22   | Mesma ideia, para o Dashboard 2 — desenhado só depois de definir widgets, variáveis e métricas |
| `justificativa-metricas.md`   | Aula 22   | Por que cada métrica/KPI do Dashboard 2 foi escolhida e o que ela comunica ao público-alvo     |

## Checklist — Aula 21

- [ ] `rascunho-dashboard1.jpg`/`.png`

## Checklist — Aula 22

- [ ] `rascunho-dashboard2.jpg`/`.png`
- [ ] `justificativa-metricas.md` preenchido (não só criado vazio)

## Checklist — entrega final (Aula 23)

- [ ] Os dois rascunhos
- [ ] `justificativa-metricas.md` completo

## Modelo de `justificativa-metricas.md`

Cada métrica indica **a variável** a que se refere, **o que mede**, **por que foi escolhida** e **o que comunica** a um público que não precisa captar as nuances da variável.

```markdown
# Justificativa das métricas — Dashboard 2

## Métrica 1: <nome>
- **Variável:** 
- **O que mede:** 
- **Por que foi escolhida:** 
- **O que comunica ao público-alvo:** 
```

### Exemplo preenchido

```markdown
## Métrica: Distribuição do colesterol em relação à mediana
- **Variável:** `chol` (colesterol sérico, mg/dl)
- **O que mede:** a proporção de pessoas da amostra abaixo, em torno e acima da mediana de `chol`,
  junto de algumas estatísticas descritivas (média, mediana, mínimo, máximo, desvio padrão).
  "Em torno" = dentro de ±10% da mediana (defina e explicite a faixa que você usar).
- **Por que foi escolhida:** dá uma visão simplificada e direta da variável, sem exigir leitura
  de histograma ou boxplot.
- **O que comunica ao público-alvo:** como está distribuída a amostra de forma resumida
  (ex.: "metade das pessoas está acima de X mg/dl"), para quem não consegue captar as
  nuances da variável.
```
