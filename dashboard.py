import streamlit as st
import cds.main as cds
import ctwp.main as ctwp


tab1, tab2 = st.tabs(["CTWP", "CDS"])


with tab2:
    cds.dashboard()


with tab1:
    ctwp.dashboard()
