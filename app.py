import pandas as pd
import streamlit as st

from src.data_loader import load_data


st.set_page_config(page_title="Saúde de baterias — Dashboard 1", layout="wide")
st.title("Saúde e falhas de baterias de veículos elétricos")
st.caption("Dashboard 1 — exploração de correlações e distribuições")

try:
    df = load_data()
except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError) as exc:
    st.error(f"Não foi possível carregar os dados tratados: {exc}")
    st.info("Execute o notebook da EDA até a última célula para gerar data/clean/ev_battery_clean.csv.")
    st.stop()

# Mesmas variáveis quantitativas utilizadas na EDA da Aula 11.
VARS_QUANT = [
    "vehicle_age_years", "battery_capacity_kwh", "odometer_km",
    "cycle_count", "battery_health_percent", "state_of_health",
    "internal_resistance", "charge_efficiency", "discharge_efficiency",
    "average_ambient_temperature", "cell_temperature_max",
    "aging_score", "predicted_remaining_life_cycles",
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
faltantes = [col for col in VARS_QUANT if col not in df.columns]
if faltantes:
    st.error("O CSV tratado não contém as colunas esperadas: " + ", ".join(faltantes))
    st.stop()
if df.empty:
    st.warning("O dataset tratado está vazio. Revise a exportação no notebook.")
    st.stop()
if any(not pd.api.types.is_numeric_dtype(df[col]) for col in VARS_QUANT):
    st.error("As variáveis quantitativas precisam ser numéricas. Revise o CSV exportado.")
    st.stop()

with st.sidebar:
    st.header("Filtros")
    variaveis = st.multiselect(
        "Variáveis para correlação",
        options=VARS_QUANT,
        default=["vehicle_age_years", "cycle_count", "battery_health_percent", "internal_resistance"],
        format_func=ROTULOS.get,
        help="Selecione pelo menos duas variáveis quantitativas.",
    )

    saude = df["battery_health_percent"].replace([float("inf"), -float("inf")], float("nan"))
    saude_valida = saude.dropna()
    if saude_valida.empty:
        st.error("Não há valores válidos de saúde da bateria para filtrar.")
        st.stop()
    minimo, maximo = float(saude_valida.min()), float(saude_valida.max())
    if minimo < maximo:
        inicio, fim = st.slider(
            "Intervalo de saúde da bateria (%)",
            min_value=minimo, max_value=maximo, value=(minimo, maximo),
            step=0.1, format="%.2f",
            help="O intervalo é inclusivo e filtra os registros das duas áreas.",
        )
    else:
        inicio = fim = minimo
        st.info(f"Todos os registros válidos têm saúde da bateria igual a {minimo:.2f}%.")

df_filtrado = df.loc[saude.between(inicio, fim)].copy()
st.caption(f"{len(df_filtrado):,} de {len(df):,} registros no intervalo selecionado.")
if saude.isna().any():
    st.caption("Registros sem valor válido de saúde da bateria são excluídos do filtro.")
if df_filtrado.empty:
    st.warning("Nenhum registro no intervalo escolhido. Amplie o filtro na barra lateral.")

col_correlacao, col_distribuicao = st.columns(2)
with col_correlacao:
    st.subheader("Correlação")
    if len(variaveis) < 2:
        st.warning("Selecione pelo menos duas variáveis para analisar a correlação.")
    else:
        st.write("Variáveis selecionadas: " + ", ".join(ROTULOS[col] for col in variaveis))
        st.info("O mapa de correlação será acrescentado na próxima aula.")
        # Próxima etapa: calcular e exibir df_filtrado[variaveis].corr().

with col_distribuicao:
    st.subheader("Distribuição")
    variavel_distribuicao = st.selectbox(
        "Variável para distribuição", options=VARS_QUANT,
        index=VARS_QUANT.index("battery_health_percent"), format_func=ROTULOS.get,
    )
    st.info("O histograma será acrescentado na próxima aula.")
    # Próxima etapa: histograma de df_filtrado[variavel_distribuicao].

with st.expander("Conferir os dados filtrados"):
    colunas_preview = list(dict.fromkeys(["battery_health_percent", *variaveis, variavel_distribuicao]))
    if "falha_label" in df_filtrado.columns:
        colunas_preview.append("falha_label")
    st.dataframe(df_filtrado[colunas_preview].head(100))
    st.caption("Prévia das primeiras 100 linhas; os filtros consideram todos os registros.")
