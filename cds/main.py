import streamlit as st
from cds.database import (
    get_total_consumption_by_month,
    get_avg_consumption_per_capita,
    get_total_consumption_by_year,
    get_consumption_by_state,
    get_consumption_by_type,
    get_trends_by_state,
    get_all_states,
)
import plotly.express as px


def dashboard():
    st.title("CDS")
    st.write(
        "Bem-vindo à aba de análise de consumo de energia elétrica no Brasil. "
        "Aqui você encontrará métricas e tendências baseadas nos dados históricos de consumo dos últimos anos, "
        "fornecidos pela [Base dos Dados](https://basedosdados.org/dataset/3e31e540-81ba-4665-9e72-3f81c176adad?table=b955feef-1649-428b-ba46-bc891d2facc2)."
    )

    st.markdown("---")

    # Total consumption by year or by month in a specific year
    st.subheader("Consumo Total")

    # Adiciona uma opção para alternar entre Ano e Mês
    granularity = st.radio("Escolha a granularidade:", ["Ano", "Mês"], index=0)

    if granularity == "Ano":
        # Exibe o consumo total por ano
        total_consumption_by_year = get_total_consumption_by_year()
        fig_total = px.line(
            total_consumption_by_year,
            x="year",
            y="total_consumption",
            title="Consumo Total por Ano",
            labels={"year": "Ano", "total_consumption": "Consumo Total (MWh)"},
        )
        st.plotly_chart(fig_total, use_container_width=True)
    else:
        # Seleção de ano para visualizar os 12 meses
        selected_year = st.slider(
            "Selecione o ano para visualizar por mês:",
            min_value=2004,
            max_value=2023,
            value=2023,
        )
        total_consumption_by_month = get_total_consumption_by_month(selected_year)
        fig_total_month = px.line(
            total_consumption_by_month,
            x="month",
            y="total_consumption",
            title=f"Consumo Total por Mês em {selected_year}",
            labels={"month": "Mês", "total_consumption": "Consumo Total (MWh)"},
        )
        st.plotly_chart(fig_total_month, use_container_width=True)

    st.markdown("---")

    # Consumption by state for a specific year
    st.subheader("Consumo por Estado")
    selected_year = st.slider(
        "Selecione o ano:", min_value=2004, max_value=2023, value=2023
    )
    consumption_by_state = get_consumption_by_state(selected_year)
    fig_state = px.bar(
        consumption_by_state,
        x="state",
        y="total_consumption",
        title=f"Consumo por Estado ({selected_year})",
        labels={"state": "Estado", "total_consumption": "Consumo Total (MWh)"},
    )
    st.plotly_chart(fig_state, use_container_width=True)

    st.markdown("---")

    # Consumption by type
    st.subheader("Consumo por Tipo")
    consumption_by_type = get_consumption_by_type()
    fig_type = px.pie(
        consumption_by_type,
        names="consumption_type",
        values="total_consumption",
        title="Distribuição por Tipo de Consumo",
        labels={
            "consumption_type": "Tipo de Consumo",
            "total_consumption": "Consumo Total (MWh)",
        },
    )
    st.plotly_chart(fig_type, use_container_width=True)

    st.markdown("---")

    # Average consumption per capita
    st.subheader("Consumo Médio Per Capita por Estado")
    avg_consumption_per_capita = get_avg_consumption_per_capita()
    fig_per_capita = px.bar(
        avg_consumption_per_capita,
        x="state",
        y="avg_consumption_per_capita",
        title="Consumo Médio Per Capita por Estado",
        labels={
            "state": "Estado",
            "avg_consumption_per_capita": "Consumo Médio Per Capita (MWh)",
        },
    )
    st.plotly_chart(fig_per_capita, use_container_width=True)

    st.markdown("---")

    # Trends for a specific state
    st.subheader("Tendências de Consumo por Estado")
    all_states = get_all_states()
    state_code = st.selectbox("Selecione o estado (sigla):", all_states["code"])
    trends_by_state = get_trends_by_state(state_code)
    if not trends_by_state.empty:
        fig_trends = px.line(
            trends_by_state,
            x="year",
            y="total_consumption",
            title=f"Tendências de Consumo - {state_code}",
            labels={"year": "Ano", "total_consumption": "Consumo Total (MWh)"},
        )
        st.plotly_chart(fig_trends, use_container_width=True)
    else:
        st.warning(f"Nenhum dado encontrado para o estado: {state_code}")
