import streamlit as st
import pandas as pd
import plotly.express as px
from ctwp.database import (
    get_latest_consumption,
    get_current_rate,
    get_total_cost,
    get_cost_by_device,
    get_all_zones,
    get_devices_by_zone,
    get_cost_by_zone,
    get_consumption_by_zone,
    get_consumption_by_device,
    get_consumption_by_period,
)


def update_metrics(consumption_placeholder, rate_placeholder, cost_placeholder):
    # Fetch data from the database
    current_consumption = get_latest_consumption()
    current_rate = get_current_rate()
    total_cost = get_total_cost()

    # Update placeholders with real-time data
    consumption_placeholder.metric("Consumo Atual (kWh)", f"{current_consumption} kWh")
    rate_placeholder.metric("Tarifa Atual (R$/kWh)", f"R${current_rate}")
    cost_placeholder.metric("Custo Total (R$)", f"R${total_cost}")


def dashboard():
    # Application title
    st.title("CTWP")
    st.write(
        "**CTWP (Computational Thinking with Python)** é um sistema para gerenciamento de consumo energético, "
        "focado na redução de custos e aumento da eficiência. Ele oferece monitoramento em tempo real, seleção de fontes econômicas "
        "e relatórios detalhados para decisões informadas."
    )

    # Separator for sections
    st.markdown("---")

    # Section: Real-time metrics
    st.header("Métricas em Tempo Real")

    # Columns for metrics
    col1, col2, col3 = st.columns(3)

    # Placeholders for metrics
    consumption_placeholder = col1.empty()
    rate_placeholder = col2.empty()
    cost_placeholder = col3.empty()
    update_metrics(consumption_placeholder, rate_placeholder, cost_placeholder)

    # Button to update metrics
    if st.button("Atualizar Métricas"):
        update_metrics(consumption_placeholder, rate_placeholder, cost_placeholder)

    # Separator for reports
    st.markdown("---")

    # Section: Zones and Devices
    st.header("Zonas e Dispositivos")

    # Fetch all zones
    zones = get_all_zones()
    zone_options = {zone["Nome"]: zone["ID"] for zone in zones}

    # Dropdown for zones
    selected_zone = st.selectbox(
        "Selecione uma Zona:",
        options=zone_options.keys(),
        format_func=lambda x: f"Zona: {x}",
    )

    # Fetch devices for the selected zone
    if selected_zone:
        zone_id = zone_options[selected_zone]
        devices = get_devices_by_zone(zone_id)

        st.subheader(f"Dispositivos na Zona: {selected_zone}")
        if devices:
            st.dataframe(devices, use_container_width=True)
        else:
            st.write("Nenhum dispositivo encontrado para esta zona.")
    else:
        st.write("Selecione uma zona para visualizar os dispositivos.")

    # Separator for reports
    st.markdown("---")

    # Section: Efficiency reports
    st.header("Relatórios de Eficiência")

    # Display cost by zone
    st.subheader("Custo por Zona")
    cost_by_zone = get_cost_by_zone()
    if cost_by_zone:
        st.dataframe(cost_by_zone, use_container_width=True)
    else:
        st.write("Nenhum custo registrado por zona.")

    # Display cost by device table
    st.subheader("Custo por Dispositivo")
    cost_by_device = get_cost_by_device()
    if cost_by_device:
        st.dataframe(cost_by_device, use_container_width=True)
    else:
        st.write("Nenhum custo registrado por dispositivo.")

    # Separator for graphs
    st.markdown("---")

    # Section: Consumption Graphs
    st.header("Gráficos de Consumo")

    # Consumption by Zone
    st.subheader("Consumo Total por Zona")
    consumption_by_zone = get_consumption_by_zone()
    if consumption_by_zone:
        df_zone = pd.DataFrame(consumption_by_zone)
        fig_zone = px.bar(
            df_zone, x="Zona", y="Consumo Total (kWh)", title="Consumo por Zona"
        )
        st.plotly_chart(fig_zone, use_container_width=True)
    else:
        st.write("Nenhum dado de consumo disponível para as zonas.")

    # Consumption by Device
    st.subheader("Consumo Total por Dispositivo")
    consumption_by_device = get_consumption_by_device()
    if consumption_by_device:
        df_device = pd.DataFrame(consumption_by_device)
        fig_device = px.bar(
            df_device,
            x="Dispositivo",
            y="Consumo Total (kWh)",
            title="Consumo por Dispositivo",
        )
        st.plotly_chart(fig_device, use_container_width=True)
    else:
        st.write("Nenhum dado de consumo disponível para os dispositivos.")

    # Separator for period details
    st.markdown("---")

    # Section: Details by Period
    st.header("Detalhes por Período")

    # Period selector
    period_option = st.selectbox("Selecione o Período", ["Diário", "Semanal", "Mensal"])

    # Fetch consumption by period from the database
    consumption_by_period = get_consumption_by_period(period_option)

    # Display results based on selected period
    if consumption_by_period:
        df_period = pd.DataFrame(consumption_by_period)
        st.subheader(f"Consumo {period_option} por Zona")
        fig_period = px.bar(
            df_period,
            x="Zona",
            y="Consumo Total (kWh)",
            title=f"Consumo {period_option} por Zona",
        )
        st.plotly_chart(fig_period, use_container_width=True)
    else:
        st.write(f"Nenhum dado de consumo disponível para o período {period_option}.")
