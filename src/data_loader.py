from pathlib import Path

import pandas as pd
import streamlit as st


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "clean" / "ev_battery_clean.csv"


@st.cache_data(ttl=60)
def load_data(path=DATA_PATH):
    """Lê apenas o CSV tratado pela EDA, com cache de até um minuto."""
    return pd.read_csv(path)
