import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from src.data_loader import load_data


st.set_page_config(
    page_title="Saúde de baterias",
    layout="wide",
)

st.title("Saúde e falhas de baterias de veículos elétricos")


VARS_QUANT = [
    "vehicle_age_years",
    "battery_capacity_kwh",
    "odometer_km",
    "cycle_count",
    "battery_health_percent",
    "state_of_health",
    "internal_resistance",
    "charge_efficiency",
    "discharge_efficiency",
    "average_ambient_temperature",
    "cell_temperature_max",
    "aging_score",
    "predicted_remaining_life_cycles",
]

ROTULOS = {
    "vehicle_age_years": "Idade do veículo (anos)",
    "battery_capacity_kwh": "Capacidade da bateria (kWh)",
    "odometer_km": "Quilometragem (km)",
    "cycle_count": "Quantidade de ciclos",
    "battery_health_percent": "Saúde da bateria (%)",
    "state_of_health": "Estado de saúde (SOH)",
    "internal_resistance": "Resistência interna",
    "charge_efficiency": "Eficiência de carga",
    "discharge_efficiency": "Eficiência de descarga",
    "average_ambient_temperature": "Temperatura ambiente média",
    "cell_temperature_max": "Temperatura máxima da célula",
    "aging_score": "Índice de envelhecimento",
    "predicted_remaining_life_cycles": "Vida restante estimada (ciclos)",
}


def formatar_numero(valor, casas=2):
    """Formata números no padrão brasileiro."""
    if pd.isna(valor):
        return "—"

    texto = f"{valor:,.{casas}f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def slider_intervalo(serie, titulo, chave):
    """Cria um slider usando apenas valores numéricos finitos."""
    valores = serie.replace([np.inf, -np.inf], np.nan).dropna()

    if valores.empty:
        st.warning(f"Não há valores válidos para: {titulo}.")
        return None

    minimo = float(valores.min())
    maximo = float(valores.max())

    if minimo == maximo:
        st.caption(f"{titulo}: {formatar_numero(minimo)}")
        return minimo, maximo

    return st.slider(
        titulo,
        min_value=minimo,
        max_value=maximo,
        value=(minimo, maximo),
        step=0.1,
        format="%.2f",
        key=chave,
    )


def mostrar_dashboard1(dados, variaveis, intervalo):
    st.header("Correlação e distribuição")

    if intervalo is None:
        st.info("Não há dados válidos para aplicar o filtro.")
        return

    inicio, fim = intervalo

    filtrado = dados.loc[
        dados["battery_health_percent"].between(inicio, fim)
    ].copy()

    st.caption(
        f"{formatar_numero(len(filtrado), 0)} de "
        f"{formatar_numero(len(dados), 0)} registros selecionados."
    )

    if filtrado.empty:
        st.warning("Nenhum registro no intervalo. Amplie o filtro.")

    col_correlacao, col_distribuicao = st.columns(2)

    with col_correlacao:
        st.subheader("Correlação")

        if len(variaveis) < 2:
            st.warning("Selecione pelo menos duas variáveis.")

        elif len(filtrado) < 2:
            st.warning(
                "São necessários pelo menos dois registros "
                "para calcular a correlação."
            )

        else:
            matriz = filtrado[variaveis].corr(
                method="spearman",
                min_periods=2,
            )

            dados_correlacao = (
                matriz
                .rename_axis("variavel_x")
                .reset_index()
                .melt(
                    id_vars="variavel_x",
                    var_name="variavel_y",
                    value_name="correlacao",
                )
                .dropna(subset=["correlacao"])
            )

            dados_correlacao["variavel_x"] = (
                dados_correlacao["variavel_x"].map(ROTULOS)
            )
            dados_correlacao["variavel_y"] = (
                dados_correlacao["variavel_y"].map(ROTULOS)
            )

            if dados_correlacao.empty:
                st.info(
                    "Não há variação suficiente "
                    "para calcular a correlação."
                )

            else:
                ordem = [ROTULOS[col] for col in variaveis]

                heatmap = (
                    alt.Chart(dados_correlacao)
                    .mark_rect()
                    .encode(
                        x=alt.X(
                            "variavel_x:N",
                            title=None,
                            sort=ordem,
                            axis=alt.Axis(
                                labelAngle=-45,
                                labelLimit=180,
                            ),
                        ),
                        y=alt.Y(
                            "variavel_y:N",
                            title=None,
                            sort=ordem,
                            axis=alt.Axis(labelLimit=180),
                        ),
                        color=alt.Color(
                            "correlacao:Q",
                            title="Spearman",
                            scale=alt.Scale(
                                domain=[-1, 1],
                                domainMid=0,
                                scheme="blueorange",
                            ),
                        ),
                        tooltip=[
                            alt.Tooltip(
                                "variavel_x:N",
                                title="Variável 1",
                            ),
                            alt.Tooltip(
                                "variavel_y:N",
                                title="Variável 2",
                            ),
                            alt.Tooltip(
                                "correlacao:Q",
                                title="Correlação",
                                format=".2f",
                            ),
                        ],
                    )
                    .properties(height=380)
                )

                st.altair_chart(
                    heatmap,
                    use_container_width=True,
                )

                st.caption(
                    "Spearman: de −1 a +1. Variáveis constantes "
                    "ficam sem coeficiente. "
                    "Correlação não implica causalidade."
                )

    with col_distribuicao:
        st.subheader("Distribuição")

        variavel_distribuicao = st.selectbox(
            "Variável para distribuição",
            options=VARS_QUANT,
            index=VARS_QUANT.index("battery_health_percent"),
            format_func=ROTULOS.get,
            key="d1_variavel_distribuicao",
        )

        quantidade_intervalos = st.slider(
            "Quantidade de intervalos do histograma",
            min_value=5,
            max_value=50,
            value=20,
            key="d1_intervalos_histograma",
        )

        valores = filtrado[variavel_distribuicao].dropna()

        if valores.empty:
            st.info("Não há valores válidos na seleção.")

        else:
            contagens, limites = np.histogram(
                valores.to_numpy(),
                bins=quantidade_intervalos,
            )

            dados_histograma = pd.DataFrame(
                {
                    "inicio": limites[:-1],
                    "fim": limites[1:],
                    "quantidade": contagens,
                }
            )

            histograma = (
                alt.Chart(dados_histograma)
                .mark_bar(
                    color="#3288bd",
                    opacity=0.9,
                    binSpacing=1,
                )
                .encode(
                    x=alt.X(
                        "inicio:Q",
                        bin="binned",
                        title=ROTULOS[variavel_distribuicao],
                        scale=alt.Scale(zero=False),
                    ),
                    x2=alt.X2("fim:Q"),
                    y=alt.Y(
                        "quantidade:Q",
                        title="Quantidade de registros",
                        axis=alt.Axis(tickMinStep=1),
                    ),
                    tooltip=[
                        alt.Tooltip(
                            "inicio:Q",
                            title="Início",
                            format=".2f",
                        ),
                        alt.Tooltip(
                            "fim:Q",
                            title="Fim",
                            format=".2f",
                        ),
                        alt.Tooltip(
                            "quantidade:Q",
                            title="Registros",
                            format=",d",
                        ),
                    ],
                )
                .properties(height=380)
            )

            st.altair_chart(
                histograma,
                use_container_width=True,
            )

            st.caption(
                f"Distribuição de "
                f"{formatar_numero(len(valores), 0)} valores válidos. "
                "Cada intervalo inclui o limite inferior; "
                "somente o último inclui também o superior."
            )

    with st.expander("Conferir os dados filtrados"):
        colunas = list(
            dict.fromkeys(
                [
                    "battery_health_percent",
                    *variaveis,
                    variavel_distribuicao,
                ]
            )
        )

        if "falha_label" in filtrado.columns:
            colunas.append("falha_label")

        st.dataframe(filtrado[colunas].head(100))
        st.caption("Prévia das primeiras 100 linhas.")


def mostrar_dashboard2(dados, tipos, intervalo):
    st.header("Indicadores de saúde das baterias")

    if intervalo is None:
        st.info("Não há idades válidas para aplicar o filtro.")
        return

    inicio, fim = intervalo

    filtrado = dados.loc[
        dados["vehicle_type"].isin(tipos)
        & dados["vehicle_age_years"].between(inicio, fim)
    ].copy()

    st.caption(
        "Esta aba usa os filtros de tipo e idade do veículo. "
        "O filtro de saúde do Dashboard 1 não é aplicado aqui."
    )

    falhas_validas = filtrado.loc[
        filtrado["battery_failure"].isin([0, 1]),
        "battery_failure",
    ]

    total = len(filtrado)
    proporcao_falhas = falhas_validas.mean()
    saude_media = filtrado["battery_health_percent"].mean()
    ciclos_medios = filtrado["cycle_count"].mean()

    cartao1, cartao2, cartao3, cartao4 = st.columns(4)

    cartao1.metric(
        "Total de registros",
        formatar_numero(total, 0),
    )

    cartao2.metric(
        "Proporção com falha",
        (
            f"{formatar_numero(proporcao_falhas * 100)}%"
            if pd.notna(proporcao_falhas)
            else "—"
        ),
    )

    cartao3.metric(
        "Saúde média da bateria",
        (
            f"{formatar_numero(saude_media)}%"
            if pd.notna(saude_media)
            else "—"
        ),
    )

    cartao4.metric(
        "Média de ciclos",
        formatar_numero(ciclos_medios),
    )

    if filtrado.empty:
        st.warning(
            "Nenhum registro encontrado. "
            "Selecione tipos de veículo ou amplie a idade."
        )
        return

    st.caption(
        f"Indicadores calculados sobre "
        f"{formatar_numero(total, 0)} registros selecionados. "
        "Médias ignoram valores ausentes e a proporção "
        "considera somente classificações 0 ou 1."
    )

    st.subheader("Proporção de falhas por tipo de veículo")

    base_falhas = filtrado.loc[
        filtrado["battery_failure"].isin([0, 1])
    ]

    resumo = (
        base_falhas
        .groupby("vehicle_type", observed=True)
        .agg(
            registros=("battery_failure", "size"),
            com_falha=("battery_failure", "sum"),
            proporcao_falhas=("battery_failure", "mean"),
        )
        .reset_index()
    )

    if resumo.empty:
        st.info(
            "Não há classificações válidas de falha "
            "para construir o gráfico."
        )
        return

    grafico = (
        alt.Chart(resumo)
        .mark_bar(
            color="#3288bd",
            cornerRadiusTopLeft=4,
            cornerRadiusTopRight=4,
        )
        .encode(
            x=alt.X(
                "vehicle_type:N",
                title="Tipo de veículo",
                sort=alt.SortField(
                    field="proporcao_falhas",
                    order="descending",
                ),
                axis=alt.Axis(labelAngle=0),
            ),
            y=alt.Y(
                "proporcao_falhas:Q",
                title="Registros com falha (%)",
                axis=alt.Axis(format=".0%"),
                scale=alt.Scale(zero=True),
            ),
            tooltip=[
                alt.Tooltip(
                    "vehicle_type:N",
                    title="Tipo de veículo",
                ),
                alt.Tooltip(
                    "registros:Q",
                    title="Registros válidos",
                    format=",d",
                ),
                alt.Tooltip(
                    "com_falha:Q",
                    title="Com falha",
                    format=",d",
                ),
                alt.Tooltip(
                    "proporcao_falhas:Q",
                    title="Proporção com falha",
                    format=".2%",
                ),
            ],
        )
        .properties(height=400)
    )

    st.altair_chart(
        grafico,
        use_container_width=True,
    )

    st.caption(
        "Passe o mouse sobre as barras para conferir "
        "as contagens e os percentuais. "
        "Os resultados descrevem a amostra selecionada, "
        "sem prever falhas futuras."
    )

    with st.expander("Conferir os cálculos por tipo"):
        tabela = resumo.copy()
        tabela["percentual_falhas"] = (
            tabela["proporcao_falhas"] * 100
        )

        st.dataframe(
            tabela[
                [
                    "vehicle_type",
                    "registros",
                    "com_falha",
                    "percentual_falhas",
                ]
            ].rename(
                columns={
                    "vehicle_type": "Tipo de veículo",
                    "registros": "Registros válidos",
                    "com_falha": "Com falha",
                    "percentual_falhas": "Falhas (%)",
                }
            ).round(2)
        )


# Carregamento do CSV tratado.
# O cache permanece definido em src/data_loader.py.
try:
    df = load_data()
except (
    FileNotFoundError,
    pd.errors.EmptyDataError,
    pd.errors.ParserError,
) as exc:
    st.error(f"Não foi possível carregar os dados tratados: {exc}")
    st.info(
        "Confira o arquivo data/clean/ev_battery_clean.csv."
    )
    st.stop()


# Validação das colunas necessárias para os dois dashboards.
colunas_necessarias = VARS_QUANT + [
    "vehicle_type",
    "battery_failure",
]

faltantes = [
    col for col in colunas_necessarias
    if col not in df.columns
]

if faltantes:
    st.error(
        "Colunas ausentes no CSV: "
        + ", ".join(faltantes)
    )
    st.stop()

if df.empty:
    st.warning("O dataset tratado está vazio.")
    st.stop()

if any(
    not pd.api.types.is_numeric_dtype(df[col])
    for col in VARS_QUANT
):
    st.error("As variáveis quantitativas precisam ser numéricas.")
    st.stop()

# Converte infinitos em ausentes para os cálculos.
df = df.copy()
df[VARS_QUANT] = df[VARS_QUANT].replace(
    [np.inf, -np.inf],
    np.nan,
)


# Filtros independentes para cada dashboard.
with st.sidebar:
    st.header("Filtros")

    with st.expander("Dashboard 1", expanded=True):
        variaveis = st.multiselect(
            "Variáveis para correlação",
            options=VARS_QUANT,
            default=[
                "vehicle_age_years",
                "cycle_count",
                "battery_health_percent",
                "internal_resistance",
            ],
            format_func=ROTULOS.get,
            key="d1_variaveis",
        )

        intervalo_saude = slider_intervalo(
            df["battery_health_percent"],
            "Intervalo de saúde da bateria (%)",
            "d1_saude",
        )

    with st.expander("Dashboard 2", expanded=True):
        tipos_disponiveis = sorted(
            df["vehicle_type"].dropna().unique().tolist()
        )

        tipos_selecionados = st.multiselect(
            "Tipo de veículo",
            options=tipos_disponiveis,
            default=tipos_disponiveis,
            key="d2_tipos",
        )

        intervalo_idade = slider_intervalo(
            df["vehicle_age_years"],
            "Idade do veículo (anos)",
            "d2_idade",
        )


aba1, aba2 = st.tabs(
    [
        "Dashboard 1 — Correlação e distribuição",
        "Dashboard 2 — Indicadores",
    ]
)

with aba1:
    mostrar_dashboard1(
        df,
        variaveis,
        intervalo_saude,
    )

with aba2:
    mostrar_dashboard2(
        df,
        tipos_selecionados,
        intervalo_idade,
    )