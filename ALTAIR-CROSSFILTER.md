# Reatividade entre gráficos (Altair)

Guia de apoio para o **Dashboard 2**, que usa Altair justamente para ter reatividade: selecionar algo em um gráfico filtra ou destaca os outros, como o *cross-filter* do Power BI. No Dashboard 1 o Altair também é bem-vindo (o Seaborn é permitido, mas o Altair é preferível).

No Altair isso não vem pronto, mas você declara uma **seleção** e conecta os gráficos a ela. Há três exemplos, do mais simples ao mais completo:

| # | Como o usuário seleciona | Para que serve | O que atualiza |
|---|---|---|---|
| 1 | **Clicar** (barra, ponto, legenda) | Categorias | Outros gráficos do mesmo objeto |
| 2 | **Arrastar uma área** | Faixas de valores numéricos | Outros gráficos do mesmo objeto |
| 3 | Clicar ou arrastar + `on_select` | Qualquer uma | **Python**: `st.metric`, tabelas, qualquer gráfico |

Os exemplos usam as colunas do dataset do projeto (`data/clean/dataset.csv`): `age`, `chol`, `sexo_label`, `doenca_cardiaca`.

## Exemplo 1: clicar numa barra filtra outro gráfico

```python
import altair as alt
import streamlit as st

from src.data_loader import load_data

df = load_data()

clique = alt.selection_point(fields=["sexo_label"])

barras = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x="sexo_label",
        y="count()",
        opacity=alt.condition(clique, alt.value(1), alt.value(0.3)),
    )
    .add_params(clique)
)

dispersao = (
    alt.Chart(df)
    .mark_point()
    .encode(x="age", y="chol", color="doenca_cardiaca")
    .transform_filter(clique)
)

st.altair_chart(barras | dispersao, width="stretch")
```

Clique em uma barra: a dispersão mostra só aquele sexo e as outras barras ficam esmaecidas. Clique em uma área vazia para limpar a seleção. Com `shift` + clique você seleciona mais de uma barra.

## Exemplo 2: arrastar uma área filtra outro gráfico

```python
import altair as alt
import streamlit as st

from src.data_loader import load_data

df = load_data()

area = alt.selection_interval()

dispersao = (
    alt.Chart(df)
    .mark_point()
    .encode(
        x="age",
        y="chol",
        color=alt.condition(area, "doenca_cardiaca", alt.value("lightgray")),
    )
    .add_params(area)
)

barras = (
    alt.Chart(df)
    .mark_bar()
    .encode(x="sexo_label", y="count()")
    .transform_filter(area)
)

st.altair_chart(dispersao | barras, width="stretch")
```

Arraste uma área na dispersão: as barras passam a contar só os pacientes selecionados, e os pontos fora da área ficam cinza.

### Peças-chave (exemplos 1 e 2)

- `alt.selection_point()`: seleção por **clique**. Use `fields=[...]` para selecionar por coluna (todos os pontos da mesma categoria de uma vez).
- `alt.selection_interval()`: seleção por **área** (arrastar). Exige eixos **quantitativos**.
- `.add_params(selecao)`: liga a seleção ao gráfico onde o usuário interage.
- `alt.condition(selecao, ...)`: destaca (cor, opacidade, tamanho) o que está dentro da seleção.
- `.transform_filter(selecao)`: mostra só o que está dentro da seleção.
- `|` junta os gráficos **lado a lado**; `&` junta **um embaixo do outro**.

### Atenção: a seleção só vale dentro do mesmo objeto

A seleção só se propaga entre gráficos combinados num único objeto (`|`, `&` ou camadas com `+`), exibido por **um só** `st.altair_chart`.

Dois `st.altair_chart` separados (por exemplo, um em cada `st.columns`) **não compartilham** seleção. Se o layout do seu rascunho pede gráficos em colunas diferentes, escolha:

- Combine os gráficos com `|` e exiba com uma só chamada, ou
- use o `on_select` (exemplo 3) e filtre os dados no Python.

## Exemplo 3: levando a seleção para o Python (`on_select`)

Com `on_select="rerun"`, o `st.altair_chart` devolve o que o usuário selecionou, e você usa isso nos KPIs, em tabelas ou em gráficos de outras colunas. Aqui, o clique numa barra atualiza as métricas:

```python
import altair as alt
import streamlit as st

from src.data_loader import load_data

df = load_data()

# A seleção precisa de um nome para ser lida depois
clique = alt.selection_point(name="clique", fields=["sexo_label"])

barras = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x="sexo_label",
        y="count()",
        opacity=alt.condition(clique, alt.value(1), alt.value(0.3)),
    )
    .add_params(clique)
)

evento = st.altair_chart(barras, key="barras", on_select="rerun", width="stretch")

# Para selection_point: lista de dicionários, um por item clicado. Vazia se não há seleção.
itens = evento.selection.get("clique", [])
sexos = [item["sexo_label"] for item in itens]
selecionado = df[df["sexo_label"].isin(sexos)] if sexos else df

st.metric("Pacientes", len(selecionado))
st.metric("Colesterol mediano (chol)", f"{selecionado['chol'].median():.0f} mg/dl")
```

Com `selection_interval(name="faixa")` a seleção volta de outro jeito: `{coluna: [mínimo, máximo]}`.

```python
for coluna, (minimo, maximo) in evento.selection.get("faixa", {}).items():
    selecionado = selecionado[selecionado[coluna].between(minimo, maximo)]
```

### Pontos de atenção

- **Dê um nome à seleção** (`name="clique"`) e leia pelo mesmo nome em `evento.selection`.
- **Use `key`** no `st.altair_chart`.
- **Sem seleção**, `evento.selection` vem vazio e `selecionado` fica igual ao `df` inteiro. Isso é o esperado (nenhum filtro).
- **Seleção que esvazia os dados:** `.median()` de uma tabela vazia dá `NaN`. Se for seu caso, proteja com `if selecionado.empty:` antes de mostrar a métrica.
- Combine com os filtros da sidebar: parta do `df_filtrado` do seu `app.py`, não do `df` bruto.
- **`on_select="rerun"` roda o app inteiro a cada seleção.** Mantenha o carregamento dos dados com `@st.cache_data`.

## Para aprofundar

- [Seleções no Vega-Lite](https://vega.github.io/vega-lite/docs/selection.html)
- [Interações no Altair](https://altair-viz.github.io/user_guide/interactions.html)
- [`st.altair_chart` na documentação do Streamlit](https://docs.streamlit.io/develop/api-reference/charts/st.altair_chart)
